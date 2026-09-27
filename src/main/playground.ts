import { existsSync, mkdirSync, readdirSync, readFileSync, renameSync, statSync, utimesSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import type { PlaygroundPage, PlaygroundRun, PlaygroundSummary } from '../shared/api'
import { presentCompilerOutput } from './judge/diagnostics'
import { run } from './judge/runner'
import { withQuietCrashes } from './judge/harness'
import { compile } from './judge/toolchain'

const RUN_TIMEOUT_MS = 10_000

export const WELCOME_CODE = `// Scratch space: write any Swift, press ⌘↵ to compile and run.
// Top-level code works here, just like main.swift.

struct Point { var x = 0, y = 0 }

var a = Point()
var b = a        // structs copy
b.x = 10
print(a.x, b.x)  // 0 10
`

export const WELCOME_NOTES = `# Scratchpad

Notes for this page live in a plain Markdown file next to the code, so you can
read them anywhere. Use **Append run to notes** to paste the code and its output
here as a record.
`

/** Pages are pairs of files: <slug>.swift (code) and <slug>.md (notes). */
export class Playground {
  constructor(readonly root: string) {
    mkdirSync(root, { recursive: true })
    if (this.list().length === 0) this.create('scratchpad', WELCOME_CODE, WELCOME_NOTES)
  }

  private paths(id: string): { code: string; notes: string } {
    if (!/^[a-z0-9][a-z0-9-]*$/.test(id)) throw new Error(`invalid page id: ${id}`)
    return { code: join(this.root, `${id}.swift`), notes: join(this.root, `${id}.md`) }
  }

  static slugify(title: string): string {
    return (
      title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '')
        .slice(0, 60) || 'untitled'
    )
  }

  list(): PlaygroundSummary[] {
    const ids = new Set(
      readdirSync(this.root)
        .filter((f) => /^[a-z0-9][a-z0-9-]*\.(swift|md)$/.test(f))
        .map((f) => f.replace(/\.(swift|md)$/, ''))
    )
    return [...ids]
      .map((id) => {
        const { code, notes } = this.paths(id)
        const mtime = Math.max(...[code, notes].filter(existsSync).map((p) => statSync(p).mtimeMs))
        return { id, title: id.replace(/-/g, ' '), updatedAt: new Date(mtime).toISOString() }
      })
      .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
  }

  load(id: string): PlaygroundPage {
    const { code, notes } = this.paths(id)
    return {
      id,
      title: id.replace(/-/g, ' '),
      code: existsSync(code) ? readFileSync(code, 'utf8') : '',
      notes: existsSync(notes) ? readFileSync(notes, 'utf8') : ''
    }
  }

  save(id: string, part: { code?: string; notes?: string }): void {
    const paths = this.paths(id)
    if (part.code !== undefined) writeFileSync(paths.code, part.code)
    if (part.notes !== undefined) writeFileSync(paths.notes, part.notes)
  }

  /** Creates a page with a unique id derived from the title. */
  create(title: string, code = '', notes = ''): string {
    const base = Playground.slugify(title)
    let id = base
    for (let n = 2; existsSync(this.paths(id).code) || existsSync(this.paths(id).notes); n++) id = `${base}-${n}`
    this.save(id, { code, notes: notes || `# ${title}\n\n` })
    return id
  }

  /** Code, notes and last-modified time of a page, or undefined if it doesn't exist (for sync). */
  snapshot(id: string): { code: string; notes: string; updatedAt: number } | undefined {
    const { code, notes } = this.paths(id)
    if (!existsSync(code) && !existsSync(notes)) return undefined
    const files = [code, notes].filter(existsSync)
    return {
      code: existsSync(code) ? readFileSync(code, 'utf8') : '',
      notes: existsSync(notes) ? readFileSync(notes, 'utf8') : '',
      updatedAt: Math.max(...files.map((f) => statSync(f).mtimeMs))
    }
  }

  /** Write a page that came from the cloud, keeping its original modification time. */
  putFromCloud(id: string, code: string, notes: string, updatedAt: number): void {
    const paths = this.paths(id)
    writeFileSync(paths.code, code)
    writeFileSync(paths.notes, notes)
    const t = new Date(updatedAt)
    utimesSync(paths.code, t, t)
    utimesSync(paths.notes, t, t)
  }

  /** A free id based on `id` (e.g. for a conflict copy). */
  freeId(id: string): string {
    let next = id
    for (let n = 2; this.snapshot(next); n++) next = `${id}-${n}`
    return next
  }

  /** The page for `title`, created with this content only if it doesn't exist yet (answers are never overwritten). */
  ensure(title: string, code: string, notes: string): string {
    const id = Playground.slugify(title)
    const { code: c, notes: n } = this.paths(id)
    if (existsSync(c) || existsSync(n)) return id
    this.save(id, { code, notes })
    return id
  }

  rename(id: string, title: string): string {
    const next = Playground.slugify(title)
    if (next === id) return id
    const from = this.paths(id)
    const to = this.paths(next)
    if (existsSync(to.code) || existsSync(to.notes)) throw new Error(`a page named "${next}" already exists`)
    if (existsSync(from.code)) renameSync(from.code, to.code)
    if (existsSync(from.notes)) renameSync(from.notes, to.notes)
    return next
  }

  filesFor(id: string): string[] {
    const { code, notes } = this.paths(id)
    return [code, notes].filter(existsSync)
  }
}

/** Compile `code` as main.swift and run it once with the given stdin. */
export async function runPlayground(code: string, stdin: string): Promise<PlaygroundRun> {
  const built = await compile([{ name: 'main.swift', content: withQuietCrashes(code) }], '6')
  const compilerOutput = presentCompilerOutput(built.output, 'main.swift')
  if (!built.ok || !built.binary) {
    return { ok: false, phase: 'compile', diagnostics: built.diagnostics, compilerOutput, stdout: '', stderr: '', exitCode: null, ms: 0, compileMs: built.ms }
  }
  const res = await run(built.binary, [], { stdin, timeoutMs: RUN_TIMEOUT_MS })
  return {
    ok: !res.timedOut && res.code === 0,
    phase: 'run',
    diagnostics: built.diagnostics,
    compilerOutput,
    stdout: res.stdout + (res.truncated ? '\n… output truncated at 1 MB' : ''),
    stderr: res.timedOut ? `stopped after ${RUN_TIMEOUT_MS / 1000}s (infinite loop?)` : res.stderr,
    exitCode: res.code,
    signal: res.signal ?? undefined,
    ms: Math.round(res.ms),
    compileMs: Math.round(built.ms)
  }
}
