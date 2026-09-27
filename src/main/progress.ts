import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs'
import { dirname } from 'node:path'
import { backfill } from '../shared/review'
import type { Progress, ProgressEntry } from '../shared/types'

interface Store {
  problems: Progress
  quiz: Record<string, boolean>
  /** When each quiz answer was given (ms), so the newest answer wins when machines sync. */
  quizAt: Record<string, number>
}

/** Small JSON store; writes go through a temp file + rename so a crash can't corrupt it. */
export class ProgressStore {
  private data: Store
  /** Called after every local change (cloud sync schedules an upload). */
  onChange?: () => void

  constructor(private readonly file: string) {
    this.data = { problems: {}, quiz: {}, quizAt: {} }
    if (existsSync(file)) {
      try {
        const parsed = JSON.parse(readFileSync(file, 'utf8')) as Partial<Store>
        this.data = { problems: parsed.problems ?? {}, quiz: parsed.quiz ?? {}, quizAt: parsed.quizAt ?? {} }
      } catch {
        renameSync(file, `${file}.corrupt-${Date.now()}`)
      }
    }
    // Problems solved before spaced repetition existed join the schedule from their solve date.
    let migrated = false
    for (const [id, entry] of Object.entries(this.data.problems)) {
      const review = backfill(entry)
      if (review) {
        this.data.problems[id] = { ...entry, review }
        migrated = true
      }
    }
    if (migrated) this.save()
  }

  private save(): void {
    mkdirSync(dirname(this.file), { recursive: true })
    const tmp = `${this.file}.tmp`
    writeFileSync(tmp, JSON.stringify(this.data, null, 2))
    renameSync(tmp, this.file)
  }

  all(): Progress {
    return this.data.problems
  }

  get(id: string): ProgressEntry {
    return this.data.problems[id] ?? { solved: false, attempts: 0 }
  }

  update(id: string, patch: Partial<ProgressEntry>): void {
    const now = Date.now()
    const prev = this.get(id)
    const draftChanged = 'draft' in patch && patch.draft !== prev.draft
    this.data.problems[id] = { ...prev, ...patch, updatedAt: now, ...(draftChanged ? { draftUpdatedAt: now } : {}) }
    this.save()
    this.onChange?.()
  }

  clearDraft(id: string): void {
    const { draft: _draft, ...rest } = this.get(id)
    const now = Date.now()
    this.data.problems[id] = { ...rest, updatedAt: now, draftUpdatedAt: now }
    this.save()
    this.onChange?.()
  }

  /** Store a value merged from the cloud (no change notification: it's already in sync). */
  putFromCloud(id: string, entry: ProgressEntry): void {
    this.data.problems[id] = entry
    this.save()
  }

  /** Quiz answers with their timestamps, for sync. */
  quizState(): Record<string, { correct: boolean; at: number }> {
    return Object.fromEntries(Object.entries(this.data.quiz).map(([id, correct]) => [id, { correct, at: this.data.quizAt[id] ?? 0 }]))
  }

  putQuizFromCloud(state: Record<string, { correct: boolean; at: number }>): void {
    this.data.quiz = Object.fromEntries(Object.entries(state).map(([id, v]) => [id, v.correct]))
    this.data.quizAt = Object.fromEntries(Object.entries(state).map(([id, v]) => [id, v.at]))
    this.save()
  }

  quiz(): Record<string, boolean> {
    return this.data.quiz
  }

  answerQuiz(id: string, correct: boolean): void {
    this.data.quiz[id] = correct
    this.data.quizAt[id] = Date.now()
    this.save()
    this.onChange?.()
  }
}
