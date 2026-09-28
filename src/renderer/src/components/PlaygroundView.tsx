import type { OnMount } from '@monaco-editor/react'
import { useCallback, useDeferredValue, useEffect, useRef, useState } from 'react'
import type { PlaygroundRun, PlaygroundSummary } from '../../../shared/api'
import { monaco } from '../monaco'
import { FILE_MANAGER, RUN_KEY } from '../platform'
import { Markdown } from './Markdown'
import { SafeEditor } from './SafeEditor'

const SAVE_DELAY_MS = 500

function useStoredId(initial?: string): [string, (id: string) => void] {
  const [id, setId] = useState(() => {
    try {
      if (initial) localStorage.setItem('playground.page', initial)
      return initial ?? localStorage.getItem('playground.page') ?? ''
    } catch {
      return initial ?? ''
    }
  })
  const set = (next: string): void => {
    setId(next)
    try {
      localStorage.setItem('playground.page', next)
    } catch {
      /* convenience only */
    }
  }
  return [id, set]
}

/** Scratch Swift + an output panel + Markdown notes, saved as plain files on disk. */
interface Props {
  /** Page to show on mount (e.g. a Confusion Compass page opened from a problem). */
  openPage?: string
  /** Changes when another machine's pages were synced in. */
  cloudVersion?: number
}

export function PlaygroundView({ openPage, cloudVersion = 0 }: Props): React.JSX.Element {
  const [pages, setPages] = useState<PlaygroundSummary[]>([])
  const [root, setRoot] = useState('')
  const [pageId, setPageId] = useStoredId(openPage)
  const [code, setCode] = useState('')
  const [notes, setNotes] = useState('')
  // The preview renders at low priority so re-rendering Markdown never slows typing.
  const previewNotes = useDeferredValue(notes)
  const [stdin, setStdin] = useState('')
  const [showStdin, setShowStdin] = useState(false)
  const [previewOpen, setPreviewOpen] = useState(() => {
    try {
      return localStorage.getItem('playground.preview') !== 'closed'
    } catch {
      return true
    }
  })
  const togglePreview = (): void => {
    setPreviewOpen((open) => {
      try {
        localStorage.setItem('playground.preview', open ? 'closed' : 'open')
      } catch {
        /* convenience only */
      }
      return !open
    })
  }
  const [result, setResult] = useState<PlaygroundRun>()
  const [running, setRunning] = useState(false)
  const [saved, setSaved] = useState(true)
  const editorRef = useRef<Parameters<OnMount>[0]>(undefined)
  const pending = useRef<{ id: string; code?: string; notes?: string }>(undefined)
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined)
  // What's on disk for the current page — edits equal to it (e.g. the load itself) aren't saved.
  const loaded = useRef<{ code: string; notes: string }>({ code: '', notes: '' })
  /** Last keystroke in either editor (ms), so background syncs never reload the page mid-typing. */
  const lastInputAt = useRef(0)

  const flush = useCallback(async () => {
    clearTimeout(timer.current)
    const p = pending.current
    pending.current = undefined
    if (p) await window.judge.playground.save(p.id, { code: p.code, notes: p.notes })
    setSaved(true)
  }, [])

  const queueSave = (part: { code?: string; notes?: string }): void => {
    lastInputAt.current = Date.now()
    if (!pageId) return
    if ((part.code === undefined || part.code === loaded.current.code) && (part.notes === undefined || part.notes === loaded.current.notes)) return
    loaded.current = { code: part.code ?? loaded.current.code, notes: part.notes ?? loaded.current.notes }
    pending.current = { ...(pending.current?.id === pageId ? pending.current : {}), id: pageId, ...part }
    setSaved(false)
    clearTimeout(timer.current)
    timer.current = setTimeout(() => void flush(), SAVE_DELAY_MS)
  }

  const refreshList = useCallback(async () => {
    const list = await window.judge.playground.list()
    setPages(list)
    return list
  }, [])

  useEffect(() => {
    void window.judge.playground.root().then(setRoot)
    void refreshList().then((list) => {
      if (!list.some((p) => p.id === pageId) && list[0]) setPageId(list[0].id)
    })
    return () => void flush()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!pageId) return
    void window.judge.playground.load(pageId).then((page) => {
      loaded.current = { code: page.code, notes: page.notes }
      setCode(page.code)
      setNotes(page.notes)
      setResult(undefined)
    })
  }, [pageId])

  // Pages synced in from another machine: refresh the list. Reload the open page only if its file
  // really changed underneath us and you aren't typing: replacing the editor's text mid-edit loses
  // keystrokes and focus (a reload used to run on every sync notice, even when nothing had changed).
  const isTyping = (): boolean => Boolean(pending.current) || Date.now() - lastInputAt.current < 5000
  useEffect(() => {
    if (!cloudVersion) return
    void refreshList().then((list) => {
      if (!list.some((p) => p.id === pageId)) {
        if (list[0]) setPageId(list[0].id)
        return
      }
      if (isTyping()) return
      void window.judge.playground.load(pageId).then((page) => {
        if (isTyping()) return
        if (page.code === loaded.current.code && page.notes === loaded.current.notes) return
        loaded.current = { code: page.code, notes: page.notes }
        setCode(page.code)
        setNotes(page.notes)
      })
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cloudVersion])

  const switchTo = async (id: string): Promise<void> => {
    await flush()
    setPageId(id)
  }

  const runCode = useCallback(async () => {
    if (running) return
    setRunning(true)
    try {
      setResult(await window.judge.playground.run(code, stdin))
    } finally {
      setRunning(false)
    }
  }, [code, stdin, running])

  // ⌘↵ runs the playground.
  const runRef = useRef(runCode)
  runRef.current = runCode
  useEffect(() => {
    const onKey = (e: KeyboardEvent): void => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault()
        void runRef.current()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  // Compiler diagnostics → editor markers.
  useEffect(() => {
    const model = editorRef.current?.getModel()
    if (!model) return
    const markers = (result?.diagnostics ?? [])
      .filter((d) => d.file === 'main.swift' && d.severity !== 'note' && d.line <= model.getLineCount())
      .map((d) => ({
        startLineNumber: d.line,
        startColumn: d.column,
        endLineNumber: d.line,
        endColumn: model.getLineMaxColumn(d.line),
        message: d.message,
        severity: d.severity === 'error' ? monaco.MarkerSeverity.Error : monaco.MarkerSeverity.Warning
      }))
    monaco.editor.setModelMarkers(model, 'swiftc', markers)
  }, [result])

  // Electron doesn't implement window.prompt(), so page names are typed into an inline form.
  const [naming, setNaming] = useState<{ mode: 'new' | 'rename'; value: string; error?: string }>()

  const submitName = async (): Promise<void> => {
    if (!naming) return
    const title = naming.value.trim()
    if (!title) return setNaming({ ...naming, error: 'Type a name first' })
    await flush()
    try {
      const id = naming.mode === 'new' ? await window.judge.playground.create(title) : await window.judge.playground.rename(pageId, title)
      await refreshList()
      setPageId(id)
      setNaming(undefined)
    } catch (e) {
      setNaming({ ...naming, error: String(e).replace(/^Error: (Error invoking remote method '[^']+': )?(Error: )?/, '') })
    }
  }

  const deletePage = async (): Promise<void> => {
    if (!confirm(`Move "${pageId}" (code and notes) to the Trash?`)) return
    pending.current = undefined
    await window.judge.playground.remove(pageId)
    const list = await refreshList()
    if (list[0]) setPageId(list[0].id)
    else setPageId(await window.judge.playground.create('scratchpad'))
    await refreshList()
  }

  const appendRunToNotes = (): void => {
    if (!result) return
    const output = result.phase === 'compile' ? result.compilerOutput : [result.stdout, result.stderr].filter(Boolean).join('\n')
    const block = `\n\n### Run — ${new Date().toLocaleString()}\n\n\`\`\`swift\n${code.trimEnd()}\n\`\`\`\n\nOutput:\n\n\`\`\`\n${output.trimEnd() || '(no output)'}\n\`\`\`\n`
    const next = notes.trimEnd() + block
    setNotes(next)
    queueSave({ notes: next })
  }

  return (
    <div className="playground">
      <aside className="sidebar pg-pages">
        <div className="pg-pages-head">
          <strong>Pages</strong>
          <button className="ghost small-btn pg-new" onClick={() => setNaming({ mode: 'new', value: '' })}>+ New</button>
        </div>
        {naming && (
          <form
            className="pg-name"
            onSubmit={(e) => {
              e.preventDefault()
              void submitName()
            }}
          >
            <label className="muted small">{naming.mode === 'new' ? 'New page name' : `Rename “${pageId}” to`}</label>
            <input
              autoFocus
              value={naming.value}
              placeholder="e.g. closures practice"
              onChange={(e) => setNaming({ ...naming, value: e.target.value, error: undefined })}
              onKeyDown={(e) => e.key === 'Escape' && setNaming(undefined)}
            />
            {naming.error && <div className="pg-name-error">{naming.error}</div>}
            <div className="pg-name-actions">
              <button type="submit" className="run small-btn">{naming.mode === 'new' ? 'Create' : 'Rename'}</button>
              <button type="button" className="ghost small-btn" onClick={() => setNaming(undefined)}>Cancel</button>
            </div>
          </form>
        )}
        <div className="list">
          {pages.map((p) => (
            <button
              key={p.id}
              data-page={p.id}
              className={`problem-item ${p.id === pageId ? 'selected' : ''}`}
              onClick={() => void switchTo(p.id)}
            >
              <span className="title">{p.title}</span>
              <span className="muted small">{new Date(p.updatedAt).toLocaleDateString()}</span>
            </button>
          ))}
        </div>
        <div className="muted small pg-root" title={root}>Saved as .swift + .md files in<br />{root}</div>
      </aside>

      <section className="pg-main">
        <div className="editor-bar">
          <span className="file">{pageId}.swift <span className="muted">{saved ? '· saved' : '· saving…'}</span></span>
          <div className="actions">
            <button className="ghost pg-rename" onClick={() => setNaming({ mode: 'rename', value: pages.find((p) => p.id === pageId)?.title ?? pageId })}>Rename</button>
            <button className="ghost" onClick={() => void window.judge.playground.reveal(pageId)}>Show in {FILE_MANAGER}</button>
            <button className="ghost" onClick={() => void deletePage()}>Delete</button>
            <button className={`ghost ${showStdin ? 'on' : ''}`} onClick={() => setShowStdin(!showStdin)}>stdin</button>
            <button className="run pg-run" disabled={running} onClick={() => void runCode()} title={RUN_KEY}>
              {running ? 'Running…' : '▶ Run'}
            </button>
          </div>
        </div>
        <div className="pg-editor">
          <SafeEditor
            language="swift"
            theme="judge-dark"
            value={code}
            onChange={(v) => {
              setCode(v)
              queueSave({ code: v })
            }}
            onMount={(ed) => {
              editorRef.current = ed
            }}
            options={{ fontSize: 14, fontFamily: 'SF Mono, Menlo, monospace', minimap: { enabled: false }, tabSize: 4, automaticLayout: true, scrollBeyondLastLine: false, padding: { top: 10 } }}
          />
        </div>
        {showStdin && (
          <textarea
            className="pg-stdin"
            placeholder="Standard input for readLine()…"
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
          />
        )}
        <div className="pg-output">
          <div className="pg-output-head">
            <strong>Output</strong>
            {result && (
              <span className={`pill ${result.ok ? 'ok' : 'bad'}`}>
                {result.phase === 'compile'
                  ? 'compile error'
                  : result.ok
                    ? `exit 0 · ${result.ms} ms`
                    : result.signal
                      ? `crashed (${result.signal})`
                      : result.exitCode === null
                        ? 'stopped'
                        : `exit ${result.exitCode}`}
              </span>
            )}
            {result && result.compileMs > 0 && <span className="muted small">compiled in {result.compileMs} ms</span>}
            {result && <button className="link pg-append" onClick={appendRunToNotes}>Append run to notes ↘</button>}
          </div>
          {!result && !running && <div className="muted hint">Press ▶ Run or {RUN_KEY} to compile and run with swiftc.</div>}
          {running && <div className="muted hint">Compiling & running…</div>}
          {result?.phase === 'compile' && <pre className="console error">{result.compilerOutput}</pre>}
          {result?.phase === 'run' && (
            <>
              <pre className="console pg-stdout">{result.stdout || '(no output)'}</pre>
              {result.stderr && <pre className="console error">{result.stderr}</pre>}
              {result.compilerOutput && (
                <details className="warnings">
                  <summary>Compiler warnings</summary>
                  <pre className="console">{result.compilerOutput}</pre>
                </details>
              )}
            </>
          )}
        </div>
      </section>

      <section className={`pg-notes ${previewOpen ? '' : 'preview-collapsed'}`}>
        <div className="pg-panel-head">
          <strong>Notes</strong>
          <span className="muted small">Markdown · {pageId}.md</span>
        </div>
        <div className="pg-notes-editor">
          <SafeEditor
            language="markdown"
            theme="judge-dark"
            value={notes}
            onChange={(v) => {
              setNotes(v)
              queueSave({ notes: v })
            }}
            options={{ fontSize: 13, wordWrap: 'on', minimap: { enabled: false }, lineNumbers: 'off', automaticLayout: true, scrollBeyondLastLine: false, padding: { top: 10 } }}
          />
        </div>
        <div className="pg-preview">
          <button className="pg-panel-head pg-preview-toggle" onClick={togglePreview} aria-expanded={previewOpen} title={previewOpen ? 'Minimise preview' : 'Show preview'}>
            <strong>{previewOpen ? '▾' : '▸'} Preview</strong>
            <span className="muted small">{previewOpen ? 'live · click to minimise' : 'minimised · click to show'}</span>
          </button>
          {previewOpen && (
            <div className="pg-preview-body">
              <Markdown source={previewNotes || '_No notes yet._'} />
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
