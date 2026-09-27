import type { ProblemSummary } from '../../../shared/types'
import { FIB_DAYS, intervalLabel, type DueItem } from '../../../shared/review'

interface Props {
  due: DueItem[]
  problems: ProblemSummary[]
  onOpen: (id: string) => void
  onClose: () => void
}

/** "Revisit today": the Fibonacci review queue, shown when the app opens. */
export function ReviewToday({ due, problems, onOpen, onClose }: Props): React.JSX.Element {
  const byId = new Map(problems.map((p) => [p.id, p]))
  const items = due.filter((d) => byId.has(d.id))
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal review-today" role="dialog" aria-label="Revisit today" onClick={(e) => e.stopPropagation()}>
        <header>
          <h2>↻ Revisit today</h2>
          <button className="close" onClick={onClose} aria-label="Close">×</button>
        </header>
        {items.length === 0 ? (
          <p className="muted">Nothing due today. Solved problems come back after 1, 1, 2, 3, 5, 8, 13… days.</p>
        ) : (
          <>
            <p className="muted">
              Re-solve these from memory. Each on-time solve pushes the next visit further out along the
              Fibonacci ladder ({FIB_DAYS.slice(0, 8).join(', ')}… days); a failed attempt brings it back sooner.
            </p>
            <ul>
              {items.map((d) => {
                const p = byId.get(d.id)!
                return (
                  <li key={d.id}>
                    <button data-id={d.id} onClick={() => onOpen(d.id)}>
                      <span className={`impact-dot ${p.impact ?? ''}`} />
                      <span className="title">{p.title}</span>
                      <span className="meta">
                        {p.topic} · after a {intervalLabel(d.review.step)}
                        {d.review.lapsed && ' · missed last time'}
                      </span>
                      <span className={`when ${d.overdue > 0 ? 'overdue' : ''}`}>
                        {d.overdue === 0 ? 'today' : `${d.overdue}d overdue`}
                      </span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </>
        )}
      </div>
    </div>
  )
}
