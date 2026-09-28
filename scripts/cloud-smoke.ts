/**
 * Live check of cloud sync against the Firebase project in firebase.config.json:
 * creates two throwaway accounts, syncs two simulated machines through real Auth + Firestore,
 * verifies the security rules keep accounts apart, then deletes everything it created.
 *   npx tsx scripts/cloud-smoke.ts
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { AuthClient, type Session } from '../src/main/cloud/auth'
import { loadFirebaseConfig } from '../src/main/cloud/config'
import { FirestoreRest } from '../src/main/cloud/firestore'
import { SyncEngine } from '../src/main/cloud/sync'
import { Playground } from '../src/main/playground'
import { ProgressStore } from '../src/main/progress'

const config = loadFirebaseConfig([join(import.meta.dirname, '..', 'firebase.config.json')])
if (!config) throw new Error('no firebase.config.json')
const auth = new AuthClient(config)
const store = new FirestoreRest(config)
const tmp = mkdtempSync(join(tmpdir(), 'swj-smoke-'))
const stamp = Date.now()
const results: [string, boolean, string?][] = []
const check = (name: string, ok: boolean, detail?: string): void => {
  results.push([name, ok, detail])
}

function machine(name: string, session: Session) {
  const progress = new ProgressStore(join(tmp, name, 'progress.json'))
  const playground = new Playground(join(tmp, name, 'playground'))
  const engine = new SyncEngine({
    store,
    idToken: (s) => new AuthClient(config!).idToken(s),
    progress,
    playground: () => playground,
    stateFile: join(tmp, name, 'sync.json'),
    removePage: async (id) => {
      for (const f of playground.filesFor(id)) rmSync(f)
    }
  })
  return { progress, playground, sync: () => engine.sync(session) }
}

const owner = await auth.signUp(`swift-judge-smoke-${stamp}@example.com`, `pw-${stamp}-smoke`)
const other = await new AuthClient(config).signUp(`swift-judge-smoke-other-${stamp}@example.com`, `pw-${stamp}-other`)
try {
  const a = machine('a', owner)
  a.progress.update('two-sum', { solved: true, attempts: 2, draft: 'func twoSum() {}' })
  a.progress.answerQuiz('193-l1-some-view', true)
  const page = a.playground.create('smoke notes', 'print("hi")', '# compass answers')
  const pushA = await a.sync()
  check('machine A uploads progress, quiz and pages', pushA.pushed >= 3, JSON.stringify(pushA))

  const b = machine('b', { ...owner })
  const pullB = await b.sync()
  check('machine B receives progress', b.progress.get('two-sum').solved === true && b.progress.get('two-sum').draft === 'func twoSum() {}')
  check('machine B receives quiz answers', b.progress.quiz()['193-l1-some-view'] === true)
  check('machine B receives Playground pages', b.playground.snapshot(page)?.notes === '# compass answers', JSON.stringify(pullB))

  b.progress.update('two-sum', { attempts: 5 })
  await b.sync()
  await a.sync()
  check('edits flow back to A (incremental pull by server time)', a.progress.get('two-sum').attempts === 5)

  // Regression: repeated edit → sync cycles within the 60 s pull overlap must not create conflict
  // copies (the pull re-delivers this machine's own uploads), and a deleted page must stay deleted.
  let phantom = 0
  for (let i = 1; i <= 4; i++) {
    a.playground.save(page, { notes: `# compass answers\n\nedit ${i}` })
    phantom += (await a.sync()).conflicts.length
  }
  check('editing and syncing repeatedly creates no conflict copies', phantom === 0 && !a.playground.list().some((p) => p.id.includes('-conflict')), `${phantom} phantom conflicts`)
  await b.sync()
  check('the other machine gets the latest edit', b.playground.snapshot(page)?.notes === '# compass answers\n\nedit 4')
  for (const f of a.playground.filesFor(page)) rmSync(f)
  await a.sync()
  await a.sync()
  await b.sync()
  check('a deleted page stays deleted on both machines', !a.playground.snapshot(page) && !b.playground.snapshot(page))

  // Security rules: another account can neither read nor write this user's data.
  const otherToken = await new AuthClient(config).idToken(other)
  const denied = async (fn: () => Promise<unknown>): Promise<boolean> => fn().then(() => false, (e) => /refused|403/.test(String(e.message)))
  check('rules: another user cannot read', await denied(() => store.changed(owner.uid, otherToken, 'problems')))
  check('rules: another user cannot write', await denied(() => store.write(owner.uid, otherToken, 'problems', [{ id: 'x', data: '{}', updatedAt: 1 }])))
  const unauth = await fetch(`https://firestore.googleapis.com/v1/projects/${config.projectId}/databases/(default)/documents/users/${owner.uid}/problems/two-sum`)
  check('rules: unauthenticated requests are refused', unauth.status === 403 || unauth.status === 401, String(unauth.status))
} finally {
  // Clean up: delete the documents, then the accounts.
  for (const session of [owner, other]) {
    const token = await new AuthClient(config).idToken(session)
    for (const collection of ['problems', 'quiz', 'playground'] as const) {
      const { docs } = await store.changed(session.uid, token, collection).catch(() => ({ docs: [] }))
      for (const d of docs) {
        await fetch(`https://firestore.googleapis.com/v1/projects/${config.projectId}/databases/(default)/documents/users/${session.uid}/${collection}/${encodeURIComponent(d.id)}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` }
        })
      }
    }
    await new AuthClient(config).deleteAccount(session)
  }
  rmSync(tmp, { recursive: true, force: true })
}
for (const [name, ok, detail] of results) console.log(`${ok ? '✓' : '✗'} ${name}${!ok && detail ? ` — ${detail}` : ''}`)
console.log('cleaned up: test documents and both throwaway accounts deleted')
process.exit(results.every((r) => r[1]) ? 0 : 1)
