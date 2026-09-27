import Editor, { type OnMount } from '@monaco-editor/react'
import { useCallback, useEffect, useRef, useState } from 'react'
import type { LearnBundle, ProblemView } from '../../../shared/api'
import type { JudgeResult, ReviewState } from '../../../shared/types'
import { monaco } from '../monaco'
import { RUN_KEY, SUBMIT_KEY } from '../platform'
import { Compass, compassNotes } from './Compass'
import { Hints } from './Hints'
import { Markdown } from './Markdown'
import { Results } from './Results'
import { dayKey, FIB_DAYS, intervalLabel } from '../../../shared/review'

/** Seconds → "m:ss" or "h:mm:ss" for video timestamps. */
function clock(seconds: number): string {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = String(seconds % 60).padStart(2, '0')
  return h ? `${h}:${String(m).padStart(2, '0')}:${s}` : `${m}:${s}`
}

type LeftTab = 'description' | 'learn' | 'solution'

interface Props {
  id: string
  solved: boolean
  draft?: string
  hintsRevealed: number
  review?: ReviewState
  onProgress: () => void
  onOpenBook: (path: string) => void
  onOpenPlayground: (pageId: string) => void
  onNext: () => void
}

const USER_FILE = { function: 'user.swift', stdio: 'main.swift', diagnostic: 'main.swift', predict: 'main.swift' }

export function ProblemWorkspace({ id, solved, draft, hintsRevealed, review, onProgress, onOpenBook, onOpenPlayground, onNext }: Props): React.JSX.Element {
  const [problem, setProblem] = useState<ProblemView>()
  const [learn, setLearn] = useState<LearnBundle>()
  const [left, setLeft] = useState<LeftTab>('description')
  const [code, setCode] = useState('')
  const [result, setResult] = useState<JudgeResult>()
  const [lastAction, setLastAction] = useState<'run' | 'submit'>()
  const [busy, setBusy] = useState<'run' | 'submit'>()
  const editorRef = useRef<Parameters<OnMount>[0]>(undefined)
  const saveTimer = useRef<ReturnType<typeof setTimeout>>(undefined)

  const load = useCallback(async () => {
    const [p, l] = await Promise.all([window.judge.getProblem(id), window.judge.getLearn(id)])
    setProblem(p)
    setLearn(l)
    return p
  }, [id])

  useEffect(() => {
    void load().then((p) => setCode(draft ?? p.starter))
    // draft is only an initial value; later changes come from our own saves
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [load])

  const isPredict = problem?.meta.mode === 'predict'

  const onChange = (value: string): void => {
    setCode(value)
    clearTimeout(saveTimer.current)
    saveTimer.current = setTimeout(() => void window.judge.saveDraft(id, value), 600)
  }

  const act = useCallback(
    async (kind: 'run' | 'submit') => {
      if (busy) return
      setBusy(kind)
      setLastAction(kind)
      try {
        const r = kind === 'run' ? await window.judge.run(id, code) : await window.judge.submit(id, code)
        setResult(r)
        if (kind === 'submit') {
          onProgress()
          if (r.verdict === 'accepted') await load()
        }
      } finally {
        setBusy(undefined)
      }
    },
    [busy, code, id, load, onProgress]
  )

  // Compiler diagnostics → inline editor markers.
  useEffect(() => {
    const model = editorRef.current?.getModel()
    if (!model || !problem) return
    const file = USER_FILE[problem.meta.mode]
    const markers = (result?.diagnostics ?? [])
      .filter((d) => d.file === file && d.severity !== 'note' && problem.meta.mode !== 'diagnostic')
      .map((d) => ({
        startLineNumber: d.line,
        startColumn: d.column,
        endLineNumber: d.line,
        endColumn: model.getLineMaxColumn(Math.min(d.line, model.getLineCount())),
        message: d.message,
        severity: d.severity === 'error' ? monaco.MarkerSeverity.Error : monaco.MarkerSeverity.Warning
      }))
    monaco.editor.setModelMarkers(model, 'swiftc', markers)
  }, [result, problem])

  // ⌘↵ run, ⌘⇧↵ submit
  const actRef = useRef(act)
  actRef.current = act
  useEffect(() => {
    const onKey = (e: KeyboardEvent): void => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault()
        void actRef.current(e.shiftKey ? 'submit' : 'run')
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  if (!problem) return <div className="empty">Loading…</div>
  const { meta } = problem

  const reset = async (): Promise<void> => {
    if (!confirm('Reset the editor to the starter code? Your draft will be discarded.')) return
    await window.judge.resetDraft(id)
    setCode(problem.starter)
    setResult(undefined)
    onProgress()
  }

  const today = dayKey(new Date())
  const reviewDue = review !== undefined && review.due <= today
  const startFromMemory = async (): Promise<void> => {
    await window.judge.resetDraft(id)
    setCode(problem.starter)
    setResult(undefined)
    onProgress()
  }

  const reveal = async (): Promise<void> => {
    if (!confirm('Reveal the reference solution? Try a few more submits first — the struggle is where the learning happens.')) return
    await window.judge.revealSolution(id)
    await load()
    onProgress()
  }

  return (
    <div className="workspace">
      <section className="pane left-pane">
        <div className="pane-tabs">
          <button className={left === 'description' ? 'active' : ''} onClick={() => setLeft('description')}>Description</button>
          <button className={left === 'learn' ? 'active' : ''} onClick={() => setLeft('learn')}>Learn</button>
          <button className={left === 'solution' ? 'active' : ''} onClick={() => setLeft('solution')}>
            Solution {solved ? '✓' : ''}
          </button>
        </div>
        <div className="pane-body">
          {left === 'description' && (
            <>
              <h1 className="problem-title">{meta.title}</h1>
              <div className="badges">
                <span className={`badge diff ${meta.difficulty}`}>{meta.difficulty}</span>
                <span className="badge">{meta.track}</span>
                <span className="badge">{meta.topic}</span>
                <span className="badge mode">{modeLabel(meta.mode)}</span>
                {meta.notesRef && <span className="badge notes">notes §{meta.notesRef}</span>}
                {meta.impact === 'core' && <span className="badge impact-core" title="The vital 20% of topics that carry ~80% of a Senior Staff iOS engineer's impact">Core 20%</span>}
                {meta.impact === 'edge' && <span className="badge impact-edge" title="Long-tail topic: part of the final 20% edge">Edge 80%</span>}
              </div>
              {reviewDue && (
                <div className="review-banner">
                  <div>
                    <strong>↻ Revisit due</strong> — solve it again from memory. An accepted submit today schedules the next
                    visit in {FIB_DAYS[Math.min(review.lapsed ? Math.max(0, review.step - 1) : review.step + 1, FIB_DAYS.length - 1)]} days.
                  </div>
                  <button onClick={() => void startFromMemory()}>Clear editor &amp; start from memory</button>
                </div>
              )}
              {review && !reviewDue && (
                <div className="review-next" title="Fibonacci spaced repetition">
                  ↻ Next revisit {review.due} ({intervalLabel(review.step)}, {review.reviews} review{review.reviews === 1 ? '' : 's'} so far)
                </div>
              )}
              <Markdown source={problem.statement} />
              {meta.jsBridge && (
                <details className="js-bridge">
                  <summary>Coming from JavaScript</summary>
                  <Markdown source={meta.jsBridge} />
                </details>
              )}
              <Compass
                meta={meta}
                onAnswer={() => {
                  const page = compassNotes(meta)
                  void window.judge.playground.ensure(page.title, page.code, page.notes).then(onOpenPlayground)
                }}
              />
              {problem.snippet && <Markdown source={'```swift\n' + problem.snippet + '\n```'} />}
              {meta.signature && (
                <div className="signature">
                  <div className="label">Signature the judge calls</div>
                  <Markdown source={'```swift\n' + signatureText(meta.signature) + '\n```'} />
                </div>
              )}
              {problem.visibleTests.length > 0 && meta.mode !== 'predict' && meta.mode !== 'diagnostic' && (
                <div className="examples">
                  <div className="label">
                    Visible tests ({problem.visibleTests.length}) · hidden tests: {problem.hiddenCount}
                  </div>
                  {problem.visibleTests.map((t) => (
                    <div key={t.name} className="example">
                      <span className="ex-name">{t.name}</span>
                      <code>{t.input}</code>
                    </div>
                  ))}
                </div>
              )}
              <Hints id={id} hints={meta.hints} initiallyRevealed={hintsRevealed} onReveal={onProgress} />
            </>
          )}
          {left === 'learn' && learn && <LearnPanel learn={learn} onOpenBook={onOpenBook} />}
          {left === 'solution' &&
            (problem.explanation !== undefined ? (
              <>
                <h2>Why it works</h2>
                <Markdown source={problem.explanation || '_No explanation yet._'} />
                {problem.solution && (
                  <>
                    <h2>Reference solution</h2>
                    <Markdown source={'```swift\n' + problem.solution + '\n```'} />
                  </>
                )}
              </>
            ) : (
              <div className="locked">
                <p>🔒 The solution and explanation unlock when you get <strong>Accepted</strong>.</p>
                <button className="ghost" onClick={reveal}>Reveal anyway</button>
              </div>
            ))}
        </div>
      </section>

      <section className="pane right-pane">
        <div className="editor-bar">
          <span className="file">{isPredict ? 'your predicted output' : USER_FILE[meta.mode]}</span>
          <div className="actions">
            <button className="ghost" onClick={reset} title="Reset to starter code">Reset</button>
            <button className="run" disabled={Boolean(busy)} onClick={() => void act('run')} title={RUN_KEY}>
              {busy === 'run' ? 'Running…' : '▶ Run'}
            </button>
            <button className="submit" disabled={Boolean(busy)} onClick={() => void act('submit')} title={SUBMIT_KEY}>
              {busy === 'submit' ? 'Judging…' : 'Submit'}
            </button>
          </div>
        </div>
        <div className="editor">
          <Editor
            language={isPredict ? 'plaintext' : 'swift'}
            theme="judge-dark"
            value={code}
            onChange={(v) => onChange(v ?? '')}
            onMount={(ed) => {
              editorRef.current = ed
            }}
            options={{
              fontSize: 14,
              fontFamily: 'SF Mono, Menlo, monospace',
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              tabSize: 4,
              automaticLayout: true,
              lineNumbers: isPredict ? 'off' : 'on',
              renderWhitespace: isPredict ? 'all' : 'none',
              padding: { top: 10 }
            }}
          />
        </div>
        <Results result={result} busy={busy} action={lastAction} onNext={onNext} />
      </section>
    </div>
  )
}

function LearnPanel({ learn, onOpenBook }: { learn: LearnBundle; onOpenBook: (p: string) => void }): React.JSX.Element {
  const book = learn.docs.filter((d) => d.book)
  const apple = learn.docs.filter((d) => d.url)
  return (
    <div className="learn">
      {apple.length > 0 && (
        <div className="doc-links ref-section">
          <div className="label">Apple Developer Documentation</div>
          {apple.map((d) => (
            <a key={d.url} className="doc-link" href={d.url} target="_blank" rel="noreferrer">↗ {d.title}</a>
          ))}
        </div>
      )}
      {book.length > 0 && (
        <div className="doc-links ref-section">
          <div className="label">The Swift Programming Language (offline)</div>
          {book.map((d) => (
            <button key={d.book} className="doc-link" onClick={() => onOpenBook(d.book!)}>📖 {d.title}</button>
          ))}
        </div>
      )}
      {learn.videos.length > 0 && (
        <div className="doc-links ref-section">
          <div className="label">Videos</div>
          {learn.videos.map((v) => (
            <a key={v.url} className="doc-link video-link" href={v.url} target="_blank" rel="noreferrer">
              ▶ {v.title}
              <span className="channel">
                {v.channel}
                {v.start !== undefined && <span className="timestamp"> · jumps to {clock(v.start)}</span>}
              </span>
              {v.moment && <span className="moment">“…{v.moment}…”</span>}
            </a>
          ))}
        </div>
      )}
      {learn.articles.length > 0 && (
        <div className="doc-links ref-section">
          <div className="label">Articles & guides</div>
          {learn.articles.map((a) => (
            <a key={a.url} className="doc-link" href={a.url} target="_blank" rel="noreferrer">
              ↗ {a.title}<span className="channel video-link"> {a.source}</span>
            </a>
          ))}
        </div>
      )}
      {learn.concepts.length > 0 && (
        <div className="concept-cards">
          <div className="label">Interview questions this problem covers</div>
          {learn.concepts.map((c) => (
            <details key={c.id} className="concept-card">
              <summary>{c.question}</summary>
              <Markdown source={c.answer} />
              <div className="sources">Asked in: {c.sources.join(' · ')}</div>
            </details>
          ))}
        </div>
      )}
      {learn.notes ? (
        <>
          <div className="label">From your notes — {learn.notes.title}</div>
          <Markdown source={learn.notes.markdown} />
        </>
      ) : (
        <p className="muted">No matching section in your notes for this problem — use the references above.</p>
      )}
    </div>
  )
}

function modeLabel(mode: ProblemView['meta']['mode']): string {
  return { function: 'implement function', stdio: 'stdin → stdout', diagnostic: 'compiler diagnostic', predict: 'predict output' }[mode]
}

function signatureText(sig: NonNullable<ProblemView['meta']['signature']>): string {
  const params = sig.params
    .map((p) => {
      const label = p.label && p.label !== p.name ? `${p.label} ` : ''
      return `${label}${p.name}: ${p.inout ? 'inout ' : ''}${p.type}`
    })
    .join(', ')
  const effects = `${sig.async ? ' async' : ''}${sig.throws ? ' throws' : ''}`
  const ret = sig.returns && sig.returns !== 'Void' ? ` -> ${sig.returns}` : ''
  return `func ${sig.name}(${params})${effects}${ret}`
}
