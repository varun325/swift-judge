/**
 * Scaffold a problem folder:
 *   npm run new-problem -- <track> <slug> [mode]
 *   npm run new-problem -- intermediate lru-cache function
 * Creates problems/<track>/<NNN>-<slug>/ with every file the judge expects.
 */
import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const [track, slug, mode = 'function'] = process.argv.slice(2)
if (!track || !slug || !['beginner', 'intermediate', 'advanced'].includes(track)) {
  console.error('usage: npm run new-problem -- <beginner|intermediate|advanced> <slug> [function|stdio|diagnostic|predict]')
  process.exit(1)
}
const trackDir = join(import.meta.dirname, '..', 'problems', track)
mkdirSync(trackDir, { recursive: true })
const nums = readdirSync(trackDir).map((d) => Number(d.split('-')[0])).filter((n) => !Number.isNaN(n))
const num = String((nums.length ? Math.max(...nums) : 0) + 10).padStart(3, '0')
const dir = join(trackDir, `${num}-${slug}`)
if (existsSync(dir)) throw new Error(`${dir} exists`)
mkdirSync(dir)

const fn = slug.replace(/-([a-z])/g, (_m, c: string) => c.toUpperCase())
const meta: Record<string, unknown> = {
  id: slug,
  title: slug.replace(/-/g, ' ').replace(/^\w/, (c) => c.toUpperCase()),
  track,
  difficulty: 'easy',
  topic: 'TODO',
  concepts: [],
  mode,
  docs: [{ title: 'TODO chapter', book: 'LanguageGuide/TheBasics' }],
  hints: [
    'Hint 1 — a nudge: which Swift feature or idea applies?',
    'Hint 2 — the approach: how to structure the solution.',
    'Hint 3 — nearly there: the key line or expression.'
  ]
}
if (mode === 'function') {
  meta.signature = { name: fn, params: [{ label: '_', name: 'input', type: '[Int]' }], returns: 'Int' }
}
writeFileSync(join(dir, 'problem.json'), JSON.stringify(meta, null, 2) + '\n')
writeFileSync(join(dir, 'statement.md'), 'Describe the task. Show examples in a ```swift block.\n')
writeFileSync(join(dir, 'explanation.md'), 'Explain the concept the reference solution demonstrates.\n')

const files: Record<string, [string, string, string]> = {
  function: [
    `func ${fn}(_ input: [Int]) -> Int {\n    // your code here\n    return 0\n}\n`,
    `func ${fn}(_ input: [Int]) -> Int {\n    input.reduce(0, +)\n}\n`,
    JSON.stringify([{ input: { input: [1, 2, 3] }, expected: 6 }, { input: { input: [] } }, { input: { input: [5] }, hidden: true }], null, 2)
  ],
  stdio: [
    `let line = readLine() ?? ""\n`,
    `let line = readLine() ?? ""\nprint(line.uppercased())\n`,
    JSON.stringify([{ input: 'hello\n', expected: 'HELLO' }, { input: 'swift\n', hidden: true }], null, 2)
  ],
  diagnostic: [
    `// write code that makes the compiler report the error\n`,
    `let x = 1\nx = 2\n`,
    JSON.stringify([{ name: 'Rejected', pattern: "cannot assign to value: 'x' is a 'let' constant" }], null, 2)
  ],
  predict: ['', '', JSON.stringify([{}])]
}
const [starter, solution, tests] = files[mode]
if (mode === 'predict') {
  writeFileSync(join(dir, 'snippet.swift'), 'let xs = [1, 2, 3]\nprint(xs.map { $0 * 2 })\n')
} else {
  writeFileSync(join(dir, 'starter.swift'), starter)
  writeFileSync(join(dir, 'solution.swift'), solution)
}
writeFileSync(join(dir, 'tests.json'), tests + '\n')
console.log(`created ${dir}\nnext: edit the files, then  npm run validate -- ${slug}`)
