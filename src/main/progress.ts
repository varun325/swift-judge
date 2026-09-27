import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs'
import { dirname } from 'node:path'
import { backfill } from '../shared/review'
import type { Progress, ProgressEntry } from '../shared/types'

interface Store {
  problems: Progress
  quiz: Record<string, boolean>
}

/** Small JSON store; writes go through a temp file + rename so a crash can't corrupt it. */
export class ProgressStore {
  private data: Store

  constructor(private readonly file: string) {
    this.data = { problems: {}, quiz: {} }
    if (existsSync(file)) {
      try {
        const parsed = JSON.parse(readFileSync(file, 'utf8')) as Partial<Store>
        this.data = { problems: parsed.problems ?? {}, quiz: parsed.quiz ?? {} }
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
    this.data.problems[id] = { ...this.get(id), ...patch }
    this.save()
  }

  clearDraft(id: string): void {
    const { draft: _draft, ...rest } = this.get(id)
    this.data.problems[id] = rest
    this.save()
  }

  quiz(): Record<string, boolean> {
    return this.data.quiz
  }

  answerQuiz(id: string, correct: boolean): void {
    this.data.quiz[id] = correct
    this.save()
  }
}
