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

export interface JudgeApi {
  listProblems(): Promise<ProblemSummary[]>
  getProblem(id: string): Promise<ProblemView>
  run(id: string, code: string): Promise<JudgeResult>
  submit(id: string, code: string): Promise<JudgeResult>
  saveDraft(id: string, code: string): Promise<void>
  resetDraft(id: string): Promise<void>
  revealSolution(id: string): Promise<string>
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
}

export type { ProgressEntry }
