import { describe, expect, it } from 'vitest'
import { addDays, afterSubmit, backfill, daysBetween, dueReviews, FIB_DAYS } from '../src/shared/review'
import type { ProgressEntry } from '../src/shared/types'

const at = (day: string): Date => {
  const [y, m, d] = day.split('-').map(Number)
  return new Date(y, m - 1, d, 12)
}

describe('fibonacci review schedule', () => {
  it('schedules the first review one day after the first accepted solve', () => {
    expect(afterSubmit({ solved: false, attempts: 0 }, true, at('2026-09-27'))).toEqual({
      step: 0, due: '2026-09-28', last: '2026-09-27', reviews: 0
    })
    expect(afterSubmit({ solved: false, attempts: 1 }, false, at('2026-09-27'))).toBeUndefined()
  })

  it('climbs 1, 1, 2, 3, 5, 8 days when every review is on time', () => {
    let entry: ProgressEntry = { solved: true, attempts: 1 }
    let day = '2026-01-01'
    const gaps: number[] = []
    entry.review = afterSubmit(entry, true, at(day))
    for (let i = 0; i < 6; i++) {
      const next = entry.review!.due
      gaps.push(daysBetween(day, next))
      day = next
      entry = { ...entry, review: afterSubmit(entry, true, at(day)) }
    }
    expect(gaps).toEqual([1, 1, 2, 3, 5, 8])
    expect(entry.review!.reviews).toBe(6)
  })

  it('ignores early practice and drops a rung after a failed review', () => {
    const review = { step: 3, due: '2026-03-10', last: '2026-03-07', reviews: 3 }
    expect(afterSubmit({ solved: true, attempts: 4, review }, true, at('2026-03-08'))).toBeUndefined()
    const lapsed = afterSubmit({ solved: true, attempts: 4, review }, false, at('2026-03-10'))!
    expect(lapsed.lapsed).toBe(true)
    const recovered = afterSubmit({ solved: true, attempts: 5, review: lapsed }, true, at('2026-03-11'))!
    expect(recovered).toEqual({ step: 2, due: addDays('2026-03-11', FIB_DAYS[2]), last: '2026-03-11', reviews: 4 })
  })

  it('late reviews still climb, measured from the day they are done', () => {
    const review = { step: 1, due: '2026-03-01', last: '2026-02-28', reviews: 1 }
    expect(afterSubmit({ solved: true, attempts: 2, review }, true, at('2026-03-20'))!.due).toBe('2026-03-22')
  })

  it('backfills solved problems and lists due ones, most overdue first', () => {
    expect(backfill({ solved: true, attempts: 1, solvedAt: new Date(2026, 8, 1, 9).toISOString() })!.due).toBe('2026-09-02')
    expect(backfill({ solved: false, attempts: 3 })).toBeUndefined()
    const due = dueReviews(
      {
        a: { solved: true, attempts: 1, review: { step: 0, due: '2026-09-27', last: '', reviews: 0 } },
        b: { solved: true, attempts: 1, review: { step: 0, due: '2026-09-20', last: '', reviews: 0 } },
        c: { solved: true, attempts: 1, review: { step: 0, due: '2026-09-28', last: '', reviews: 0 } }
      },
      at('2026-09-27')
    )
    expect(due.map((d) => [d.id, d.overdue])).toEqual([['b', 7], ['a', 0]])
  })

  it('crosses month ends and DST changes by calendar day', () => {
    expect(addDays('2026-01-31', 1)).toBe('2026-02-01')
    expect(addDays('2026-03-07', 3)).toBe('2026-03-10')
    expect(daysBetween('2026-10-30', '2026-11-03')).toBe(4)
  })
})
