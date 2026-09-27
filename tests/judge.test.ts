import { mkdtempSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { beforeAll, describe, expect, it } from 'vitest'
import { loadAll } from '../src/main/content/loader'
import { compareJson, compareText } from '../src/main/judge/compare'
import { parseDiagnostics, stripPaths } from '../src/main/judge/diagnostics'
import { generateDriver, parseDriverOutput } from '../src/main/judge/harness'
import { judge } from '../src/main/judge/judge'
import { setCacheRoot } from '../src/main/judge/toolchain'
import type { Problem } from '../src/shared/types'

const root = join(__dirname, '..', 'problems')
const bank = loadAll(root)
const load = (id: string): Problem => {
  const p = bank.problems.get(id)
  if (!p) throw new Error(`no problem ${id}`)
  return p
}

beforeAll(() => setCacheRoot(mkdtempSync(join(tmpdir(), 'swj-test-cache-'))))

describe('compare', () => {
  it('json deep-equal ignores key order and whitespace', () => {
    expect(compareJson('{"b":1,"a":[1,2]}', { a: [1, 2], b: 1 })).toBe(true)
    expect(compareJson('[1,2]', [2, 1])).toBe(false)
  })
  it('json-unordered sorts top-level arrays only', () => {
    expect(compareJson('[[2,1],[3]]', [[3], [2, 1]], 'json-unordered')).toBe(true)
    expect(compareJson('[[1,2],[3]]', [[3], [2, 1]], 'json-unordered')).toBe(false)
    expect(compareJson('[[1,2],[3]]', [[3], [2, 1]], 'json-unordered-deep')).toBe(true)
  })
  it('float tolerance', () => {
    expect(compareJson('0.30000000000000004', 0.3, 'float:1e-9')).toBe(true)
    expect(compareText('x 1.0000001\n', 'x 1.0', 'float:1e-6')).toBe(true)
  })
  it('trimmed text ignores trailing whitespace and final newlines', () => {
    expect(compareText('a  \nb\n\n', 'a\nb')).toBe(true)
    expect(compareText('a\nb', 'b\na')).toBe(false)
    expect(compareText('a\nb', 'b\na', 'unorderedLines')).toBe(true)
  })
})

describe('diagnostics + harness', () => {
  it('parses llvm-style diagnostics', () => {
    const d = parseDiagnostics('/tmp/x/user.swift:3:5: error: cannot find \'y\' in scope\n  y = 1\n  ^')
    expect(d).toEqual([{ file: 'user.swift', line: 3, column: 5, severity: 'error', message: "cannot find 'y' in scope" }])
  })
  it('handles Windows-style paths (drive letters, backslashes, spaces)', () => {
    const out = 'C:\\Users\\Ann Lee\\AppData\\Local\\Temp\\swj-1\\user.swift:4:9: error: cannot find \'x\' in scope'
    expect(parseDiagnostics(out)).toEqual([{ file: 'user.swift', line: 4, column: 9, severity: 'error', message: "cannot find 'x' in scope" }])
    expect(stripPaths(out)).toBe("user.swift:4:9: error: cannot find 'x' in scope")
    expect(stripPaths('/private/var/folders/x y/swj-2/main.swift:1:1: warning: w')).toBe('main.swift:1:1: warning: w')
  })
  it('generates labels, inout and throws correctly', () => {
    const src = generateDriver({
      name: 'f', returns: 'Void', throws: true,
      params: [{ label: '_', name: 'a', type: '[Int]', inout: true }, { name: 'k', type: 'Int' }]
    })
    expect(src).toContain('try f(&__p_a, k: __i.k)')
    expect(src).toContain('return __p_a')
  })
  it('splits per-case stdout', () => {
    const out = 'hi\n\u001FJUDGE\u001F0\u001F0.1\u001F[1]\n\u001FJUDGE\u001F1\u001F0.2\u001F2\ncrash'
    const r = parseDriverOutput(out)
    expect(r.cases.map((c) => [c.stdout, c.json])).toEqual([['hi\n', '[1]'], ['', '2']])
    expect(r.trailing).toBe('crash')
  })
})

describe('judge (runs swiftc)', { timeout: 120_000 }, () => {
  it('function mode: reference solution is accepted, including derived expectations', async () => {
    const p = load('two-sum')
    const r = await judge(p, p.solution, true)
    expect(r.message).toBeUndefined()
    expect(r.verdict).toBe('accepted')
    expect(r.total).toBe(p.tests.length)
  })
  it('function mode: Run skips hidden tests', async () => {
    const p = load('two-sum')
    expect((await judge(p, p.solution, false)).total).toBe(p.tests.filter((t) => !t.hidden).length)
  })
  it('function mode: wrong answer shows expected vs actual', async () => {
    const p = load('two-sum')
    const r = await judge(p, 'func twoSum(_ nums: [Int], target: Int) -> [Int] { [0, 1] }', true)
    expect(r.verdict).toBe('wrong_answer')
    const bad = r.tests.find((t) => t.status === 'wrong')!
    expect(bad.actual).toBe('[0,1]')
  })
  it('function mode: compile errors map to user lines', async () => {
    const p = load('two-sum')
    const r = await judge(p, 'func twoSum(_ nums: [Int], target: Int) -> [Int] {\n  return undefinedThing\n}', true)
    expect(r.verdict).toBe('compile_error')
    expect(r.diagnostics.some((d) => d.file === 'user.swift' && d.line === 2)).toBe(true)
  })
  it('function mode: a crash is isolated to its case, later cases still run', async () => {
    const p = load('two-sum')
    const code = 'func twoSum(_ nums: [Int], target: Int) -> [Int] {\n  if nums.count == 2 && nums[0] == 3 { return [nums[5]] }\n  return nums.isEmpty ? [] : [0, 1]\n}'
    const r = await judge(p, code, true)
    expect(r.tests[1].status).toBe('runtime_error')
    expect(r.tests[1].stderr).toMatch(/Index out of range/)
    expect(r.tests[2].status).not.toBe('runtime_error')
    expect(r.tests.length).toBe(p.tests.length)
    expect(r.tests.slice(3).some((t) => t.status === 'passed')).toBe(true)
  })
  it('function mode: infinite loop times out without waiting for the whole batch', async () => {
    const p = { ...load('two-sum') }
    p.meta = { ...p.meta, timeLimitMs: 500 }
    const code = 'func twoSum(_ nums: [Int], target: Int) -> [Int] {\n  var i = 0\n  while nums.count > 1 { i &+= 1 }\n  return nums.isEmpty ? [] : [i]\n}'
    const t0 = Date.now()
    const r = await judge(p, code, true)
    expect(r.verdict).toBe('timeout')
    expect(r.tests[0].status).toBe('timeout') // [2,7,11,15] loops forever
    expect(r.tests.slice(1).every((t) => t.status === 'skipped')).toBe(true) // stop at first TLE
    expect(Date.now() - t0).toBeLessThan(8_000)
  })
  it('stdio mode: accepted and wrong answer', async () => {
    const p = load('fizzbuzz-stdio')
    expect((await judge(p, p.solution, true)).verdict).toBe('accepted')
    const r = await judge(p, 'let n = Int(readLine()!)!\nfor i in 1...max(n,1) { print(i) }', true)
    expect(r.verdict).not.toBe('accepted')
  })
  it('stdio mode: compile errors and crashes point at the learner\'s own lines', async () => {
    const p = load('fizzbuzz-stdio')
    const ce = await judge(p, 'let n = 1\nlet x: Int = "oops"\nprint(n)', true)
    expect(ce.verdict).toBe('compile_error')
    expect(ce.diagnostics.map((d) => [d.file, d.line])).toContainEqual(['main.swift', 2])
    const crash = await judge(p, 'let xs: [Int] = []\nlet n = Int(readLine()!)!\nprint(xs[n])', true)
    expect(crash.verdict).toBe('runtime_error')
    const bad = crash.tests.find((t) => t.status === 'runtime_error')!
    expect(bad.stderr).toMatch(/Index out of range/)
    const nilCrash = await judge(p, 'let s: String? = nil\n\nprint(s!)', true)
    expect(nilCrash.tests[0].stderr).toMatch(/main\.swift:3: Fatal error: Unexpectedly found nil/)
  })
  it('crashes exit quietly with 128 + signal, and are still reported as crashes', async () => {
    const p = load('two-sum')
    const r = await judge(p, 'func f(_ n: Int) -> Int { f(n + 1) + 1 }\nfunc twoSum(_ nums: [Int], target: Int) -> [Int] { [f(0)] }', true)
    expect(r.tests[0].status).toBe('runtime_error')
    if (process.platform === 'darwin') expect(r.tests[0].stderr).toMatch(/SIGSEGV|stack overflow/)
  })
  it('diagnostic mode: passes only when the expected error appears', async () => {
    const p = load('diag-private-access')
    expect((await judge(p, p.solution, true)).verdict).toBe('accepted')
    expect((await judge(p, p.starter, true)).verdict).toBe('wrong_answer')
  })
  it('driver names cannot be shadowed by user types', async () => {
    const p = load('two-sum')
    const code = 'struct FileHandle {}\nstruct Data {}\nstruct JSONEncoder {}\nfunc print(_ x: Any) {}\n' + p.solution
    expect((await judge(p, code, true)).verdict).toBe('accepted')
  })
  it('predict mode: compares prediction against real program output', async () => {
    const p = load('predict-array-copy')
    expect((await judge(p, '3 4\n["a", "b", "c"]', true)).verdict).toBe('accepted')
    expect((await judge(p, '4 4\n["a", "b", "c", "d"]', true)).verdict).toBe('wrong_answer')
  })
})
