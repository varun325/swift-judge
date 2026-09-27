import type { Progress, ProgressEntry, ReviewState } from './types'

/**
 * Fibonacci spaced repetition. After the first accepted solve a problem comes back in 1 day;
 * each on-time re-solve climbs one rung (1, 1, 2, 3, 5, 8, 13 … days). Failing a due review
 * drops it one rung, so shaky problems come back sooner.
 */
export const FIB_DAYS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

/** Local calendar day, "YYYY-MM-DD" (reviews are day-granular, in the learner's time zone). */
export function dayKey(date: Date): string {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

export function addDays(day: string, n: number): string {
  const [y, m, d] = day.split('-').map(Number)
  return dayKey(new Date(y, m - 1, d + n))
}

/** Whole days from `from` to `to` (both "YYYY-MM-DD"); DST-safe because it goes through UTC. */
export function daysBetween(from: string, to: string): number {
  const utc = (s: string): number => {
    const [y, m, d] = s.split('-').map(Number)
    return Date.UTC(y, m - 1, d)
  }
  return Math.round((utc(to) - utc(from)) / 86_400_000)
}

function start(today: string): ReviewState {
  return { step: 0, due: addDays(today, FIB_DAYS[0]), last: today, reviews: 0 }
}

/** The review state after a submission, or undefined when nothing changes. */
export function afterSubmit(entry: ProgressEntry, accepted: boolean, now: Date): ReviewState | undefined {
  const today = dayKey(now)
  const r = entry.review
  if (!r) return accepted ? start(today) : undefined
  if (r.due > today) return undefined // not due yet: practising early doesn't move the schedule
  if (!accepted) return r.lapsed ? undefined : { ...r, lapsed: true }
  const step = r.lapsed ? Math.max(0, r.step - 1) : Math.min(r.step + 1, FIB_DAYS.length - 1)
  return { step, due: addDays(today, FIB_DAYS[step]), last: today, reviews: r.reviews + 1 }
}

/** Solved problems from before reviews existed: schedule them from the day they were solved. */
export function backfill(entry: ProgressEntry): ReviewState | undefined {
  if (!entry.solved || entry.review) return undefined
  return start(entry.solvedAt ? dayKey(new Date(entry.solvedAt)) : dayKey(new Date()))
}

export interface DueItem {
  id: string
  review: ReviewState
  /** Days past the due date (0 = due today). */
  overdue: number
}

/** Problems to revisit today, most overdue first. */
export function dueReviews(progress: Progress, now: Date): DueItem[] {
  const today = dayKey(now)
  return Object.entries(progress)
    .flatMap(([id, e]) => (e.review && e.review.due <= today ? [{ id, review: e.review, overdue: daysBetween(e.review.due, today) }] : []))
    .sort((a, b) => b.overdue - a.overdue || a.id.localeCompare(b.id))
}

/** Human description of a rung: "day-3 interval". */
export function intervalLabel(step: number): string {
  const n = FIB_DAYS[Math.min(step, FIB_DAYS.length - 1)]
  return `${n}-day interval`
}
