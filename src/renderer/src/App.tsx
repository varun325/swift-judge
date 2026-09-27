import { useCallback, useEffect, useMemo, useState } from 'react'
import type { CloudStatus, SwiftInfo } from '../../shared/api'
import type { ProblemSummary, Progress } from '../../shared/types'
import { BookView } from './components/BookView'
import { ConceptsView } from './components/ConceptsView'
import { ProblemList } from './components/ProblemList'
import { PlaygroundView } from './components/PlaygroundView'
import { ProblemWorkspace } from './components/ProblemWorkspace'
import { QuizView } from './components/QuizView'
import { ReviewToday } from './components/ReviewToday'
import { AccountDialog, statusLine } from './components/AccountDialog'
import { dayKey, dueReviews } from '../../shared/review'

type Tab = 'problems' | 'playground' | 'concepts' | 'quiz' | 'book'

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
  const [reviewOpen, setReviewOpen] = useState(false)
  const [playgroundPage, setPlaygroundPage] = useState<string>()
  const [cloud, setCloud] = useState<CloudStatus>()
  const [accountOpen, setAccountOpen] = useState(false)
  /** Bumped when another machine's changes arrive, so views re-read their data. */
  const [cloudVersion, setCloudVersion] = useState(0)
  const [loaded, setLoaded] = useState(false)

  const refresh = useCallback(async () => {
    const [list, prog] = await Promise.all([window.judge.listProblems(), window.judge.getProgress()])
    setProblems(list)
    setProgress(prog)
    setLoaded(true)
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
    void window.judge.cloud.status().then(setCloud)
    return window.judge.cloud.onChange((status, dataChanged) => {
      setCloud(status)
      if (dataChanged) {
        void refresh()
        setCloudVersion((v) => v + 1)
      }
    })
  }, [refresh])

  useEffect(() => {
    if (!selected && problems.length) setSelected(problems[0].id)
  }, [problems, selected, setSelected])

  const due = useMemo(() => {
    const ids = new Set(problems.map((p) => p.id))
    return dueReviews(progress, new Date()).filter((d) => ids.has(d.id))
  }, [problems, progress])
  const dueIds = useMemo(() => new Set(due.map((d) => d.id)), [due])

  // On the first load each day, greet the learner with what to revisit.
  useEffect(() => {
    if (!loaded) return
    const today = dayKey(new Date())
    let shown: string | null = null
    try {
      shown = localStorage.getItem('review.shownOn')
    } catch {
      /* storage unavailable: just show it */
    }
    if (shown !== today && due.length > 0) setReviewOpen(true)
    try {
      localStorage.setItem('review.shownOn', today)
    } catch {
      /* per-viewer convenience only */
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loaded])

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
          {(['problems', 'playground', 'concepts', 'quiz', 'book'] as Tab[]).map((t) => (
            <button
              key={t}
              className={tab === t ? 'active' : ''}
              onClick={() => {
                setPlaygroundPage(undefined) // a page opened from a problem only applies to that one visit
                setTab(t)
              }}
            >
              {t === 'book' ? 'Swift Book' : t[0].toUpperCase() + t.slice(1)}
            </button>
          ))}
        </nav>
        <div className="status">
          {cloud?.enabled && (
            <button
              className={`account-button ${cloud.signedIn ? cloud.state : 'signed-out'}`}
              onClick={() => setAccountOpen(true)}
              title={statusLine(cloud)}
            >
              {!cloud.signedIn ? '☁ Sign in' : cloud.state === 'syncing' ? '⟳ Syncing' : cloud.state === 'idle' ? '☁ Synced' : cloud.state === 'offline' ? '☁ Offline' : '⚠ Sync issue'}
            </button>
          )}
          <button
            className={`review-button ${due.length ? 'has-due' : ''}`}
            onClick={() => setReviewOpen(true)}
            title="Fibonacci spaced repetition: problems to re-solve today"
          >
            ↻ {due.length} to revisit
          </button>
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
            <ProblemList problems={problems} progress={progress} dueIds={dueIds} selected={selected} onSelect={setSelected} />
            {selected && problems.some((p) => p.id === selected) ? (
              <ProblemWorkspace
                key={selected}
                id={selected}
                solved={Boolean(progress[selected]?.solved)}
                draft={progress[selected]?.draft}
                hintsRevealed={progress[selected]?.hintsRevealed ?? 0}
                review={progress[selected]?.review}
                onProgress={refresh}
                onOpenBook={openBook}
                onOpenPlayground={(id) => {
                  setPlaygroundPage(id)
                  setTab('playground')
                }}
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
        {tab === 'playground' && <PlaygroundView openPage={playgroundPage} cloudVersion={cloudVersion} />}
        {tab === 'concepts' && <ConceptsView problems={problems} progress={progress} onOpen={openProblem} />}
        {tab === 'quiz' && <QuizView key={cloudVersion} />}
        {tab === 'book' && <BookView initialPath={bookPath} />}
      </main>
      {accountOpen && cloud && <AccountDialog status={cloud} onClose={() => setAccountOpen(false)} />}
      {reviewOpen && (
        <ReviewToday
          due={due}
          problems={problems}
          onClose={() => setReviewOpen(false)}
          onOpen={(id) => {
            setReviewOpen(false)
            openProblem(id)
          }}
        />
      )}
    </div>
  )
}
