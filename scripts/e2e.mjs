/**
 * End-to-end test of the built app (run `npm run build` first, or use `npm run e2e`).
 *
 * Drives the real Electron window with Playwright in a throwaway profile:
 *   1. For every problem: submit the starter (must NOT be accepted), then the reference
 *      solution (must be Accepted). Predict problems use the snippet's real output.
 *   2. Scenario checks: Run vs Submit, compile-error markers, time limit, views, plug-in reload.
 *
 *   npm run e2e                 # everything
 *   npm run e2e -- closure      # only problems whose id contains "closure"
 * Screenshots of failures land in .e2e/.
 */
import { _electron as electron } from 'playwright-core'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const APP = path.resolve(import.meta.dirname, '..')
const OUT = path.join(APP, '.e2e')
const filter = process.argv[2]
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'swift-judge-e2e-'))
fs.rmSync(OUT, { recursive: true, force: true })
fs.mkdirSync(OUT, { recursive: true })

// ---- problem bank from disk
const problems = []
for (const track of ['beginner', 'intermediate', 'advanced']) {
  for (const d of fs.readdirSync(path.join(APP, 'problems', track)).sort()) {
    const dir = path.join(APP, 'problems', track, d)
    const meta = JSON.parse(fs.readFileSync(path.join(dir, 'problem.json'), 'utf8'))
    if (!filter || meta.id.includes(filter)) problems.push({ dir, meta })
  }
}
if (problems.length === 0) {
  console.error(`no problems match "${filter}"`)
  process.exit(1)
}
const read = (dir, f) => (fs.existsSync(path.join(dir, f)) ? fs.readFileSync(path.join(dir, f), 'utf8') : '')

/** Real output of a predict snippet, computed independently of the app. */
function snippetOutput(dir) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'swj-e2e-snip-'))
  try {
    fs.copyFileSync(path.join(dir, 'snippet.swift'), path.join(tmp, 'main.swift'))
    const sdk = execFileSync('xcrun', ['--sdk', 'macosx', '--show-sdk-path'], { encoding: 'utf8' }).trim()
    execFileSync('xcrun', ['swiftc', '-sdk', sdk, '-swift-version', '6', 'main.swift', '-o', 'prog'], { cwd: tmp, stdio: 'pipe' })
    return execFileSync(path.join(tmp, 'prog'), { encoding: 'utf8' })
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
}

// ---- launch
const app = await electron.launch({
  executablePath: path.join(APP, 'node_modules/electron/dist/Electron.app/Contents/MacOS/Electron'),
  args: [APP],
  cwd: APP,
  timeout: 30_000,
  env: { ...process.env, SWIFT_JUDGE_USER_DATA: profile }
})
const page = await app.firstWindow()
const pageErrors = []
page.on('pageerror', (e) => pageErrors.push(e.message))
page.on('console', (m) => m.type() === 'error' && pageErrors.push(m.text()))
await page.waitForSelector('.problem-item', { timeout: 30_000 })

const failures = []
const fail = async (what, detail) => {
  failures.push(`${what}: ${detail}`)
  await page.screenshot({ path: path.join(OUT, `${failures.length}-${what.replace(/[^\w-]+/g, '_')}.png`) })
}

async function openProblem(id) {
  await page.click('.tabs button:has-text("Problems")')
  const item = page.locator(`.problem-item[data-id="${id}"]`)
  await item.scrollIntoViewIfNeeded()
  await item.click()
  await page.waitForFunction(
    (t) => document.querySelector('.problem-title')?.textContent === t && window.monaco?.editor.getEditors().length > 0,
    problems.find((p) => p.meta.id === id)?.meta.title ?? id,
    { timeout: 15_000 }
  )
}

async function setCode(code) {
  await page.evaluate((c) => window.monaco.editor.getEditors()[0].getModel().setValue(c), code)
}

async function verdict(button = 'button.submit') {
  await page.click(button)
  await page.waitForSelector(`${button}:disabled`, { timeout: 3000 }).catch(() => {})
  await page.waitForFunction(
    (b) => !document.querySelector(b).disabled && document.querySelector('.verdict') && !document.querySelector('.verdict.pending'),
    button,
    { timeout: 120_000 }
  )
  return (await page.textContent('.verdict > span')).trim()
}

// ---- 1. every problem: starter rejected, reference accepted
const t0 = Date.now()
let n = 0
for (const { dir, meta } of problems) {
  n++
  try {
    await openProblem(meta.id)
    const isPredict = meta.mode === 'predict'
    await setCode(isPredict ? '' : read(dir, 'starter.swift'))
    const starterVerdict = await verdict()
    if (starterVerdict === 'Accepted') await fail(meta.id, 'starter was accepted')
    await setCode(isPredict ? snippetOutput(dir) : read(dir, 'solution.swift'))
    const solutionVerdict = await verdict()
    if (solutionVerdict !== 'Accepted') await fail(meta.id, `reference got "${solutionVerdict}"`)
    process.stdout.write(solutionVerdict === 'Accepted' && starterVerdict !== 'Accepted' ? '.' : 'x')
  } catch (e) {
    await fail(meta.id, String(e).split('\n')[0])
    process.stdout.write('E')
  }
  if (n % 50 === 0) process.stdout.write(` ${n}\n`)
}
const perProblemSeconds = ((Date.now() - t0) / 1000).toFixed(0)
console.log(`\n${problems.length} problems driven through the UI in ${perProblemSeconds}s`)

// ---- 2. scenarios (only on a full run)
if (!filter) {
  const check = async (name, ok, detail = '') => {
    if (!ok) await fail(name, detail)
    console.log(`${ok ? '✓' : '✗'} ${name}${detail && !ok ? ` — ${detail}` : ''}`)
  }

  await openProblem('two-sum')
  await setCode('func twoSum(_ nums: [Int], target: Int) -> [Int] { [0, 1] }')
  const runV = await verdict('button.run')
  const runCount = (await page.textContent('.verdict .count')).trim()
  await check('Run judges visible tests only', runV === 'Wrong Answer' && runCount.includes('(visible only)'), `${runV} ${runCount}`)
  const actualShown = await page.locator('.field pre.bad').first().textContent().catch(() => '')
  await check('wrong answer shows your output', actualShown === '[0,1]', actualShown)

  await setCode('func twoSum(_ nums: [Int], target: Int) -> [Int] {\n    let x: Int = "oops"\n    return []\n}')
  const ce = await verdict('button.run')
  await page.waitForTimeout(300)
  const markers = await page.evaluate(() => window.monaco.editor.getModelMarkers({}).map((m) => m.startLineNumber))
  await check('compile error is reported with an editor marker on line 2', ce === 'Compile Error' && markers.includes(2), `${ce} ${markers}`)

  await openProblem('fix-infinite-while')
  // Pass 1 solved it, so the editor reopened the saved draft; load the buggy starter again.
  const loopDir = problems.find((p) => p.meta.id === 'fix-infinite-while').dir
  await setCode(read(loopDir, 'starter.swift'))
  const started = Date.now()
  const tle = await verdict()
  const skipped = await page.locator('.case.skipped').count()
  await check('infinite loop → Time Limit Exceeded, rest skipped, under 10s', tle === 'Time Limit Exceeded' && skipped > 0 && Date.now() - started < 10_000, `${tle}, ${skipped} skipped, ${Date.now() - started}ms`)

  await openProblem('two-sum')
  await page.click('.pane-tabs button:has-text("Learn")')
  await check('Learn tab shows notes and book link', (await page.locator('.learn .doc-link').count()) > 0 && (await page.textContent('.learn')).includes('From your notes'))
  await page.click('.pane-tabs button:has-text("Solution")')
  await check('Solution unlocked after Accepted', (await page.locator('.locked').count()) === 0)

  const solvedText = (await page.textContent('.solved-count')).trim()
  await check('solved counter reflects every accepted problem', solvedText === `${problems.length}/${problems.length} solved`, solvedText)

  await page.click('.tabs button:has-text("Concepts")')
  await page.waitForSelector('.concept-card')
  await check('Concepts view lists every concept', (await page.locator('.concept-card').count()) >= 150)
  await page.click('.tabs button:has-text("Quiz")')
  await page.waitForSelector('.quiz-card')
  await page.locator('.quiz-card').first().locator('.choice').first().click()
  await check('Quiz reveals the explanation after answering', (await page.locator('.quiz-card .explain').count()) === 1)
  await page.click('.tabs button:has-text("Swift Book")')
  await page.locator('.book-toc .problem-item', { hasText: 'Closures' }).first().click()
  await page.waitForTimeout(500)
  await check('Swift Book renders code blocks', (await page.locator('.book-body pre.code').count()) > 5)

  await page.click('.tabs button:has-text("Problems")')
  const before = await page.locator('.problem-item').count()
  execFileSync('npx', ['tsx', 'scripts/new-problem.ts', 'advanced', 'e2e-plugin-check', 'function'], { cwd: APP, stdio: 'pipe' })
  try {
    await page.waitForFunction((b) => document.querySelectorAll('.problem-item').length === b + 1, before, { timeout: 10_000 })
    await check('new problem folder appears without restarting', true)
  } catch {
    await check('new problem folder appears without restarting', false, `still ${await page.locator('.problem-item').count()}`)
  } finally {
    const adv = path.join(APP, 'problems', 'advanced')
    for (const d of fs.readdirSync(adv).filter((d) => d.endsWith('-e2e-plugin-check'))) fs.rmSync(path.join(adv, d), { recursive: true })
  }
}

await app.close()
fs.rmSync(profile, { recursive: true, force: true })
if (pageErrors.length) failures.push(...pageErrors.map((e) => `page error: ${e}`))
console.log(failures.length ? `\n${failures.length} failure(s):\n  ${failures.join('\n  ')}` : '\nall e2e checks passed')
process.exit(failures.length ? 1 : 0)
