import { useState } from 'react'
import { Markdown } from './Markdown'

const LABELS = ['Nudge', 'Approach', 'Almost there']

interface Props {
  id: string
  hints: string[]
  initiallyRevealed: number
  onReveal: () => void
}

/** Hints unlock one at a time, each more revealing than the last. */
export function Hints({ id, hints, initiallyRevealed, onReveal }: Props): React.JSX.Element | null {
  const [revealed, setRevealed] = useState(initiallyRevealed)
  if (hints.length === 0) return null

  const reveal = async (level: number): Promise<void> => {
    setRevealed(level)
    await window.judge.revealHint(id, level)
    onReveal()
  }

  return (
    <div className="hints">
      <div className="label">Hints · {revealed}/{hints.length} used</div>
      {hints.map((hint, i) => {
        const level = i + 1
        if (level <= revealed) {
          return (
            <div key={i} className="hint open" data-level={level}>
              <div className="hint-title">Hint {level} — {LABELS[i] ?? ''}</div>
              <Markdown source={hint} />
            </div>
          )
        }
        const next = level === revealed + 1
        return (
          <button
            key={i}
            className="hint locked-hint"
            data-level={level}
            disabled={!next}
            onClick={() => void reveal(level)}
            title={next ? 'Reveal this hint' : 'Open the previous hint first'}
          >
            {next ? '💡' : '🔒'} Show hint {level} — {LABELS[i] ?? ''}
          </button>
        )
      })}
    </div>
  )
}
