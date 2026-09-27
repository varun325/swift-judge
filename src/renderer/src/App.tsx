import { useCallback, useEffect, useState } from 'react'
import type { SwiftInfo } from '../../shared/api'
import type { ProblemSummary, Progress } from '../../shared/types'
import { BookView } from './components/BookView'
import { ConceptsView } from './components/ConceptsView'
import { ProblemList } from './components/ProblemList'
import { ProblemWorkspace } from './components/ProblemWorkspace'
import { QuizView } from './components/QuizView'

type Tab = 'problems' | 'concepts' | 'quiz' | 'book'

function useStored(key: string, initial: string): [string, (v: string) => void] {
  const [v, setV] = useState(() => {
    try {
      return localStorage.getItem(key) ?? initial
    } catch {
      return initial
    }
  })
  const set = (next: string): void => {
    setV(next)
    try {
      localStorage.setItem(key, next)
    } catch {
      /* per-viewer convenience only */
    }
  }
  return [v, set]
}

export function App(): React.JSX.Element {
  const [tab, setTab] = useStored('tab', 'problems')
  const [problems, setProblems] = useState<ProblemSummary[]>([])
  const [progress, setProgress] = useState<Progress>({})
  const [selected, setSelected] = useStored('selected', '')
  const [info, setInfo] = useState<SwiftInfo>()
  const [bookPath, setBookPath] = useState<string>()

  const refresh = useCallback(async () => {
    const [list, prog] = await Promise.all([window.judge.listProblems(), window.judge.getProgress()])
    setProblems(list)
    setProgress(prog)
  }, [])

  useEffect(() => {
    void refresh()
    void window.judge.swiftInfo().then(setInfo)
    return window.judge.onProblemsChanged(() => {
      void refresh()
      void window.judge.swiftInfo().then(setInfo)
    })
  }, [refresh])

  useEffect(() => {
    if (!selected && problems.length) setSelected(problems[0].id)
  }, [problems, selected, setSelected])

  const solved = problems.filter((p) => progress[p.id]?.solved).length
  const openProblem = (id: string): void => {
    setSelected(id)
    setTab('problems')
  }
  const openBook = (path: string): void => {
    setBookPath(path)
    setTab('book')
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="logo">◆</span> Swift Judge
        </div>
        <nav className="tabs">
          {(['problems', 'concepts', 'quiz', 'book'] as Tab[]).map((t) => (
            <button key={t} className={tab === t ? 'active' : ''} onClick={() => setTab(t)}>
              {t === 'book' ? 'Swift Book' : t[0].toUpperCase() + t.slice(1)}
            </button>
          ))}
        </nav>
        <div className="status">
          <span className="solved-count">
            {solved}/{problems.length} solved
          </span>
          <span className="swift-version" title={info?.swiftc}>
            {info?.version.replace(/\(.*\)/, '').trim() ?? '…'}
          </span>
        </div>
      </header>
      {info && info.loadErrors.length > 0 && (
        <div className="load-errors">
          <strong>{info.loadErrors.length} problem(s) failed to load:</strong>
          {info.loadErrors.map((e) => (
            <pre key={e}>{e}</pre>
          ))}
        </div>
      )}
      <main className="body">
        {tab === 'problems' && (
          <>
            <ProblemList problems={problems} progress={progress} selected={selected} onSelect={setSelected} />
            {selected && problems.some((p) => p.id === selected) ? (
              <ProblemWorkspace
                key={selected}
                id={selected}
                solved={Boolean(progress[selected]?.solved)}
                draft={progress[selected]?.draft}
                onProgress={refresh}
                onOpenBook={openBook}
                onNext={() => {
                  const i = problems.findIndex((p) => p.id === selected)
                  const next = problems.slice(i + 1).find((p) => !progress[p.id]?.solved) ?? problems[i + 1]
                  if (next) setSelected(next.id)
                }}
              />
            ) : (
              <div className="empty">Select a problem</div>
            )}
          </>
        )}
        {tab === 'concepts' && <ConceptsView problems={problems} progress={progress} onOpen={openProblem} />}
        {tab === 'quiz' && <QuizView />}
        {tab === 'book' && <BookView initialPath={bookPath} />}
      </main>
    </div>
  )
}
