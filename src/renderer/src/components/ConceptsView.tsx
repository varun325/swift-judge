import { useEffect, useMemo, useState } from 'react'
import type { Concept, ProblemSummary, Progress } from '../../../shared/types'
import { Markdown } from './Markdown'

interface Props {
  problems: ProblemSummary[]
  progress: Progress
  onOpen: (id: string) => void
}

/** Every interview question from the sources, with the judged problems that drill it. */
export function ConceptsView({ problems, progress, onOpen }: Props): React.JSX.Element {
  const [concepts, setConcepts] = useState<Concept[]>([])
  const [query, setQuery] = useState('')
  const [source, setSource] = useState('all')
  useEffect(() => {
    void window.judge.listConcepts().then(setConcepts)
  }, [problems])

  const titles = useMemo(() => new Map(problems.map((p) => [p.id, p.title])), [problems])
  const sources = useMemo(() => [...new Set(concepts.flatMap((c) => c.sources))].sort(), [concepts])
  const q = query.trim().toLowerCase()
  const shown = concepts.filter(
    (c) =>
      (source === 'all' || c.sources.includes(source)) &&
      (!q || c.question.toLowerCase().includes(q) || c.topic.toLowerCase().includes(q))
  )
  const topics = [...new Set(shown.map((c) => c.topic))]
  const covered = concepts.filter((c) => c.problemIds.length > 0 && c.problemIds.every((id) => progress[id]?.solved)).length

  return (
    <div className="full-view">
      <div className="full-header">
        <h1>Concepts &amp; interview questions</h1>
        <p className="muted">
          {concepts.length} questions, merged from five interview-question sources · {covered} fully practiced
        </p>
        <div className="filter-row">
          <input placeholder="Search questions…" value={query} onChange={(e) => setQuery(e.target.value)} />
          <select value={source} onChange={(e) => setSource(e.target.value)}>
            <option value="all">All sources</option>
            {sources.map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="concept-list">
        {topics.map((topic) => (
          <section key={topic}>
            <h2>{topic}</h2>
            {shown
              .filter((c) => c.topic === topic)
              .map((c) => {
                const done = c.problemIds.filter((id) => progress[id]?.solved).length
                return (
                  <details key={c.id} className="concept-card">
                    <summary>
                      <span>{c.question}</span>
                      <span className={`pill ${c.problemIds.length && done === c.problemIds.length ? 'ok' : ''}`}>
                        {done}/{c.problemIds.length}
                      </span>
                    </summary>
                    <Markdown source={c.answer} />
                    <div className="practice">
                      {c.problemIds.map((id) => (
                        <button key={id} className="link" onClick={() => onOpen(id)}>
                          {progress[id]?.solved ? '✓' : '○'} {titles.get(id) ?? id}
                        </button>
                      ))}
                    </div>
                    <div className="sources">Asked in: {c.sources.join(' · ')}</div>
                  </details>
                )
              })}
          </section>
        ))}
      </div>
    </div>
  )
}
