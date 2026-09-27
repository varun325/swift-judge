import { useMemo, useState } from 'react'
import type { ProblemSummary, Progress, Track } from '../../../shared/types'

const TRACKS: Track[] = ['beginner', 'intermediate', 'advanced']
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
  selected: string
  onSelect: (id: string) => void
}

export function ProblemList({ problems, progress, selected, onSelect }: Props): React.JSX.Element {
  const [query, setQuery] = useState('')
  const [difficulty, setDifficulty] = useState<string>('all')
  const [hideSolved, setHideSolved] = useState(false)
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({})

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return problems.filter(
      (p) =>
        (difficulty === 'all' || p.difficulty === difficulty) &&
        (!hideSolved || !progress[p.id]?.solved) &&
        (!q || p.title.toLowerCase().includes(q) || p.topic.toLowerCase().includes(q) || p.concepts.some((c) => c.includes(q)))
    )
  }, [problems, progress, query, difficulty, hideSolved])

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
                <span>{collapsed[track] ? '▸' : '▾'} {track}</span>
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
                          <span className={`check ${progress[p.id]?.solved ? 'done' : progress[p.id]?.attempts ? 'tried' : ''}`}>
                            {progress[p.id]?.solved ? '✓' : progress[p.id]?.attempts ? '•' : ''}
                          </span>
                          <span className="mode" title={MODE_TITLE[p.mode]}>{MODE_ICON[p.mode]}</span>
                          <span className="title">{p.title}</span>
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
