import type { CompassKind, CompassQuestion, ProblemMeta } from '../../../shared/types'
import { Markdown } from './Markdown'

export const COMPASS_LABEL: Record<CompassKind, string> = {
  practice: 'In practice',
  js: 'vs JavaScript',
  java: 'vs Java',
  contrast: 'Compare',
  edge: 'Edge case'
}

/** The Playground notes page a learner answers the compass questions in. */
export function compassNotes(meta: ProblemMeta): { title: string; code: string; notes: string } {
  const questions = (meta.compass ?? [])
    .map((c, i) => `## ${i + 1}. ${COMPASS_LABEL[c.kind]}\n\n${c.q}\n\n**My answer (before looking anything up):**\n\n\n**What I found / verified:**\n\n`)
    .join('\n')
  return {
    title: `compass ${meta.id}`,
    code: `// Confusion Compass — ${meta.title}\n// Test your answers here: write the smallest program that proves (or disproves) each one.\n\n`,
    notes:
      `# Confusion Compass: ${meta.title}\n\n` +
      `Problem \`${meta.id}\` · ${meta.track} · ${meta.topic}\n\n` +
      `> Answer each question in your own words **before** researching. A wrong first answer is the point: ` +
      `the gap between it and what you verify is what sticks.\n\n` +
      questions
  }
}

interface Props {
  meta: ProblemMeta
  onAnswer: () => void
}

/** Questions meant to unsettle a shallow understanding; answered in the Playground, not revealed here. */
export function Compass({ meta, onAnswer }: Props): React.JSX.Element | null {
  const questions: CompassQuestion[] = meta.compass ?? []
  if (!questions.length) return null
  return (
    <details className="compass" open>
      <summary>
        Confusion Compass <span className="muted">· {questions.length} questions to wrestle with</span>
      </summary>
      <ol>
        {questions.map((c) => (
          <li key={c.q} data-kind={c.kind}>
            <span className={`compass-kind ${c.kind}`}>{COMPASS_LABEL[c.kind]}</span>
            <Markdown source={c.q} />
          </li>
        ))}
      </ol>
      <button className="compass-answer" onClick={onAnswer}>
        ✎ Answer in Playground
      </button>
    </details>
  )
}
