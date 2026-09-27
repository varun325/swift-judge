import { useEffect, useState } from 'react'
import type { QuizItem } from '../../../shared/types'
import { Markdown } from './Markdown'

/** Quick-recall multiple choice. Not compiled — the judged problems do the heavy lifting. */
export function QuizView(): React.JSX.Element {
  const [items, setItems] = useState<QuizItem[]>([])
  const [done, setDone] = useState<Record<string, boolean>>({})
  const [picked, setPicked] = useState<Record<string, number>>({})
  const [topic, setTopic] = useState('all')

  useEffect(() => {
    void Promise.all([window.judge.listQuiz(), window.judge.getQuizProgress()]).then(([q, p]) => {
      setItems(q)
      setDone(p)
    })
  }, [])

  const choose = (item: QuizItem, i: number): void => {
    if (picked[item.id] !== undefined) return
    setPicked({ ...picked, [item.id]: i })
    const correct = i === item.answer
    setDone({ ...done, [item.id]: correct })
    void window.judge.saveQuizAnswer(item.id, correct)
  }

  const topics = [...new Set(items.map((i) => i.topic ?? 'Other'))]
  const shown = topic === 'all' ? items : items.filter((i) => (i.topic ?? 'Other') === topic)
  const right = shown.filter((i) => done[i.id]).length
  return (
    <div className="full-view">
      <div className="full-header">
        <h1>Quick quiz</h1>
        <p className="muted">
          <select className="quiz-topic" value={topic} onChange={(e) => setTopic(e.target.value)}>
            <option value="all">All topics ({items.length})</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t} ({items.filter((i) => (i.topic ?? 'Other') === t).length})
              </option>
            ))}
          </select>{' '}
          {right}/{shown.length} answered correctly (last attempt) ·{' '}
          <button className="link" onClick={() => setPicked({})}>retry all</button>
        </p>
      </div>
      <div className="quiz-list">
        {shown.map((item, n) => {
          const p = picked[item.id]
          return (
            <div key={item.id} className="quiz-card">
              <div className="q">
                <span className="num">{n + 1}.</span> <Markdown source={item.question} />
                {done[item.id] !== undefined && p === undefined && (
                  <span className={`pill ${done[item.id] ? 'ok' : 'bad'}`}>{done[item.id] ? 'got it' : 'missed'}</span>
                )}
              </div>
              <div className="choices">
                {item.choices.map((c, i) => (
                  <button
                    key={i}
                    className={`choice ${p !== undefined && i === item.answer ? 'right' : ''} ${p === i && i !== item.answer ? 'wrong' : ''}`}
                    onClick={() => choose(item, i)}
                  >
                    <Markdown source={c} />
                  </button>
                ))}
              </div>
              {p !== undefined && (
                <div className="explain">
                  <Markdown source={item.explanation} />
                  {item.source && <div className="sources">Source: {item.source}</div>}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
