import { useEffect, useState } from 'react'
import type { JudgeResult, TestResult, Verdict } from '../../../shared/types'
import { RUN_KEY, SUBMIT_KEY } from '../platform'

const VERDICT: Record<Verdict, { label: string; cls: string }> = {
  accepted: { label: 'Accepted', cls: 'ok' },
  wrong_answer: { label: 'Wrong Answer', cls: 'bad' },
  compile_error: { label: 'Compile Error', cls: 'bad' },
  runtime_error: { label: 'Runtime Error', cls: 'bad' },
  timeout: { label: 'Time Limit Exceeded', cls: 'bad' },
  internal_error: { label: 'Judge Error', cls: 'warn' }
}

interface Props {
  result?: JudgeResult
  busy?: 'run' | 'submit'
  action?: 'run' | 'submit'
  onNext: () => void
}

export function Results({ result, busy, action, onNext }: Props): React.JSX.Element {
  const [open, setOpen] = useState(0)
  useEffect(() => {
    const firstBad = result?.tests.findIndex((t) => t.status !== 'passed') ?? -1
    setOpen(firstBad >= 0 ? firstBad : 0)
  }, [result])

  if (busy) {
    return (
      <div className="results">
        <div className="verdict pending">{busy === 'run' ? 'Compiling & running visible tests…' : 'Compiling & judging all tests…'}</div>
      </div>
    )
  }
  if (!result) {
    return (
      <div className="results">
        <div className="muted hint">
          <strong>Run</strong> ({RUN_KEY}) checks the visible tests · <strong>Submit</strong> ({SUBMIT_KEY}) judges every test, hidden ones included
        </div>
      </div>
    )
  }

  const v = VERDICT[result.verdict]
  const test: TestResult | undefined = result.tests[open]
  return (
    <div className="results">
      <div className={`verdict ${v.cls}`}>
        <span>{v.label}</span>
        {result.total > 0 && (
          <span className="count">
            {result.passed}/{result.total} tests passed {action === 'run' ? '(visible only)' : ''}
          </span>
        )}
        {result.compileMs > 0 && <span className="muted small">compile {Math.round(result.compileMs)} ms</span>}
        {result.verdict === 'accepted' && action === 'submit' && (
          <button className="next" onClick={onNext}>Next problem →</button>
        )}
      </div>
      {result.message && result.verdict === 'internal_error' && <pre className="console">{result.message}</pre>}
      {result.verdict === 'compile_error' && <pre className="console error">{result.compilerOutput}</pre>}
      {result.tests.length > 0 && (
        <>
          <div className="case-tabs">
            {result.tests.map((t, i) => (
              <button key={i} className={`case ${t.status} ${i === open ? 'open' : ''}`} onClick={() => setOpen(i)}>
                {t.status === 'passed' ? '✓' : t.status === 'skipped' ? '–' : '✗'} {t.hidden ? `Hidden ${i + 1}` : t.name}
              </button>
            ))}
          </div>
          {test && <CaseDetail t={test} />}
        </>
      )}
      {result.verdict !== 'compile_error' && result.compilerOutput && result.diagnostics.some((d) => d.severity === 'warning') && (
        <details className="warnings">
          <summary>Compiler warnings</summary>
          <pre className="console">{result.compilerOutput}</pre>
        </details>
      )}
    </div>
  )
}

function CaseDetail({ t }: { t: TestResult }): React.JSX.Element {
  const statusText = {
    passed: 'Passed', wrong: 'Wrong answer', runtime_error: 'Runtime error', timeout: 'Time limit exceeded', skipped: 'Skipped'
  }[t.status]
  return (
    <div className="case-detail">
      <div className={`case-status ${t.status}`}>
        {statusText}
        {t.timeMs !== undefined && <span className="muted small"> · {t.timeMs} ms</span>}
      </div>
      {t.input !== undefined && <Field label="Input" value={t.input} />}
      {t.expected !== undefined && <Field label="Expected" value={t.expected} />}
      {t.actual !== undefined && <Field label="Your output" value={t.actual} bad={t.status === 'wrong'} />}
      {t.stdout && <Field label="Your print() output" value={t.stdout} />}
      {t.stderr && <Field label="stderr" value={t.stderr} bad />}
    </div>
  )
}

function Field({ label, value, bad }: { label: string; value: string; bad?: boolean }): React.JSX.Element {
  return (
    <div className="field">
      <div className="label">{label}</div>
      <pre className={bad ? 'bad' : ''}>{value === '' ? '(empty)' : value}</pre>
    </div>
  )
}
