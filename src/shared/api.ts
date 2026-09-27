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
  concepts: Concept[]
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
  playground: {
    root(): Promise<string>
    list(): Promise<PlaygroundSummary[]>
    load(id: string): Promise<PlaygroundPage>
    save(id: string, part: { code?: string; notes?: string }): Promise<void>
    create(title: string): Promise<string>
    rename(id: string, title: string): Promise<string>
    remove(id: string): Promise<void>
    reveal(id: string): Promise<void>
    run(code: string, stdin: string): Promise<PlaygroundRun>
  }
}

export type { ProgressEntry }
