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
 *   npm run e2e -- --scenarios  # skip the per-problem pass, run only the UI scenarios
 * Screenshots of failures land in .e2e/.
 */
import { _electron as electron } from 'playwright-core'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const APP = path.resolve(import.meta.dirname, '..')
const OUT = path.join(APP, '.e2e')
const scenariosOnly = process.argv.includes('--scenarios')
const filter = process.argv.slice(2).find((a) => !a.startsWith('--'))
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'swift-judge-e2e-'))
const playgroundDir = path.join(profile, 'playground')
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
    execFileSync('xcrun', ['swiftc', '-sdk', sdk, '-swift-version', '6', '-module-name', 'Solution', 'main.swift', '-o', 'prog'], { cwd: tmp, stdio: 'pipe' })
    return execFileSync(path.join(tmp, 'prog'), { encoding: 'utf8' })
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
}

// ---- seed a profile with spaced-repetition state: two-sum's revisit is 3 days overdue, and
// leap-year was solved before reviews existed (no schedule yet, so it must be backfilled).
const localDay = (offset) => {
  const d = new Date()
  d.setDate(d.getDate() + offset)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
fs.writeFileSync(
  path.join(profile, 'progress.json'),
  JSON.stringify({
    problems: {
      'two-sum': { solved: true, attempts: 3, review: { step: 2, due: localDay(-3), last: localDay(-5), reviews: 2 } },
      'leap-year': { solved: true, attempts: 1, solvedAt: new Date(Date.now() - 10 * 86_400_000).toISOString() }
    },
    quiz: {}
  })
)

// ---- launch
const app = await electron.launch({
  executablePath: path.join(APP, 'node_modules/electron/dist/Electron.app/Contents/MacOS/Electron'),
  args: [APP],
  cwd: APP,
  timeout: 30_000,
  // No cloud in UI tests: point the Firebase config at nothing so the app runs offline-only.
  env: { ...process.env, SWIFT_JUDGE_USER_DATA: profile, SWIFT_JUDGE_PLAYGROUND: playgroundDir, SWIFT_JUDGE_FIREBASE_CONFIG: '/nonexistent' }
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

// ---- 0. Fibonacci review queue greets the learner on launch
{
  const ok = (name, cond, detail = '') => {
    if (!cond) failures.push(`${name}: ${detail}`)
    console.log(`${cond ? '✓' : '✗'} ${name}${detail && !cond ? ` — ${detail}` : ''}`)
  }
  await page.waitForSelector('.review-today', { timeout: 10_000 }).catch(() => {})
  await page.screenshot({ path: path.join(OUT, 'review-dialog.png') })
  const dueIds = await page.locator('.review-today li button').evaluateAll((els) => els.map((e) => e.dataset.id))
  const overdueText = (await page.locator('.review-today li button[data-id="two-sum"] .when').textContent().catch(() => '')) ?? ''
  ok('revisit dialog opens on launch with due + backfilled problems', dueIds[0] === 'leap-year' && dueIds.includes('two-sum') && overdueText.includes('3d overdue'),
    `${dueIds} / ${overdueText}`)
  await page.click('.review-today li button[data-id="two-sum"]')
  await page.waitForFunction(() => document.querySelector('.problem-title')?.textContent?.startsWith('Two Sum') && window.monaco?.editor.getEditors().length > 0)
  await page.screenshot({ path: path.join(OUT, 'review-banner.png') })
  ok('opening a due problem shows the revisit banner', (await page.locator('.review-banner').count()) === 1)
  await page.click('.review-banner button')
  const twoSumDir = path.join(APP, 'problems', 'beginner', fs.readdirSync(path.join(APP, 'problems', 'beginner')).find((d) => d.endsWith('-two-sum')))
  await page.waitForFunction((s) => window.monaco.editor.getEditors()[0].getModel().getValue() === s, read(twoSumDir, 'starter.swift'))
  await setCode(read(twoSumDir, 'solution.swift'))
  const v = await verdict()
  await page.waitForSelector('.review-next', { timeout: 5000 }).catch(() => {})
  const nextText = (await page.textContent('.review-next').catch(() => '')) ?? ''
  const button = (await page.textContent('.review-button')).trim()
  ok('an on-time re-solve climbs the ladder (step 2 → next visit in 3 days)',
    v === 'Accepted' && (await page.locator('.review-banner').count()) === 0 && nextText.includes(localDay(3)) && button === '↻ 1 to revisit',
    `${v} / ${nextText} / ${button}`)
  await page.click('.review-button')
  await page.waitForSelector('.review-today')
  ok('revisit dialog reopens from the top bar with what is left', (await page.locator('.review-today li button').count()) === 1)
  await page.click('.review-today .close')
}

// ---- 1. every problem: starter rejected, reference accepted
const t0 = Date.now()
let n = 0
for (const { dir, meta } of scenariosOnly ? [] : problems) {
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
if (!scenariosOnly) console.log(`\n${problems.length} problems driven through the UI in ${perProblemSeconds}s`)

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

  // Hints: three per problem, unlocked strictly in order, remembered across visits.
  await openProblem('leap-year')
  const locked = await page.locator('.locked-hint').count()
  const secondDisabled = await page.locator('.locked-hint[data-level="2"]').isDisabled()
  await page.click('.locked-hint[data-level="1"]')
  await page.waitForSelector('.hint.open[data-level="1"]')
  const secondEnabled = await page.locator('.locked-hint[data-level="2"]').isEnabled()
  await page.click('.locked-hint[data-level="2"]')
  await page.waitForSelector('.hint.open[data-level="2"]')
  await openProblem('two-sum')
  await openProblem('leap-year')
  const reopened = await page.locator('.hint.open').count()
  const usedLabel = (await page.textContent('.hints .label')).trim()
  await check('hints unlock in order and persist', locked === 3 && secondDisabled && secondEnabled && reopened === 2 && usedLabel.includes('2/3'),
    `locked=${locked} secondDisabled=${secondDisabled} secondEnabled=${secondEnabled} reopened=${reopened} label=${usedLabel}`)

  await openProblem('two-sum')
  await page.click('.pane-tabs button:has-text("Learn")')
  await check('Learn tab shows notes and book link', (await page.locator('.learn .doc-link').count()) > 0 && (await page.textContent('.learn')).includes('From your notes'))
  await page.click('.pane-tabs button:has-text("Solution")')
  if (!scenariosOnly) await check('Solution unlocked after Accepted', (await page.locator('.locked').count()) === 0)

  const solvedText = (await page.textContent('.solved-count')).trim()
  if (!scenariosOnly) await check('solved counter reflects every accepted problem', solvedText.startsWith(`${problems.length}/`), solvedText)

  // Learning content: every problem in every track shows its JS comparison and Confusion Compass.
  {
    const all = []
    for (const track of fs.readdirSync(path.join(APP, 'problems'))) {
      const dir = path.join(APP, 'problems', track)
      if (!fs.statSync(dir).isDirectory()) continue
      for (const d of fs.readdirSync(dir)) {
        const f = path.join(dir, d, 'problem.json')
        if (fs.existsSync(f)) all.push(JSON.parse(fs.readFileSync(f, 'utf8')))
      }
    }
    const missing = []
    for (const meta of all) {
      await page.click('.tabs button:has-text("Problems")')
      const item = page.locator(`.problem-item[data-id="${meta.id}"]`)
      await item.scrollIntoViewIfNeeded()
      await item.click()
      await page.waitForFunction((t) => document.querySelector('.problem-title')?.textContent === t, meta.title, { timeout: 15_000 })
      const shown = await page.evaluate(() => ({
        js: document.querySelector('.js-bridge .markdown')?.textContent?.trim().length ?? 0,
        jsClosed: document.querySelector('.js-bridge')?.open === false, // closed by default: it can act as a hint
        compass: document.querySelectorAll('.compass li').length,
        jsQuestion: document.querySelectorAll('.compass li[data-kind="js"]').length,
        impact: document.querySelectorAll('.badge.impact-core, .badge.impact-edge').length
      }))
      if (!shown.js || !shown.jsClosed || shown.compass !== meta.compass.length || !shown.jsQuestion || shown.impact !== 1) missing.push(`${meta.id} ${JSON.stringify(shown)}`)
    }
    await check(`all ${all.length} problems render a (closed) JS comparison, 80/20 badge and Confusion Compass`, missing.length === 0, missing.slice(0, 5).join('; '))
  }

  // Confusion Compass → "Answer in Playground" opens a notes page pre-filled with the questions.
  {
    await openProblem('two-sum')
    const firstQuestion = (await page.locator('.compass li .markdown').first().textContent()).trim().slice(0, 40)
    await page.click('.compass-answer')
    await page.waitForFunction(
      (q) => window.monaco?.editor.getEditors().some((e) => e.getModel()?.getLanguageId() === 'markdown' && e.getModel().getValue().includes(q)),
      firstQuestion.slice(0, 25),
      { timeout: 15_000 }
    )
    const notesFile = path.join(playgroundDir, 'compass-two-sum.md')
    const onDisk = fs.existsSync(notesFile) ? fs.readFileSync(notesFile, 'utf8') : ''
    // Write an answer, come back through the problem: the page must reopen with the answer intact.
    await page.evaluate(() => {
      const md = window.monaco.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === 'markdown')
      md.getModel().setValue(md.getModel().getValue() + '\nMY-ANSWER-MARKER\n')
    })
    await page.waitForTimeout(1200)
    await openProblem('two-sum')
    await page.click('.compass-answer')
    await page.waitForTimeout(800)
    const kept = fs.existsSync(notesFile) && fs.readFileSync(notesFile, 'utf8').includes('MY-ANSWER-MARKER')
    const pages = fs.readdirSync(playgroundDir).filter((f) => f.startsWith('compass-two-sum')).length
    await check('Answer in Playground opens a pre-filled notes page and never overwrites answers',
      onDisk.includes('Confusion Compass: Two Sum') && onDisk.includes('My answer') && kept && pages === 2,
      `onDisk=${onDisk.length} kept=${kept} files=${pages}`)
  }


  await page.click(".tabs button:has-text(\"Problems\")") // the compass check left the Playground open on its page
  await page.evaluate(() => localStorage.setItem("playground.page", "scratchpad"))
  await page.click('.tabs button:has-text("Playground")')
  // Wait until the scratchpad page has loaded into the editor before replacing its text.
  await page.waitForFunction(
    () => window.monaco?.editor.getEditors().some((e) => e.getModel()?.getLanguageId() === 'swift' && e.getModel().getValue().includes('Scratch space')),
    null,
    { timeout: 15_000 }
  )
  const pgCode = 'let xs = [3, 1, 2]\nprint(xs.sorted())\nprint(readLine() ?? "none")'
  await page.evaluate((c) => window.monaco.editor.getEditors().find((e) => e.getModel().getLanguageId() === 'swift').getModel().setValue(c), pgCode)
  await page.click('button:has-text("stdin")')
  await page.fill('.pg-stdin', 'hello from stdin')
  await page.click('button.pg-run')
  await page.waitForSelector('.pg-stdout', { timeout: 60_000 })
  const pgOut = (await page.textContent('.pg-stdout')).trim()
  await check('playground runs code with stdin', pgOut === '[1, 2, 3]\nhello from stdin', JSON.stringify(pgOut))
  await page.click('.pg-append')
  await page.waitForTimeout(1200)
  const pgNotes = fs.readFileSync(path.join(playgroundDir, 'scratchpad.md'), 'utf8')
  const pgSwift = fs.readFileSync(path.join(playgroundDir, 'scratchpad.swift'), 'utf8')
  await check('playground saves code and appended run to files', pgSwift === pgCode && pgNotes.includes('[1, 2, 3]') && pgNotes.includes('```swift'), pgNotes.slice(-120))
  await page.evaluate(() => window.monaco.editor.getEditors().find((e) => e.getModel().getLanguageId() === 'swift').getModel().setValue('let x: Int = "no"'))
  await page.click('button.pg-run')
  await page.waitForSelector('.pg-output .console.error', { timeout: 60_000 })
  await page.waitForTimeout(300)
  const pgMarkers = await page.evaluate(() => window.monaco.editor.getModelMarkers({ owner: 'swiftc' }).length)
  await check('playground shows compile errors inline', pgMarkers > 0)
  await check('playground notes preview renders Markdown live', (await page.locator('.pg-preview-body .markdown pre.code').count()) > 0)
  await page.click('.pg-preview-toggle')
  const minimised = (await page.locator('.pg-preview-body').count()) === 0 && (await page.locator('.pg-notes.preview-collapsed').count()) === 1
  await page.click('.pg-preview-toggle')
  await check('notes preview can be minimised and restored', minimised && (await page.locator('.pg-preview-body').count()) === 1)

  // Regression: a cloud sync notice arriving while you type must not reload the page under you
  // (it used to replace the notes with the last autosaved text, eating keystrokes and moving the cursor).
  {
    // Put the cursor at the very end of the notes (via Monaco, so it's the same on every OS and input mode).
    await page.evaluate(() => {
      const md = window.monaco.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === 'markdown')
      const m = md.getModel()
      md.focus()
      md.setPosition({ lineNumber: m.getLineCount(), column: m.getLineMaxColumn(m.getLineCount()) })
    })
    await page.keyboard.type(' first-burst', { delay: 5 })
    await page.waitForTimeout(900) // autosave (500 ms) has flushed
    await page.keyboard.type(' second-burst', { delay: 5 })
    await app.evaluate(({ BrowserWindow }) => {
      for (const w of BrowserWindow.getAllWindows()) w.webContents.send('cloud:changed', { enabled: true, signedIn: true, state: 'idle', lastSync: Date.now() }, true)
    })
    await page.keyboard.type(' third-burst', { delay: 5 })
    await page.waitForTimeout(1500)
    const text = await page.evaluate(() => window.monaco.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === 'markdown').getModel().getValue())
    const focused = await page.evaluate(() => Boolean(document.activeElement?.closest('.pg-notes-editor')))
    await check('typing in notes survives a cloud sync notice (no reload under the cursor)',
      /first-burst second-burst third-burst\s*$/.test(text) && focused,
      JSON.stringify(text.slice(-80)) + ` focused=${focused} found-anywhere=${text.includes('first-burst second-burst third-burst')}`)
  }

  // + New and Rename use an inline form (Electron has no window.prompt()).
  await page.click('.pg-new')
  await page.fill('.pg-name input', 'Closures Practice')
  await page.press('.pg-name input', 'Enter')
  await page.waitForSelector('.problem-item.selected[data-page="closures-practice"]', { timeout: 10_000 }).catch(() => {})
  const created = fs.existsSync(path.join(playgroundDir, 'closures-practice.md')) && (await page.locator('.pg-name').count()) === 0
  await page.click('.pg-rename')
  await page.fill('.pg-name input', 'scratchpad')
  await page.press('.pg-name input', 'Enter')
  const duplicateError = await page.waitForSelector('.pg-name-error', { timeout: 5000 }).then(() => true).catch(() => false)
  await page.fill('.pg-name input', 'Closures Deep Dive')
  await page.press('.pg-name input', 'Enter')
  await page.waitForSelector('.problem-item.selected[data-page="closures-deep-dive"]', { timeout: 10_000 }).catch(() => {})
  const renamed = fs.existsSync(path.join(playgroundDir, 'closures-deep-dive.md')) && !fs.existsSync(path.join(playgroundDir, 'closures-practice.md'))
  await check('Playground + New and Rename work (inline name form, duplicate names rejected)', created && duplicateError && renamed,
    `created=${created} duplicateError=${duplicateError} renamed=${renamed}`)

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

// ---- 3. closing the window must not break the live problem-folder watcher (macOS keeps the
// app running with no window; a later file change used to throw "Object has been destroyed").
{
  await app.evaluate(() => {
    globalThis.__mainErrors = []
    process.on('uncaughtException', (e) => globalThis.__mainErrors.push(String(e)))
  })
  await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows().forEach((w) => w.close()))
  const touched = path.join(APP, 'problems', 'beginner', fs.readdirSync(path.join(APP, 'problems', 'beginner')).find((d) => d.endsWith('-two-sum')), 'problem.json')
  fs.utimesSync(touched, new Date(), new Date())
  await new Promise((r) => setTimeout(r, 1500))
  const mainErrors = await app.evaluate(() => globalThis.__mainErrors)
  await app.evaluate(({ app }) => app.emit('activate'))
  const reopened = await app.waitForEvent('window', { timeout: 10_000 }).catch(() => undefined)
  const ok = mainErrors.length === 0 && reopened !== undefined
  if (!ok) failures.push(`closed window + file change: ${mainErrors.join('; ') || 'window did not reopen'}`)
  console.log(`${ok ? '✓' : '✗'} file changes with the window closed don't crash the main process; the window reopens`)
}

await app.close()
fs.rmSync(profile, { recursive: true, force: true })
if (pageErrors.length) failures.push(...pageErrors.map((e) => `page error: ${e}`))
console.log(failures.length ? `\n${failures.length} failure(s):\n  ${failures.join('\n  ')}` : '\nall e2e checks passed')
process.exit(failures.length ? 1 : 0)
