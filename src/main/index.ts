import { app, BrowserWindow, ipcMain, shell } from 'electron'
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
import { ProgressStore } from './progress'

// Lets e2e runs use a throwaway profile instead of the learner's real progress.
if (process.env.SWIFT_JUDGE_USER_DATA) app.setPath('userData', process.env.SWIFT_JUDGE_USER_DATA)

const appRoot = app.getAppPath()
const problemsRoot = process.env.SWIFT_JUDGE_PROBLEMS ?? join(appRoot, 'problems')
const bookRoot = join(appRoot, 'docs', 'swift-book')
const contentRoot = join(appRoot, 'content')

let problems = new Map<string, Problem>()
let loadErrors: string[] = []
let notes = new Map<string, NotesSection>()
let concepts: Concept[] = []
let quiz: QuizItem[] = []
let progress: ProgressStore
let win: BrowserWindow | undefined

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

function registerIpc(): void {
  ipcMain.handle('listProblems', () => summarize(problems.values()))
  ipcMain.handle('getProblem', (_e, id: string) => view(requireProblem(id)))
  ipcMain.handle('run', (_e, id: string, code: string) => judge(requireProblem(id), code, false))
  ipcMain.handle('submit', async (_e, id: string, code: string) => {
    const p = requireProblem(id)
    const result = await judge(p, code, true)
    const prev = progress.get(id)
    progress.update(id, {
      attempts: prev.attempts + 1,
      draft: code,
      ...(result.verdict === 'accepted' && !prev.solved ? { solved: true, solvedAt: new Date().toISOString() } : {})
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
  ipcMain.handle('getProgress', () => progress.all())
  ipcMain.handle('getLearn', (_e, id: string): LearnBundle => {
    const p = requireProblem(id)
    const section = p.meta.notesRef ? notes.get(p.meta.notesRef) : undefined
    return {
      notes: section ? { title: `§${section.number}. ${section.title}`, markdown: section.markdown } : undefined,
      docs: p.meta.docs,
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
      reloadContent()
      win?.webContents.send('problemsChanged')
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
  reloadContent()
  registerIpc()
  watchProblems()
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
