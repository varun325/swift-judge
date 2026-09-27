import { z } from 'zod'

export const Mode = z.enum(['function', 'stdio', 'diagnostic', 'predict'])
export type Mode = z.infer<typeof Mode>

export const Difficulty = z.enum(['easy', 'medium', 'hard'])
export type Difficulty = z.infer<typeof Difficulty>

export const Track = z.enum(['beginner', 'intermediate', 'advanced'])
export type Track = z.infer<typeof Track>

/**
 * How output is compared.
 *   function mode: json (default), json-unordered (top-level array order ignored),
 *                  json-unordered-deep (every array order ignored), float:<eps>
 *   stdio/predict: trimmed (default), exact, unorderedLines, float:<eps>
 */
export const Compare = z.union([
  z.enum(['json', 'json-unordered', 'json-unordered-deep', 'exact', 'trimmed', 'unorderedLines']),
  z.string().regex(/^float:[0-9.eE-]+$/)
])
export type Compare = z.infer<typeof Compare>

export const Param = z.object({
  /** External label. Omit to use `name`; use "_" for an unlabeled argument. */
  label: z.string().optional(),
  name: z.string(),
  /** Swift type, must be Codable (Int, String, [Int], [String: Int], Double?, ...). */
  type: z.string(),
  /** inout parameter: the judge passes `&copy` and reports the mutated value. */
  inout: z.boolean().optional()
})
export type Param = z.infer<typeof Param>

export const Signature = z.object({
  name: z.string(),
  params: z.array(Param),
  returns: z.string().default('Void'),
  throws: z.boolean().optional(),
  async: z.boolean().optional()
})
export type Signature = z.infer<typeof Signature>

export const DocLink = z.object({
  title: z.string(),
  /** Path inside the vendored swift-book (e.g. "LanguageGuide/Closures") */
  book: z.string().optional(),
  url: z.string().optional()
})
export type DocLink = z.infer<typeof DocLink>

export const ProblemMeta = z.object({
  id: z.string(),
  title: z.string(),
  track: Track,
  difficulty: Difficulty,
  topic: z.string(),
  concepts: z.array(z.string()).default([]),
  mode: Mode,
  notesRef: z.string().optional(),
  docs: z.array(DocLink).default([]),
  signature: Signature.optional(),
  compare: Compare.optional(),
  timeLimitMs: z.number().int().positive().default(2000),
  swiftVersion: z.enum(['5', '6']).default('6'),
  /** Starter code is intentionally broken (fix-the-bug problems); validate expects it to fail. */
  starterFails: z.boolean().optional()
})
export type ProblemMeta = z.infer<typeof ProblemMeta>

export const TestCase = z.object({
  name: z.string().optional(),
  /** function: object keyed by param name. stdio: stdin string. predict/diagnostic: unused. */
  input: z.unknown().optional(),
  /** Omit to derive from the reference solution. */
  expected: z.unknown().optional(),
  hidden: z.boolean().optional(),
  /** diagnostic mode: regex that must match one compiler diagnostic */
  pattern: z.string().optional(),
  /** diagnostic mode: "error" (default) | "warning" | "none" (must compile cleanly) */
  severity: z.enum(['error', 'warning', 'none']).optional()
})
export type TestCase = z.infer<typeof TestCase>

export interface Problem {
  meta: ProblemMeta
  dir: string
  statement: string
  starter: string
  solution: string
  /** predict mode: the program whose output you predict */
  snippet?: string
  explanation: string
  harness?: string
  tests: TestCase[]
}

/** What the renderer sees in the problem list. */
export interface ProblemSummary {
  id: string
  title: string
  track: Track
  difficulty: Difficulty
  topic: string
  mode: Mode
  concepts: string[]
}

export interface Diagnostic {
  file: string
  line: number
  column: number
  severity: 'error' | 'warning' | 'note'
  message: string
}

export type TestStatus = 'passed' | 'wrong' | 'runtime_error' | 'timeout' | 'skipped'

export interface TestResult {
  index: number
  name: string
  hidden: boolean
  status: TestStatus
  input?: string
  expected?: string
  actual?: string
  stdout?: string
  stderr?: string
  timeMs?: number
}

export type Verdict =
  | 'accepted'
  | 'wrong_answer'
  | 'compile_error'
  | 'runtime_error'
  | 'timeout'
  | 'internal_error'

export interface JudgeResult {
  verdict: Verdict
  diagnostics: Diagnostic[]
  compilerOutput: string
  tests: TestResult[]
  passed: number
  total: number
  compileMs: number
  message?: string
}

export interface ProgressEntry {
  solved: boolean
  attempts: number
  draft?: string
  solvedAt?: string
  revealed?: boolean
}
export type Progress = Record<string, ProgressEntry>

export interface Concept {
  id: string
  question: string
  topic: string
  answer: string
  sources: string[]
  problemIds: string[]
}

export interface QuizItem {
  id: string
  question: string
  choices: string[]
  answer: number
  explanation: string
  source?: string
}
