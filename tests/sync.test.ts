import { existsSync, mkdtempSync, rmSync, utimesSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, describe, expect, it } from 'vitest'
import type { CloudDoc, CloudStore, Collection } from '../src/main/cloud/firestore'
import { SyncEngine } from '../src/main/cloud/sync'
import { Playground } from '../src/main/playground'
import { ProgressStore } from '../src/main/progress'
import { mergeEntry } from '../src/shared/sync-merge'
import type { ProgressEntry } from '../src/shared/types'

/** In-memory Firestore stand-in with a server clock, counting reads and writes. */
class FakeStore implements CloudStore {
  docs = new Map<string, CloudDoc & { syncedAt: number }>()
  clock = Date.parse('2026-09-27T10:00:00Z')
  reads = 0
  writes = 0
  async changed(uid: string, _t: string, collection: Collection, since?: string) {
    const after = since ? Date.parse(since) : -Infinity
    const docs = [...this.docs.entries()]
      .filter(([k, d]) => k.startsWith(`${uid}/${collection}/`) && d.syncedAt > after)
      .map(([, d]) => ({ id: d.id, data: d.data, updatedAt: d.updatedAt, deleted: d.deleted }))
    this.reads += Math.max(1, docs.length)
    return { docs, readTime: new Date(this.clock).toISOString() }
  }
  async write(uid: string, _t: string, collection: Collection, docs: CloudDoc[]) {
    for (const d of docs) {
      this.clock += 120_000 // later than any overlap window, so incremental pulls are exercised
      this.docs.set(`${uid}/${collection}/${d.id}`, { ...d, syncedAt: this.clock })
      this.writes++
    }
  }
}

const dirs: string[] = []
afterEach(() => {
  for (const d of dirs.splice(0)) rmSync(d, { recursive: true, force: true })
})

function machine(store: FakeStore) {
  const dir = mkdtempSync(join(tmpdir(), 'swj-sync-'))
  dirs.push(dir)
  const progress = new ProgressStore(join(dir, 'progress.json'))
  const playground = new Playground(join(dir, 'playground'))
  const removed: string[] = []
  const engine = new SyncEngine({
    store,
    idToken: async () => 'token',
    progress,
    playground: () => playground,
    stateFile: join(dir, 'sync-state.json'),
    removePage: async (id) => {
      removed.push(id)
      for (const f of playground.filesFor(id)) rmSync(f)
    }
  })
  const session = { uid: 'user-1', email: 'a@example.com', refreshToken: 'r' }
  return { progress, playground, engine, removed, sync: () => engine.sync(session) }
}

describe('merge rules', () => {
  it('never loses progress and is order independent', () => {
    const a: ProgressEntry = { solved: true, attempts: 3, solvedAt: '2026-09-01T00:00:00Z', draft: 'old', draftUpdatedAt: 100, hintsRevealed: 1 }
    const b: ProgressEntry = { solved: false, attempts: 5, draft: 'new', draftUpdatedAt: 200, hintsRevealed: 2, revealed: true }
    const m = mergeEntry(a, b)
    expect(m).toMatchObject({ solved: true, attempts: 5, solvedAt: a.solvedAt, draft: 'new', hintsRevealed: 2, revealed: true })
    expect(mergeEntry(b, a)).toEqual(m)
  })
  it('keeps the review schedule from the most recent solve', () => {
    const older = { step: 3, due: '2026-10-01', last: '2026-09-20', reviews: 3 }
    const newer = { step: 1, due: '2026-09-29', last: '2026-09-27', reviews: 4, lapsed: false }
    expect(mergeEntry({ solved: true, attempts: 1, review: older }, { solved: true, attempts: 1, review: newer }).review).toEqual(newer)
  })
})

describe('sync between two machines', () => {
  it('moves progress, quiz answers and playground pages across, then syncs incrementally', async () => {
    const store = new FakeStore()
    const a = machine(store)
    a.progress.update('two-sum', { solved: true, attempts: 2, draft: 'func twoSum() {}' })
    a.progress.answerQuiz('q-1', true)
    const notes = a.playground.create('closures notes', 'let x = 1', '# my answers')
    await a.sync()

    const b = machine(store)
    const first = await b.sync()
    expect(first.changedProblems && first.changedQuiz && first.changedPlayground).toBe(true)
    expect(b.progress.get('two-sum')).toMatchObject({ solved: true, attempts: 2, draft: 'func twoSum() {}' })
    expect(b.progress.quiz()).toEqual({ 'q-1': true })
    expect(b.playground.load(notes)).toMatchObject({ code: 'let x = 1', notes: '# my answers' })
    // B's untouched welcome page doesn't clash with A's.
    expect(first.conflicts).toEqual([])

    // Nothing changed: an incremental sync pushes nothing and reads almost nothing.
    const writes = store.writes
    const reads = store.reads
    const idle = await b.sync()
    expect(idle.pushed).toBe(0)
    expect(store.writes).toBe(writes)
    expect(store.reads - reads).toBeLessThanOrEqual(3)
  })

  it('merges concurrent edits and propagates deletions', async () => {
    const store = new FakeStore()
    const a = machine(store)
    const b = machine(store)
    a.progress.update('leap-year', { attempts: 1 })
    const page = a.playground.create('shared page', 'print(1)', 'v1')
    await a.sync()
    await b.sync()

    // Offline on both: A solves it, B keeps attempting and writes a newer draft.
    a.progress.update('leap-year', { solved: true, attempts: 2, solvedAt: '2026-09-27T09:00:00Z' })
    await new Promise((r) => setTimeout(r, 5))
    b.progress.update('leap-year', { attempts: 4, draft: 'newest draft' })
    await a.sync()
    await b.sync()
    await a.sync()
    for (const m of [a, b]) expect(m.progress.get('leap-year')).toMatchObject({ solved: true, attempts: 4, draft: 'newest draft' })

    // B deletes the page; A removes it on its next sync.
    for (const f of b.playground.filesFor(page)) rmSync(f)
    await b.sync()
    await a.sync()
    expect(a.removed).toEqual([page])
    expect(a.playground.snapshot(page)).toBeUndefined()
  })

  it('keeps both versions when a page was edited on two machines between syncs', async () => {
    const store = new FakeStore()
    const a = machine(store)
    const b = machine(store)
    const page = a.playground.create('essay', '', 'first')
    await a.sync()
    await b.sync()
    a.playground.save(page, { notes: 'A edit' })
    b.playground.save(page, { notes: 'B edit' })
    // B's edit is newer.
    const later = new Date(Date.now() + 10_000)
    for (const f of b.playground.filesFor(page)) utimesSync(f, later, later)
    await b.sync()
    const res = await a.sync()
    expect(res.conflicts).toEqual([`${page} → ${page}-conflict`])
    expect(a.playground.load(page).notes).toBe('B edit')
    expect(a.playground.load(`${page}-conflict`).notes).toBe('A edit')
    // The copy reaches B too.
    await b.sync()
    expect(existsSync(join(b.playground.root, `${page}-conflict.md`))).toBe(true)
  })

  it('a new sign-in on a machine with existing progress merges it into the account', async () => {
    const store = new FakeStore()
    const a = machine(store)
    a.progress.update('fizzbuzz-stdio', { solved: true, attempts: 1 })
    await a.sync()
    const b = machine(store)
    b.progress.update('palindrome', { solved: true, attempts: 3 })
    await b.sync()
    await a.sync()
    expect(Object.keys(a.progress.all()).sort()).toEqual(['fizzbuzz-stdio', 'palindrome'])
    expect(Object.keys(b.progress.all()).sort()).toEqual(['fizzbuzz-stdio', 'palindrome'])
  })
})
