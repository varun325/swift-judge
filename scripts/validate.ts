/**
 * Validates every problem folder (or those matching a filter):
 *   - schema (problem.json, tests.json)
 *   - reference solution compiles and passes every test; explicit `expected`
 *     values agree with what the reference actually produces
 *   - starter compiles (or deliberately fails when starterFails / diagnostic mode)
 *   - concepts referenced exist in content/concepts.json
 *
 *   npm run validate                 # everything
 *   npm run validate -- closures     # ids/paths containing "closures"
 */
import { existsSync, mkdirSync, readFileSync } from 'node:fs'
import { join, relative } from 'node:path'
import { loadAll } from '../src/main/content/loader'
import { judge } from '../src/main/judge/judge'
import { mapLimit } from '../src/main/judge/runner'
import { setCacheRoot } from '../src/main/judge/toolchain'
import type { Concept, Problem } from '../src/shared/types'

const root = join(import.meta.dirname, '..')
const filter = process.argv[2]
setCacheRoot(join(root, '.cache'))
mkdirSync(join(root, '.cache'), { recursive: true })

const { problems, errors } = loadAll(join(root, 'problems'))
const conceptsFile = join(root, 'content', 'concepts.json')
const conceptIds = new Set(
  existsSync(conceptsFile) ? (JSON.parse(readFileSync(conceptsFile, 'utf8')) as Concept[]).map((c) => c.id) : []
)

async function check(p: Problem): Promise<string[]> {
  const issues: string[] = []
  const { mode } = p.meta
  if (p.tests.length === 0) issues.push('no tests')
  if (p.meta.hints.length !== 3) issues.push(`expected 3 hints, found ${p.meta.hints.length}`)
  if (mode === 'function' && !p.meta.signature && !p.harness) issues.push('function mode needs signature or harness.swift')
  if (mode === 'diagnostic' && p.tests.some((t) => t.severity !== 'none' && !t.pattern)) issues.push('diagnostic test without pattern')
  for (const c of p.meta.concepts) if (conceptIds.size && !conceptIds.has(c)) issues.push(`unknown concept "${c}"`)

  const ref = await judge(p, mode === 'predict' ? '' : p.solution, true)
  if (mode === 'predict') {
    if (ref.verdict === 'internal_error') issues.push(`snippet failed: ${ref.message}`)
  } else if (ref.verdict !== 'accepted') {
    const bad = ref.tests.find((t) => t.status !== 'passed')
    issues.push(
      `reference solution: ${ref.verdict}` +
        (ref.message ? `\n${ref.message}` : '') +
        (ref.compilerOutput && ref.verdict === 'compile_error' ? `\n${ref.compilerOutput}` : '') +
        (bad ? `\n  ${bad.name}: input=${bad.input} expected=${bad.expected} got=${bad.actual ?? ''} ${bad.stderr ?? ''}` : '')
    )
  }

  if (mode !== 'predict') {
    const starter = await judge(p, p.starter, true)
    if (starter.verdict === 'accepted') issues.push('starter code already passes every test')
    if (starter.verdict === 'internal_error') issues.push(`starter: ${starter.message}`)
    const shouldFail = p.meta.starterFails || mode === 'diagnostic'
    if (!shouldFail && starter.verdict === 'compile_error') issues.push(`starter does not compile:\n${starter.compilerOutput}`)
  }
  return issues
}

const list = [...problems.values()].filter((p) => !filter || p.meta.id.includes(filter) || p.dir.includes(filter))
const t0 = Date.now()
let tests = 0
const results = await mapLimit(list, 6, async (p) => {
  const issues = await check(p)
  tests += p.tests.length
  process.stdout.write(issues.length ? '✗' : '.')
  return { p, issues }
})
console.log('\n')

const failed = results.filter((r) => r.issues.length)
for (const { p, issues } of failed) {
  console.log(`✗ ${relative(root, p.dir)} (${p.meta.id})`)
  for (const i of issues) console.log('   ' + i.replace(/\n/g, '\n   '))
}
for (const e of errors) console.log(`✗ load: ${e}`)

const byTrack = new Map<string, number>()
const byMode = new Map<string, number>()
for (const p of list) {
  byTrack.set(p.meta.track, (byTrack.get(p.meta.track) ?? 0) + 1)
  byMode.set(p.meta.mode, (byMode.get(p.meta.mode) ?? 0) + 1)
}
console.log(`${list.length - failed.length}/${list.length} problems OK · ${tests} test cases · ${((Date.now() - t0) / 1000).toFixed(1)}s`)
console.log('by track:', Object.fromEntries(byTrack), ' by mode:', Object.fromEntries(byMode))
if (failed.length || errors.length) process.exit(1)
