import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { z } from 'zod'
import { parseExact } from '../../shared/json'
import { ProblemMeta, TestCase, type Problem, type ProblemSummary } from '../../shared/types'

function readOpt(dir: string, name: string): string | undefined {
  const p = join(dir, name)
  return existsSync(p) ? readFileSync(p, 'utf8') : undefined
}

export class ProblemLoadError extends Error {}

/** Load one problem folder. Throws ProblemLoadError with a readable message on schema errors. */
export function loadProblem(dir: string): Problem {
  const where = dir
  const parse = <T>(schema: z.ZodType<T>, file: string): T => {
    const raw = readOpt(dir, file)
    if (raw === undefined) throw new ProblemLoadError(`${where}: missing ${file}`)
    let json: unknown
    try {
      json = parseExact(raw)
    } catch (e) {
      throw new ProblemLoadError(`${where}/${file}: invalid JSON (${String(e)})`)
    }
    const r = schema.safeParse(json)
    if (!r.success) throw new ProblemLoadError(`${where}/${file}: ${z.prettifyError(r.error)}`)
    return r.data
  }

  const meta = parse(ProblemMeta, 'problem.json')
  const tests = parse(z.array(TestCase), 'tests.json')
  const snippet = readOpt(dir, 'snippet.swift')
  const solution = readOpt(dir, 'solution.swift') ?? ''
  if (!solution && meta.mode !== 'diagnostic' && meta.mode !== 'predict') {
    throw new ProblemLoadError(`${where}: missing solution.swift`)
  }
  if (meta.mode === 'predict' && !snippet) throw new ProblemLoadError(`${where}: predict mode needs snippet.swift`)

  return {
    meta,
    dir,
    statement: readOpt(dir, 'statement.md') ?? '',
    starter: readOpt(dir, 'starter.swift') ?? '',
    solution,
    snippet,
    explanation: readOpt(dir, 'explanation.md') ?? '',
    harness: readOpt(dir, 'harness.swift'),
    tests
  }
}

/** Every directory under `root` containing a problem.json is a problem. */
export function findProblemDirs(root: string): string[] {
  const out: string[] = []
  const walk = (d: string): void => {
    if (existsSync(join(d, 'problem.json'))) {
      out.push(d)
      return
    }
    for (const e of readdirSync(d)) {
      const p = join(d, e)
      if (!e.startsWith('.') && statSync(p).isDirectory()) walk(p)
    }
  }
  if (existsSync(root)) walk(root)
  return out.sort()
}

export interface LoadedBank {
  problems: Map<string, Problem>
  errors: string[]
}

export function loadAll(root: string): LoadedBank {
  const problems = new Map<string, Problem>()
  const errors: string[] = []
  for (const dir of findProblemDirs(root)) {
    try {
      const p = loadProblem(dir)
      if (problems.has(p.meta.id)) {
        errors.push(`${relative(root, dir)}: duplicate id "${p.meta.id}" (also in ${relative(root, problems.get(p.meta.id)!.dir)})`)
        continue
      }
      problems.set(p.meta.id, p)
    } catch (e) {
      errors.push(e instanceof Error ? e.message : String(e))
    }
  }
  return { problems, errors }
}

const TRACK_ORDER = { beginner: 0, intermediate: 1, advanced: 2 } as const

export function summarize(problems: Iterable<Problem>): ProblemSummary[] {
  return [...problems]
    .map((p) => ({
      id: p.meta.id,
      title: p.meta.title,
      track: p.meta.track,
      difficulty: p.meta.difficulty,
      topic: p.meta.topic,
      mode: p.meta.mode,
      concepts: p.meta.concepts,
      order: relativeOrder(p.dir)
    }))
    .sort((a, b) => TRACK_ORDER[a.track] - TRACK_ORDER[b.track] || a.order.localeCompare(b.order))
    .map(({ order: _order, ...s }) => s)
}

/** Folder names are NNN-slug, so sorting by path gives curriculum order. */
function relativeOrder(dir: string): string {
  return dir.split('/').slice(-2).join('/')
}
