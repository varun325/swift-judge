import type { ProgressEntry, ReviewState } from './types'

/**
 * Merge rules for syncing progress between machines. They are field-wise rather than
 * last-writer-wins, so working on two machines never loses anything:
 * solved/revealed stay true once true, counters take the max, the newer draft wins and the
 * more advanced review schedule wins. merge(a, b) equals merge(b, a).
 */
export function mergeEntry(a: ProgressEntry | undefined, b: ProgressEntry | undefined): ProgressEntry {
  if (!a) return { ...b! }
  if (!b) return { ...a }
  const newerDraft = (a.draftUpdatedAt ?? 0) >= (b.draftUpdatedAt ?? 0) ? a : b
  const merged: ProgressEntry = {
    solved: a.solved || b.solved,
    attempts: Math.max(a.attempts, b.attempts)
  }
  const solvedAt = [a.solvedAt, b.solvedAt].filter(Boolean).sort()[0]
  if (solvedAt) merged.solvedAt = solvedAt
  if (a.revealed || b.revealed) merged.revealed = true
  const hints = Math.max(a.hintsRevealed ?? 0, b.hintsRevealed ?? 0)
  if (hints) merged.hintsRevealed = hints
  if (newerDraft.draft !== undefined) merged.draft = newerDraft.draft
  const draftAt = Math.max(a.draftUpdatedAt ?? 0, b.draftUpdatedAt ?? 0)
  if (draftAt) merged.draftUpdatedAt = draftAt
  const review = mergeReview(a.review, b.review)
  if (review) merged.review = review
  const updatedAt = Math.max(a.updatedAt ?? 0, b.updatedAt ?? 0)
  if (updatedAt) merged.updatedAt = updatedAt
  return merged
}

/** The schedule that has seen the most recent successful solve (ties: more reviews, later due date). */
function mergeReview(a?: ReviewState, b?: ReviewState): ReviewState | undefined {
  if (!a || !b) return a ?? b
  const key = (r: ReviewState): string => `${r.last}|${String(r.reviews).padStart(6, '0')}|${r.due}|${r.lapsed ? 1 : 0}`
  return key(a) >= key(b) ? a : b
}

/** Canonical JSON for comparing entries (key order independent). */
export function sameEntry(a: ProgressEntry | undefined, b: ProgressEntry | undefined): boolean {
  const canon = (e?: ProgressEntry): string =>
    e ? JSON.stringify(Object.keys(e).filter((k) => k !== 'updatedAt').sort().map((k) => [k, e[k as keyof ProgressEntry]])) : ''
  return canon(a) === canon(b)
}

/** A timestamped value, for records where the newest copy wins (quiz answers, Playground pages). */
export interface Stamped<T> {
  value: T
  updatedAt: number
  deleted?: boolean
}

export function newest<T>(a: Stamped<T> | undefined, b: Stamped<T> | undefined): Stamped<T> | undefined {
  if (!a || !b) return a ?? b
  return a.updatedAt >= b.updatedAt ? a : b
}
