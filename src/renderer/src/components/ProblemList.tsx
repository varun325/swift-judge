import { useMemo, useState } from 'react'
import type { ProblemSummary, Progress, Track } from '../../../shared/types'

const TRACKS: Track[] = ['beginner', 'intermediate', 'advanced', 'swiftui', 'frameworks', 'cs193p']
const TRACK_LABEL: Record<Track, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
  swiftui: 'SwiftUI',
  frameworks: 'Apple Frameworks',
  cs193p: 'Stanford CS193p (2025)'
}
const MODE_ICON: Record<ProblemSummary['mode'], string> = {
  function: 'ƒ',
  stdio: '⌨',
  diagnostic: '⚠',
  predict: '?'
}
const MODE_TITLE: Record<ProblemSummary['mode'], string> = {
  function: 'Implement a function',
  stdio: 'Read input, print output',
  diagnostic: 'Make the compiler report a specific error',
  predict: 'Predict the program output'
}

interface Props {
  problems: ProblemSummary[]
  progress: Progress
  /** Problems due for a spaced-repetition revisit today. */
  dueIds: Set<string>
  selected: string
  onSelect: (id: string) => void
}

export function ProblemList({ problems, progress, dueIds, selected, onSelect }: Props): React.JSX.Element {
  const [query, setQuery] = useState('')
  const [difficulty, setDifficulty] = useState<string>('all')
  const [hideSolved, setHideSolved] = useState(false)
  const [coreOnly, setCoreOnly] = useState(false)
  const [dueOnly, setDueOnly] = useState(false)
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({})

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return problems.filter(
      (p) =>
        (difficulty === 'all' || p.difficulty === difficulty) &&
        (!hideSolved || !progress[p.id]?.solved) &&
        (!coreOnly || p.impact === 'core') &&
        (!dueOnly || dueIds.has(p.id)) &&
        (!q || p.title.toLowerCase().includes(q) || p.topic.toLowerCase().includes(q) || p.concepts.some((c) => c.includes(q)))
    )
  }, [problems, progress, query, difficulty, hideSolved, coreOnly, dueOnly, dueIds])

  return (
    <aside className="sidebar">
      <div className="filters">
        <input placeholder="Search problems, topics…" value={query} onChange={(e) => setQuery(e.target.value)} />
        <div className="filter-row">
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <option value="all">All levels</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
          <label>
            <input type="checkbox" checked={hideSolved} onChange={(e) => setHideSolved(e.target.checked)} /> Hide solved
          </label>
          <label title="The vital 20% of topics that carry ~80% of a Senior Staff iOS engineer's impact">
            <input type="checkbox" checked={coreOnly} onChange={(e) => setCoreOnly(e.target.checked)} /> Core 20%
          </label>
          <label title="Solved problems whose Fibonacci revisit is due today">
            <input type="checkbox" checked={dueOnly} onChange={(e) => setDueOnly(e.target.checked)} /> Due ({dueIds.size})
          </label>
        </div>
      </div>
      <div className="list">
        {TRACKS.map((track) => {
          const items = filtered.filter((p) => p.track === track)
          if (!items.length) return null
          const all = problems.filter((p) => p.track === track)
          const done = all.filter((p) => progress[p.id]?.solved).length
          const topics = [...new Set(items.map((p) => p.topic))]
          return (
            <section key={track} className="track">
              <h3 onClick={() => setCollapsed({ ...collapsed, [track]: !collapsed[track] })}>
                <span>{collapsed[track] ? '▸' : '▾'} {TRACK_LABEL[track]}</span>
                <span className="track-progress">
                  {done}/{all.length}
                  <span className="bar"><span style={{ width: `${all.length ? (100 * done) / all.length : 0}%` }} /></span>
                </span>
              </h3>
              {!collapsed[track] &&
                topics.map((topic) => (
                  <div key={topic} className="topic">
                    <div className="topic-name">{topic}</div>
                    {items
                      .filter((p) => p.topic === topic)
                      .map((p) => (
                        <button
                          key={p.id}
                          data-id={p.id}
                          className={`problem-item ${p.id === selected ? 'selected' : ''}`}
                          onClick={() => onSelect(p.id)}
                        >
                          <span className={`impact-dot ${p.impact ?? ''}`} title={p.impact === 'core' ? 'Core 20% — high-impact topic' : 'Edge — long-tail mastery'} />
                          <span className={`check ${progress[p.id]?.solved ? 'done' : progress[p.id]?.attempts ? 'tried' : ''}`}>
                            {progress[p.id]?.solved ? '✓' : progress[p.id]?.attempts ? '•' : ''}
                          </span>
                          <span className="mode" title={MODE_TITLE[p.mode]}>{MODE_ICON[p.mode]}</span>
                          <span className="title">{p.title}</span>
                          {dueIds.has(p.id) && <span className="due-mark" title="Due for a revisit today">↻</span>}
                          {!p.supported && <span className="badge mac-only" title="Needs Apple frameworks — available on macOS">mac</span>}
                          <span className={`diff ${p.difficulty}`}>{p.difficulty[0].toUpperCase()}</span>
                        </button>
                      ))}
                  </div>
                ))}
            </section>
          )
        })}
        {!filtered.length && <div className="empty small">No problems match.</div>}
      </div>
    </aside>
  )
}
