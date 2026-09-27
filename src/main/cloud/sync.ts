import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs'
import { dirname } from 'node:path'
import { mergeEntry, sameEntry } from '../../shared/sync-merge'
import type { ProgressEntry } from '../../shared/types'
import type { Playground } from '../playground'
import { WELCOME_CODE, WELCOME_NOTES } from '../playground'
import type { ProgressStore } from '../progress'
import type { Session } from './auth'
import type { CloudDoc, CloudStore, Collection } from './firestore'

type QuizState = Record<string, { correct: boolean; at: number }>
interface PageValue {
  code: string
  notes: string
}

/** What this machine last saw in the cloud, per signed-in user: content hashes plus pull cursors. */
interface SyncState {
  uid: string
  cursor: Partial<Record<Collection, string>>
  synced: { problems: Record<string, string>; quiz?: string; playground: Record<string, string> }
}

const DELETED = 'deleted'
const QUIZ_DOC = 'answers'

function hash(value: unknown): string {
  return createHash('sha1').update(JSON.stringify(value)).digest('hex')
}

/** Canonical form of a progress entry (key order and the updatedAt stamp don't count as changes). */
function entryHash(e: ProgressEntry): string {
  const { updatedAt: _u, ...rest } = e
  return hash(Object.keys(rest).sort().map((k) => [k, rest[k as keyof typeof rest]]))
}
const pageHash = (p: PageValue): string => hash([p.code, p.notes])
const quizHash = (q: QuizState): string => hash(Object.keys(q).sort().map((k) => [k, q[k].correct, q[k].at]))

/** 60 s before a server read time: overlapping pulls are harmless (merges are idempotent), gaps aren't. */
function overlap(readTime: string): string {
  return new Date(Date.parse(readTime) - 60_000).toISOString()
}

export interface SyncDeps {
  store: CloudStore
  idToken: (session: Session) => Promise<string>
  progress: ProgressStore
  playground: () => Playground
  stateFile: string
  /** Remove a page deleted on another machine (the app moves it to the Trash). */
  removePage: (id: string) => Promise<void>
}

export interface SyncResult {
  pulled: number
  pushed: number
  /** Local data changed because of the pull (the UI should refresh). */
  changedProblems: boolean
  changedQuiz: boolean
  changedPlayground: boolean
  conflicts: string[]
}

/**
 * Local-first sync of progress, quiz answers and Playground pages with Firestore.
 * Pull (incremental by server time) → merge into local → push whatever differs from what the
 * cloud holds. Safe to call repeatedly; one sync runs at a time.
 */
export class SyncEngine {
  private running?: Promise<SyncResult>

  constructor(private readonly deps: SyncDeps) {}

  private loadState(uid: string): SyncState {
    try {
      const s = JSON.parse(readFileSync(this.deps.stateFile, 'utf8')) as SyncState
      if (s.uid === uid) return { ...s, synced: { problems: s.synced?.problems ?? {}, quiz: s.synced?.quiz, playground: s.synced?.playground ?? {} } }
    } catch {
      /* first sync for this user on this machine */
    }
    return { uid, cursor: {}, synced: { problems: {}, playground: {} } }
  }

  private saveState(state: SyncState): void {
    mkdirSync(dirname(this.deps.stateFile), { recursive: true })
    const tmp = `${this.deps.stateFile}.tmp`
    writeFileSync(tmp, JSON.stringify(state))
    renameSync(tmp, this.deps.stateFile)
  }

  /** Forget this machine's sync state (on sign-out), so the next sign-in does a full merge. */
  reset(): void {
    if (existsSync(this.deps.stateFile)) writeFileSync(this.deps.stateFile, '{}')
  }

  sync(session: Session): Promise<SyncResult> {
    this.running ??= this.run(session).finally(() => (this.running = undefined))
    return this.running
  }

  private async run(session: Session): Promise<SyncResult> {
    const { store } = this.deps
    const state = this.loadState(session.uid)
    const result: SyncResult = { pulled: 0, pushed: 0, changedProblems: false, changedQuiz: false, changedPlayground: false, conflicts: [] }
    const token = await this.deps.idToken(session)

    // ---- pull
    for (const collection of ['problems', 'quiz', 'playground'] as Collection[]) {
      const { docs, readTime } = await store.changed(session.uid, token, collection, state.cursor[collection])
      result.pulled += docs.length
      if (collection === 'problems') this.applyProblems(docs, state, result)
      else if (collection === 'quiz') this.applyQuiz(docs, state, result)
      else await this.applyPages(docs, state, result)
      if (readTime) state.cursor[collection] = overlap(readTime)
    }
    this.saveState(state)

    // ---- push what differs from the cloud
    const now = Date.now()
    const problemDocs: CloudDoc[] = []
    for (const [id, entry] of Object.entries(this.deps.progress.all())) {
      const h = entryHash(entry)
      if (state.synced.problems[id] !== h) problemDocs.push({ id, data: JSON.stringify(entry), updatedAt: entry.updatedAt ?? now })
    }
    const quiz = this.deps.progress.quizState()
    const quizDocs: CloudDoc[] =
      Object.keys(quiz).length && state.synced.quiz !== quizHash(quiz) ? [{ id: QUIZ_DOC, data: JSON.stringify(quiz), updatedAt: now }] : []
    const pageDocs: CloudDoc[] = []
    const pg = this.deps.playground()
    const localPages = new Set(pg.list().map((p) => p.id))
    for (const id of localPages) {
      const snap = pg.snapshot(id)
      if (!snap) continue
      if (state.synced.playground[id] !== pageHash(snap)) {
        pageDocs.push({ id, data: JSON.stringify({ code: snap.code, notes: snap.notes }), updatedAt: Math.round(snap.updatedAt) })
      }
    }
    for (const [id, h] of Object.entries(state.synced.playground)) {
      if (h !== DELETED && !localPages.has(id)) pageDocs.push({ id, data: 'null', updatedAt: now, deleted: true })
    }

    for (const [collection, docs] of [['problems', problemDocs], ['quiz', quizDocs], ['playground', pageDocs]] as [Collection, CloudDoc[]][]) {
      if (!docs.length) continue
      await store.write(session.uid, token, collection, docs)
      result.pushed += docs.length
      for (const d of docs) {
        if (collection === 'problems') state.synced.problems[d.id] = entryHash(JSON.parse(d.data) as ProgressEntry)
        else if (collection === 'quiz') state.synced.quiz = quizHash(JSON.parse(d.data) as QuizState)
        else state.synced.playground[d.id] = d.deleted ? DELETED : pageHash(JSON.parse(d.data) as PageValue)
      }
      this.saveState(state)
    }
    return result
  }

  private applyProblems(docs: CloudDoc[], state: SyncState, result: SyncResult): void {
    const { progress } = this.deps
    for (const d of docs) {
      const remote = JSON.parse(d.data) as ProgressEntry | null
      if (!remote) continue
      const local = progress.all()[d.id]
      const merged = mergeEntry(local, remote)
      if (!local || !sameEntry(merged, local)) {
        progress.putFromCloud(d.id, merged)
        result.changedProblems = true
      }
      state.synced.problems[d.id] = entryHash(remote)
    }
  }

  private applyQuiz(docs: CloudDoc[], state: SyncState, result: SyncResult): void {
    const doc = docs.find((d) => d.id === QUIZ_DOC)
    if (!doc) return
    const remote = (JSON.parse(doc.data) ?? {}) as QuizState
    const local = this.deps.progress.quizState()
    const merged: QuizState = { ...remote }
    for (const [id, v] of Object.entries(local)) if (!merged[id] || v.at > merged[id].at) merged[id] = v
    if (quizHash(merged) !== quizHash(local)) {
      this.deps.progress.putQuizFromCloud(merged)
      result.changedQuiz = true
    }
    state.synced.quiz = quizHash(remote)
  }

  private async applyPages(docs: CloudDoc[], state: SyncState, result: SyncResult): Promise<void> {
    const pg = this.deps.playground()
    for (const d of docs) {
      const known = state.synced.playground[d.id]
      const local = pg.snapshot(d.id)
      const localChanged = local ? known === undefined || pageHash(local) !== known : false
      if (d.deleted) {
        // Deleted elsewhere: remove here unless it was edited here after the deletion.
        if (local && !(localChanged && local.updatedAt > d.updatedAt)) {
          await this.deps.removePage(d.id)
          result.changedPlayground = true
        }
        state.synced.playground[d.id] = DELETED
        continue
      }
      const remote = JSON.parse(d.data) as PageValue
      const remoteHash = pageHash(remote)
      state.synced.playground[d.id] = remoteHash
      if (!local) {
        pg.putFromCloud(d.id, remote.code, remote.notes, d.updatedAt)
        result.changedPlayground = true
        continue
      }
      if (pageHash(local) === remoteHash) continue
      const untouchedDefault = local.code === WELCOME_CODE && local.notes === WELCOME_NOTES
      if (!localChanged || untouchedDefault) {
        pg.putFromCloud(d.id, remote.code, remote.notes, d.updatedAt)
        result.changedPlayground = true
        continue
      }
      // Edited on both machines since the last sync: keep both. The newer copy keeps the name.
      const copy = pg.freeId(`${d.id}-conflict`)
      if (local.updatedAt >= d.updatedAt) {
        pg.putFromCloud(copy, remote.code, remote.notes, d.updatedAt)
      } else {
        pg.putFromCloud(copy, local.code, local.notes, local.updatedAt)
        pg.putFromCloud(d.id, remote.code, remote.notes, d.updatedAt)
      }
      result.conflicts.push(`${d.id} → ${copy}`)
      result.changedPlayground = true
    }
  }
}
