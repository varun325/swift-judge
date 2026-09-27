import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import type {
  Compare, Diagnostic, JudgeResult, Problem, TestCase, TestResult, TestStatus, Verdict
} from '../../shared/types'
import { stringifyExact } from '../../shared/json'
import { compareJson, compareText } from './compare'
import { presentCompilerOutput, stripPaths } from './diagnostics'
import { generateDriver, parseDriverOutput, withQuietCrashes, wrapCustomHarness } from './harness'
import { mapLimit, run } from './runner'
import { compile, getCacheRoot, sha, typecheck, type SourceFile } from './toolchain'

/** Outcome of running one program against a list of test inputs. */
interface CaseOutput {
  status: 'ok' | 'runtime_error' | 'timeout' | 'skipped'
  output: string // JSON (function mode) or stdout (stdio mode)
  stdout: string
  stderr: string
  ms: number
}

type Built =
  | { ok: true; binary: string; diagnostics: Diagnostic[]; output: string; ms: number }
  | { ok: false; diagnostics: Diagnostic[]; output: string; ms: number }

const USER_FILE = { function: 'user.swift', stdio: 'main.swift', diagnostic: 'main.swift', predict: 'main.swift' } as const
const STDIO_PARALLELISM = 4

function driverFor(p: Problem): string {
  if (p.harness) return wrapCustomHarness(p.harness)
  if (!p.meta.signature) throw new Error(`${p.meta.id}: function mode needs a signature or harness.swift`)
  return generateDriver(p.meta.signature)
}

function sourcesFor(p: Problem, code: string): SourceFile[] {
  if (p.meta.mode === 'function') {
    return [{ name: 'user.swift', content: code }, { name: 'main.swift', content: driverFor(p) }]
  }
  return [{ name: 'main.swift', content: withQuietCrashes(code) }]
}

/** Drop warnings that come from the judge's own driver so the learner only sees their code's. */
function filterOutput(output: string, userFile: string): string {
  if (userFile === 'main.swift') return output
  const blocks: string[][] = []
  for (const line of output.split('\n')) {
    if (/^\S*\.swift:\d+:\d+: (error|warning|note):/.test(line) || blocks.length === 0) blocks.push([line])
    else blocks[blocks.length - 1].push(line)
  }
  return blocks
    .filter((b) => !/^\S*main\.swift:\d+:\d+: (warning|note):/.test(b[0]))
    .map((b) => b.join('\n'))
    .join('\n')
    .trim()
}

async function build(p: Problem, code: string): Promise<Built> {
  const userFile = USER_FILE[p.meta.mode]
  const res = await compile(sourcesFor(p, code), p.meta.swiftVersion)
  const diagnostics = res.diagnostics.filter((d) => d.file === userFile || d.severity === 'error')
  const output = presentCompilerOutput(filterOutput(stripPaths(res.output), userFile), userFile)
  if (!res.ok || !res.binary) return { ok: false, diagnostics, output, ms: res.ms }
  return { ok: true, binary: res.binary, diagnostics, output, ms: res.ms }
}

function crashReason(stderr: string, code: number | null, signal: string | null): string {
  const fatal = stderr.split('\n').find((l) => /Fatal error|fatal error|precondition|Assertion failed/i.test(l))
  if (fatal) return fatal.trim()
  if (signal === 'SIGTRAP' || signal === 'SIGILL') {
    return `runtime trap (${signal}) — usually integer overflow, force-unwrapping nil, an out-of-range index, or a failed precondition`
  }
  if (signal === 'SIGSEGV' || signal === 'SIGBUS') return `crash (${signal}) — often unbounded recursion (stack overflow)`
  // Windows reports crashes as NTSTATUS exit codes rather than signals.
  const status = code === null ? 0 : code >>> 0
  const windows: Record<number, string> = {
    0xc000001d: 'runtime trap (illegal instruction) — usually integer overflow, force-unwrapping nil, an out-of-range index, or a failed precondition',
    0x80000003: 'runtime trap (breakpoint) — usually integer overflow, force-unwrapping nil, an out-of-range index, or a failed precondition',
    0xc00000fd: 'crash (stack overflow) — often unbounded recursion',
    0xc0000005: 'crash (access violation)'
  }
  if (windows[status]) return windows[status]
  if (signal) return `process killed by ${signal}`
  return `exit code ${code}`
}

/** Function mode: one process runs many inputs; on a crash, resume after the crashing case. */
async function runFunctionCases(binary: string, inputs: unknown[], timeLimitMs: number): Promise<CaseOutput[]> {
  const results: CaseOutput[] = []
  let start = 0
  while (start < inputs.length) {
    const batch = inputs.slice(start)
    const res = await run(binary, [], {
      stdin: stringifyExact(batch),
      timeoutMs: timeLimitMs * batch.length + 5000,
      // Startup + one case must finish within the per-case limit (plus slack for process launch).
      progressTimeoutMs: timeLimitMs + 1000,
      progressMarker: '\u001FJUDGE'
    })
    if (res.stderr.includes('JUDGE_INPUT_ERROR')) {
      throw new Error(`test input doesn't decode into the function's parameter types:\n${res.stderr}`)
    }
    const { cases, trailing } = parseDriverOutput(res.stdout)
    for (const c of cases) {
      results.push({ status: 'ok', output: c.json, stdout: c.stdout, stderr: '', ms: c.ms })
    }
    const finishedAll = cases.length === batch.length
    if (finishedAll) {
      // Per-case time limit is enforced on the driver-measured time.
      for (let i = results.length - cases.length; i < results.length; i++) {
        if (results[i].ms > timeLimitMs) results[i].status = 'timeout'
      }
      break
    }
    // The case after the last reported one crashed or ran out of time.
    results.push({
      status: res.timedOut ? 'timeout' : 'runtime_error',
      output: '',
      stdout: trailing,
      stderr: res.timedOut ? `time limit exceeded (${timeLimitMs} ms)` : crashReason(res.stderr, res.code, res.signal) + '\n' + res.stderr,
      ms: res.ms
    })
    start += cases.length + 1
    if (res.timedOut) {
      // Like LeetCode: stop at the first time-out instead of paying the limit on every remaining case.
      while (results.length < inputs.length) {
        results.push({ status: 'skipped', output: '', stdout: '', stderr: 'not run — an earlier test exceeded the time limit', ms: 0 })
      }
      break
    }
  }
  return results
}

async function runStdioCases(binary: string, inputs: string[], timeLimitMs: number): Promise<CaseOutput[]> {
  return mapLimit(inputs, STDIO_PARALLELISM, async (stdin) => {
    const res = await run(binary, [], { stdin, timeoutMs: timeLimitMs + 500 })
    const status = res.timedOut ? 'timeout' : res.code === 0 ? 'ok' : 'runtime_error'
    return {
      status,
      output: res.stdout,
      stdout: res.stdout,
      stderr: status === 'runtime_error' ? crashReason(res.stderr, res.code, res.signal) + '\n' + res.stderr : res.stderr,
      ms: res.ms
    } satisfies CaseOutput
  })
}

async function runCases(p: Problem, binary: string, tests: TestCase[]): Promise<CaseOutput[]> {
  if (p.meta.mode === 'function') return runFunctionCases(binary, tests.map((t) => t.input ?? {}), p.meta.timeLimitMs)
  return runStdioCases(binary, tests.map((t) => (typeof t.input === 'string' ? t.input : '')), p.meta.timeLimitMs)
}

/**
 * Expected outputs for tests without an explicit `expected`: run the reference
 * solution on the same inputs. Cached on disk by content hash.
 */
export async function referenceOutputs(p: Problem, tests: TestCase[]): Promise<string[]> {
  const source = p.meta.mode === 'predict' ? (p.snippet ?? p.solution) : p.solution
  const key = sha(
    'ref-v1', p.meta.mode, p.meta.swiftVersion, source, p.harness ?? '',
    JSON.stringify(p.meta.signature ?? null), stringifyExact(tests.map((t) => t.input ?? null))
  )
  const dir = join(getCacheRoot(), 'refcache')
  const file = join(dir, `${key}.json`)
  if (existsSync(file)) return JSON.parse(readFileSync(file, 'utf8')) as string[]

  const problemForRef: Problem = p.meta.mode === 'predict' ? { ...p, meta: { ...p.meta, mode: 'stdio' } } : p
  const built = await build(problemForRef, source)
  if (!built.ok) throw new Error(`reference solution for ${p.meta.id} does not compile:\n${built.output}`)
  const outs = await runCases(problemForRef, built.binary, tests)
  const bad = outs.findIndex((o) => o.status !== 'ok')
  if (bad >= 0) {
    throw new Error(`reference solution for ${p.meta.id} failed test #${bad + 1} (${outs[bad].status}):\n${outs[bad].stderr}`)
  }
  const values = outs.map((o) => o.output)
  mkdirSync(dir, { recursive: true })
  writeFileSync(file, JSON.stringify(values))
  return values
}

function defaultCompare(p: Problem): Compare {
  return p.meta.compare ?? (p.meta.mode === 'function' ? 'json' : 'trimmed')
}

function showInput(p: Problem, t: TestCase): string | undefined {
  if (p.meta.mode === 'function') return stringifyExact(t.input ?? {})
  if (p.meta.mode === 'stdio') return typeof t.input === 'string' ? t.input : ''
  return undefined
}

function showExpected(p: Problem, expected: unknown): string {
  if (p.meta.mode === 'function') return typeof expected === 'string' ? expected : stringifyExact(expected)
  return String(expected)
}

function verdictFrom(tests: TestResult[]): Verdict {
  const worst: Record<TestStatus, Verdict | undefined> = {
    passed: undefined, skipped: undefined, wrong: 'wrong_answer', runtime_error: 'runtime_error', timeout: 'timeout'
  }
  for (const t of tests) {
    const v = worst[t.status]
    if (v) return v
  }
  return 'accepted'
}

function failure(verdict: Verdict, message: string, extra: Partial<JudgeResult> = {}): JudgeResult {
  return { verdict, diagnostics: [], compilerOutput: '', tests: [], passed: 0, total: 0, compileMs: 0, message, ...extra }
}

async function judgeDiagnostic(p: Problem, code: string, tests: TestCase[]): Promise<JudgeResult> {
  const { diagnostics, output, ms } = await typecheck({ name: 'main.swift', content: code }, p.meta.swiftVersion)
  const results: TestResult[] = tests.map((t, index) => {
    const severity = t.severity ?? 'error'
    let ok: boolean
    let actual: string
    if (severity === 'none') {
      const errs = diagnostics.filter((d) => d.severity === 'error')
      ok = errs.length === 0
      actual = ok ? 'compiles cleanly' : errs.map((d) => `${d.line}: ${d.message}`).join('\n')
    } else {
      const re = new RegExp(t.pattern ?? '.', 'i')
      const hit = diagnostics.find((d) => d.severity === severity && re.test(d.message))
      ok = Boolean(hit)
      actual = hit
        ? `line ${hit.line}: ${hit.severity}: ${hit.message}`
        : diagnostics.length
          ? diagnostics.map((d) => `line ${d.line}: ${d.severity}: ${d.message}`).join('\n')
          : 'no diagnostics — the code compiles cleanly'
    }
    return {
      index,
      name: t.name ?? `Check ${index + 1}`,
      hidden: Boolean(t.hidden),
      status: ok ? 'passed' : 'wrong',
      expected: severity === 'none' ? 'no errors' : `${severity} matching /${t.pattern}/`,
      actual
    }
  })
  const passed = results.filter((r) => r.status === 'passed').length
  return {
    verdict: verdictFrom(results), diagnostics, compilerOutput: output, tests: results,
    passed, total: results.length, compileMs: ms
  }
}

async function judgePredict(p: Problem, prediction: string, tests: TestCase[]): Promise<JudgeResult> {
  const [expected] = await referenceOutputs(p, tests.length ? tests : [{}])
  const compare = defaultCompare(p)
  const ok = compareText(prediction, expected, compare)
  const results: TestResult[] = [{
    index: 0, name: 'Program output', hidden: false, status: ok ? 'passed' : 'wrong',
    expected, actual: prediction
  }]
  return {
    verdict: ok ? 'accepted' : 'wrong_answer', diagnostics: [], compilerOutput: '', tests: results,
    passed: ok ? 1 : 0, total: 1, compileMs: 0
  }
}

/**
 * Judge `code` against a problem. `submit` includes hidden tests (like LeetCode's Submit);
 * otherwise only visible tests run (Run).
 */
export async function judge(p: Problem, code: string, submit: boolean): Promise<JudgeResult> {
  const tests = submit ? p.tests : p.tests.filter((t) => !t.hidden)
  if (p.meta.platforms && !(p.meta.platforms as string[]).includes(process.platform)) {
    return failure('internal_error', `This problem uses Apple frameworks (such as SwiftUI, Combine or SwiftData) that only exist on macOS, so it can't be judged on ${process.platform}. Read the Learn tab and try it on a Mac.`)
  }
  try {
    if (p.meta.mode === 'diagnostic') return await judgeDiagnostic(p, code, tests)
    if (p.meta.mode === 'predict') return await judgePredict(p, code, tests)

    const needRef = tests.some((t) => t.expected === undefined)
    const [built, ref] = await Promise.all([
      build(p, code),
      needRef ? referenceOutputs(p, tests) : Promise.resolve(undefined)
    ])
    if (!built.ok) {
      return failure('compile_error', 'Compilation failed', {
        diagnostics: built.diagnostics, compilerOutput: built.output, compileMs: built.ms, total: tests.length
      })
    }
    const outs = await runCases(p, built.binary, tests)
    const compare = defaultCompare(p)
    const results: TestResult[] = tests.map((t, index) => {
      const o = outs[index]
      const expected = t.expected !== undefined ? t.expected : ref![index]
      let status: TestStatus
      if (o.status !== 'ok') status = o.status
      else if (p.meta.mode === 'function') status = compareJson(o.output, expected, compare) ? 'passed' : 'wrong'
      else status = compareText(o.output, String(expected), compare) ? 'passed' : 'wrong'
      return {
        index,
        name: t.name ?? `Case ${index + 1}`,
        hidden: Boolean(t.hidden),
        status,
        input: showInput(p, t),
        expected: showExpected(p, expected),
        actual: o.status === 'ok' ? o.output : undefined,
        stdout: p.meta.mode === 'function' ? o.stdout : undefined,
        stderr: o.stderr || undefined,
        timeMs: Math.round(o.ms * 100) / 100
      }
    })
    const passed = results.filter((r) => r.status === 'passed').length
    return {
      verdict: verdictFrom(results),
      diagnostics: built.diagnostics,
      compilerOutput: built.output,
      tests: results,
      passed,
      total: results.length,
      compileMs: built.ms
    }
  } catch (e) {
    return failure('internal_error', e instanceof Error ? e.message : String(e))
  }
}
