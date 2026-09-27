import type {
  Concept, JudgeResult, Problem, ProblemSummary, Progress, ProgressEntry, QuizItem
} from './types'

/** A problem as the renderer sees it: the solution only once solved or revealed. */
export interface ProblemView {
  id: string
  meta: Problem['meta']
  statement: string
  starter: string
  snippet?: string
  explanation?: string
  solution?: string
  visibleTests: { name: string; input?: string }[]
  hiddenCount: number
}

export interface BookChapter {
  path: string
  title: string
}

export interface LearnBundle {
  notes?: { title: string; markdown: string }
  docs: { title: string; book?: string; url?: string }[]
  videos: { title: string; url: string; channel: string; start?: number; moment?: string }[]
  articles: { title: string; url: string; source: string }[]
  concepts: Concept[]
}

/** Account + sync state shown in the top bar. */
export interface CloudStatus {
  /** This build has a Firebase config; otherwise the app is offline-only and hides sign-in. */
  enabled: boolean
  signedIn: boolean
  email?: string
  state: 'idle' | 'syncing' | 'offline' | 'error'
  lastSync?: number
  error?: string
  /** Playground pages edited on two machines at once, kept as copies ("page → page-conflict"). */
  conflicts?: string[]
}

export interface SwiftInfo {
  version: string
  swiftc: string
  problemsRoot: string
  loadErrors: string[]
}

export interface PlaygroundSummary {
  id: string
  title: string
  updatedAt: string
}

export interface PlaygroundPage {
  id: string
  title: string
  code: string
  notes: string
}

export interface PlaygroundRun {
  ok: boolean
  phase: 'compile' | 'run'
  diagnostics: import('./types').Diagnostic[]
  compilerOutput: string
  stdout: string
  stderr: string
  exitCode: number | null
  signal?: string
  ms: number
  compileMs: number
}

export interface JudgeApi {
  platform: string
  listProblems(): Promise<ProblemSummary[]>
  getProblem(id: string): Promise<ProblemView>
  run(id: string, code: string): Promise<JudgeResult>
  submit(id: string, code: string): Promise<JudgeResult>
  saveDraft(id: string, code: string): Promise<void>
  resetDraft(id: string): Promise<void>
  revealSolution(id: string): Promise<string>
  revealHint(id: string, level: number): Promise<void>
  getProgress(): Promise<Progress>
  getLearn(id: string): Promise<LearnBundle>
  listBook(): Promise<BookChapter[]>
  getBookChapter(path: string): Promise<string>
  listConcepts(): Promise<Concept[]>
  listQuiz(): Promise<QuizItem[]>
  saveQuizAnswer(id: string, correct: boolean): Promise<void>
  getQuizProgress(): Promise<Record<string, boolean>>
  swiftInfo(): Promise<SwiftInfo>
  openExternal(url: string): Promise<void>
  onProblemsChanged(cb: () => void): () => void
  cloud: {
    status(): Promise<CloudStatus>
    signIn(email: string, password: string, create: boolean): Promise<CloudStatus>
    resetPassword(email: string): Promise<void>
    signOut(): Promise<CloudStatus>
    syncNow(): Promise<CloudStatus>
    /** Status changes and data pulled from another machine. */
    onChange(listener: (status: CloudStatus, dataChanged: boolean) => void): () => void
  }
  playground: {
    root(): Promise<string>
    list(): Promise<PlaygroundSummary[]>
    load(id: string): Promise<PlaygroundPage>
    save(id: string, part: { code?: string; notes?: string }): Promise<void>
    create(title: string): Promise<string>
    /** Open-or-create a page by title; existing content is kept. Returns the page id. */
    ensure(title: string, code: string, notes: string): Promise<string>
    rename(id: string, title: string): Promise<string>
    remove(id: string): Promise<void>
    reveal(id: string): Promise<void>
    run(code: string, stdin: string): Promise<PlaygroundRun>
  }
}

export type { ProgressEntry }
