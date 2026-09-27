import { app, BrowserWindow, ipcMain, safeStorage, shell } from 'electron'
import { existsSync, readFileSync, watch } from 'node:fs'
import { join } from 'node:path'
import type { LearnBundle, ProblemView } from '../shared/api'
import { stringifyExact } from '../shared/json'
import type { Concept, Problem, QuizItem } from '../shared/types'
import { listBook, readChapter } from './content/book'
import { loadAll, summarize } from './content/loader'
import { loadNotes, type NotesSection } from './content/notes'
import { judge } from './judge/judge'
import { findSwiftc, setCacheRoot, swiftVersion } from './judge/toolchain'
import { Playground, runPlayground } from './playground'
import { ProgressStore } from './progress'
import { loadFirebaseConfig } from './cloud/config'
import { CloudService } from './cloud/service'
import { afterSubmit } from '../shared/review'

// Lets e2e runs use a throwaway profile instead of the learner's real progress.
if (process.env.SWIFT_JUDGE_USER_DATA) app.setPath('userData', process.env.SWIFT_JUDGE_USER_DATA)

/**
 * Where problems, content and docs live.
 * - dev: the project folder (app.getAppPath()).
 * - packaged: the project folder recorded at build time (resources/source-root.json) if it still
 *   exists — so adding problems there works in the installed app too — otherwise the copy bundled
 *   in the app's Resources folder.
 */
function resolveContentRoot(): string {
  if (!app.isPackaged) return app.getAppPath()
  try {
    const recorded = JSON.parse(readFileSync(join(process.resourcesPath, 'source-root.json'), 'utf8')) as { root?: string }
    if (recorded.root && existsSync(join(recorded.root, 'problems'))) return recorded.root
  } catch {
    /* no recorded project folder — use the bundled copy */
  }
  return join(process.resourcesPath, 'bundle')
}

const appRoot = resolveContentRoot()
const problemsRoot = process.env.SWIFT_JUDGE_PROBLEMS ?? join(appRoot, 'problems')
const bookRoot = join(appRoot, 'docs', 'swift-book')
const contentRoot = join(appRoot, 'content')

let problems = new Map<string, Problem>()
let loadErrors: string[] = []
let notes = new Map<string, NotesSection>()
let concepts: Concept[] = []
let quiz: QuizItem[] = []
let progress: ProgressStore
let playground: Playground
let cloud: CloudService
let win: BrowserWindow | undefined

/**
 * Playground pages live next to swift-notes.md when running from the author's project folder, and
 * otherwise in this machine's userData folder. If the preferred folder can't be created (moved,
 * read-only, another OS), fall back to userData rather than failing to start.
 */
function openPlayground(): Playground {
  const userData = join(app.getPath('userData'), 'playground')
  const preferred =
    process.env.SWIFT_JUDGE_PLAYGROUND ?? (existsSync(join(appRoot, '..', 'swift-notes.md')) ? join(appRoot, '..', 'playground') : userData)
  try {
    return new Playground(preferred)
  } catch (e) {
    console.error(`playground folder ${preferred} unavailable, using ${userData}:`, e)
    return new Playground(userData)
  }
}

function readJson<T>(file: string, fallback: T): T {
  try {
    return existsSync(file) ? (JSON.parse(readFileSync(file, 'utf8')) as T) : fallback
  } catch (e) {
    loadErrors.push(`${file}: ${String(e)}`)
    return fallback
  }
}

function reloadContent(): void {
  const bank = loadAll(problemsRoot)
  problems = bank.problems
  loadErrors = bank.errors
  // Prefer the live notes next to the project (you may keep editing them), fall back to the bundled copy.
  notes = loadNotes([join(appRoot, '..', 'swift-notes.md'), join(contentRoot, 'swift-notes.md')])
  concepts = readJson<Concept[]>(join(contentRoot, 'concepts.json'), [])
  quiz = readJson<QuizItem[]>(join(contentRoot, 'quiz.json'), [])
  // Derive concept → problem links from each problem's `concepts` list.
  const byConcept = new Map<string, string[]>()
  for (const p of problems.values()) {
    for (const c of p.meta.concepts) byConcept.set(c, [...(byConcept.get(c) ?? []), p.meta.id])
  }
  concepts = concepts.map((c) => ({ ...c, problemIds: byConcept.get(c.id) ?? [] }))
}

function requireProblem(id: string): Problem {
  const p = problems.get(id)
  if (!p) throw new Error(`Unknown problem: ${id}`)
  return p
}

function view(p: Problem): ProblemView {
  const prog = progress.get(p.meta.id)
  const unlocked = prog.solved || prog.revealed
  return {
    id: p.meta.id,
    meta: p.meta,
    statement: p.statement,
    starter: p.starter,
    snippet: p.snippet,
    explanation: unlocked ? p.explanation : undefined,
    solution: unlocked && p.meta.mode !== 'predict' ? p.solution : undefined,
    visibleTests: p.tests
      .filter((t) => !t.hidden)
      .map((t, i) => ({
        name: t.name ?? `Case ${i + 1}`,
        input: p.meta.mode === 'function' ? stringifyExact(t.input ?? {}) : typeof t.input === 'string' ? t.input : undefined
      })),
    hiddenCount: p.tests.filter((t) => t.hidden).length
  }
}

/** Run a Playground mutation and schedule a cloud upload. */
function withSync<T>(result: T): T {
  cloud.changed()
  return result
}

function registerIpc(): void {
  ipcMain.handle('listProblems', () => summarize(problems.values()))
  ipcMain.handle('getProblem', (_e, id: string) => view(requireProblem(id)))
  ipcMain.handle('run', (_e, id: string, code: string) => judge(requireProblem(id), code, false))
  ipcMain.handle('submit', async (_e, id: string, code: string) => {
    const p = requireProblem(id)
    const result = await judge(p, code, true)
    const prev = progress.get(id)
    const accepted = result.verdict === 'accepted'
    const review = afterSubmit(prev, accepted, new Date())
    progress.update(id, {
      attempts: prev.attempts + 1,
      draft: code,
      ...(accepted && !prev.solved ? { solved: true, solvedAt: new Date().toISOString() } : {}),
      ...(review ? { review } : {})
    })
    return result
  })
  ipcMain.handle('saveDraft', (_e, id: string, code: string) => progress.update(id, { draft: code }))
  ipcMain.handle('resetDraft', (_e, id: string) => progress.clearDraft(id))
  ipcMain.handle('revealSolution', (_e, id: string) => {
    const p = requireProblem(id)
    progress.update(id, { revealed: true })
    return p.meta.mode === 'predict' ? '' : p.solution
  })
  ipcMain.handle('revealHint', (_e, id: string, level: number) => {
    const p = requireProblem(id)
    const current = progress.get(id).hintsRevealed ?? 0
    const next = Math.min(Math.max(current, level), p.meta.hints.length)
    if (next !== current) progress.update(id, { hintsRevealed: next })
  })
  ipcMain.handle('getProgress', () => progress.all())
  ipcMain.handle('getLearn', (_e, id: string): LearnBundle => {
    const p = requireProblem(id)
    const section = p.meta.notesRef ? notes.get(p.meta.notesRef) : undefined
    return {
      notes: section ? { title: `§${section.number}. ${section.title}`, markdown: section.markdown } : undefined,
      docs: p.meta.docs,
      videos: p.meta.videos,
      articles: p.meta.articles,
      concepts: concepts.filter((c) => p.meta.concepts.includes(c.id))
    }
  })
  ipcMain.handle('listBook', () => listBook(bookRoot))
  ipcMain.handle('getBookChapter', (_e, path: string) => readChapter(bookRoot, path))
  ipcMain.handle('listConcepts', () => concepts)
  ipcMain.handle('listQuiz', () => quiz)
  ipcMain.handle('saveQuizAnswer', (_e, id: string, correct: boolean) => progress.answerQuiz(id, correct))
  ipcMain.handle('getQuizProgress', () => progress.quiz())
  ipcMain.handle('swiftInfo', () => ({ version: swiftVersion(), swiftc: findSwiftc(), problemsRoot, loadErrors }))
  ipcMain.handle('cloud:status', () => cloud.current())
  ipcMain.handle('cloud:signIn', (_e, email: string, password: string, create: boolean) => cloud.signIn(email, password, create))
  ipcMain.handle('cloud:resetPassword', (_e, email: string) => cloud.resetPassword(email))
  ipcMain.handle('cloud:signOut', () => cloud.signOut())
  ipcMain.handle('cloud:syncNow', () => cloud.syncNow())

  ipcMain.handle('pg:root', () => playground.root)
  ipcMain.handle('pg:list', () => playground.list())
  ipcMain.handle('pg:load', (_e, id: string) => playground.load(id))
  ipcMain.handle('pg:save', (_e, id: string, part: { code?: string; notes?: string }) => withSync(playground.save(id, part)))
  ipcMain.handle('pg:create', (_e, title: string) => withSync(playground.create(title)))
  ipcMain.handle('pg:ensure', (_e, title: string, code: string, notes: string) => withSync(playground.ensure(title, code, notes)))
  ipcMain.handle('pg:rename', (_e, id: string, title: string) => withSync(playground.rename(id, title)))
  ipcMain.handle('pg:remove', async (_e, id: string) => {
    cloud.changed()
    // Move to the macOS Trash rather than deleting, so notes are recoverable.
    for (const file of playground.filesFor(id)) await shell.trashItem(file)
  })
  ipcMain.handle('pg:reveal', (_e, id: string) => {
    const [file] = playground.filesFor(id)
    if (file) shell.showItemInFolder(file)
  })
  ipcMain.handle('pg:run', (_e, code: string, stdin: string) => runPlayground(code, stdin))
  ipcMain.handle('openExternal', (_e, url: string) => {
    if (/^https:\/\//.test(url)) return shell.openExternal(url)
  })
}

/** Plug-in workflow: drop a folder into problems/ and the list refreshes. */
function watchProblems(): void {
  if (!existsSync(problemsRoot)) return
  let timer: NodeJS.Timeout | undefined
  const onChange = (): void => {
    clearTimeout(timer)
    timer = setTimeout(() => {
      try {
        reloadContent()
      } catch (e) {
        // Mid-write (e.g. a batch of problems being regenerated): keep the current bank; the
        // next change event reloads again.
        console.error('reload failed, keeping previous content:', e)
        return
      }
      // The window may have been closed (the app keeps running on macOS) — only notify live ones.
      for (const w of BrowserWindow.getAllWindows()) {
        if (!w.isDestroyed() && !w.webContents.isDestroyed()) w.webContents.send('problemsChanged')
      }
    }, 300)
  }
  watch(problemsRoot, { recursive: true }, onChange)
  if (existsSync(contentRoot)) watch(contentRoot, { recursive: true }, onChange)
}

function createWindow(): void {
  win = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 960,
    minHeight: 600,
    title: 'Swift Judge',
    backgroundColor: '#1e1f24',
    webPreferences: {
      preload: join(import.meta.dirname, '../preload/index.mjs'),
      sandbox: false,
      contextIsolation: true
    }
  })
  win.on('closed', () => {
    win = undefined
  })
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https:\/\//.test(url)) void shell.openExternal(url)
    return { action: 'deny' }
  })
  if (process.env.ELECTRON_RENDERER_URL) void win.loadURL(process.env.ELECTRON_RENDERER_URL)
  else void win.loadFile(join(import.meta.dirname, '../renderer/index.html'))
}

app.whenReady().then(() => {
  setCacheRoot(join(app.getPath('userData'), 'cache'))
  progress = new ProgressStore(join(app.getPath('userData'), 'progress.json'))
  // Playground pages live next to swift-notes.md when that folder exists, else in userData.
  playground = openPlayground()
  cloud = new CloudService({
    // Firebase web config: env override → project folder (dev / local install) → bundled in the build.
    config: loadFirebaseConfig([
      process.env.SWIFT_JUDGE_FIREBASE_CONFIG ?? '',
      process.env.SWIFT_JUDGE_FIREBASE_CONFIG ? '' : join(appRoot, 'firebase.config.json'),
      process.env.SWIFT_JUDGE_FIREBASE_CONFIG ? '' : join(process.resourcesPath ?? '', 'firebase.config.json')
    ]),
    sessionFile: join(app.getPath('userData'), 'cloud-session.bin'),
    box: {
      available: () => safeStorage.isEncryptionAvailable(),
      encrypt: (t) => safeStorage.encryptString(t),
      decrypt: (b) => safeStorage.decryptString(b)
    },
    deps: {
      progress,
      playground: () => playground,
      stateFile: join(app.getPath('userData'), 'cloud-sync-state.json'),
      removePage: async (id) => {
        for (const file of playground.filesFor(id)) await shell.trashItem(file)
      }
    },
    notify: (status, changed) => {
      const dataChanged = Boolean(changed && (changed.changedProblems || changed.changedQuiz || changed.changedPlayground))
      for (const w of BrowserWindow.getAllWindows()) {
        if (!w.isDestroyed() && !w.webContents.isDestroyed()) w.webContents.send('cloud:changed', status, dataChanged)
      }
    }
  })
  progress.onChange = () => cloud.changed()
  reloadContent()
  registerIpc()
  watchProblems()
  createWindow()
  cloud.start()
  app.on('browser-window-focus', () => cloud.focused())
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Upload the last changes before quitting (bounded, so quitting never hangs).
let flushed = false
app.on('before-quit', (event) => {
  if (flushed || !cloud?.current().signedIn) return
  event.preventDefault()
  flushed = true
  void cloud.flush().finally(() => app.quit())
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
