import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join, normalize } from 'node:path'
import type { BookChapter } from '../../shared/api'

const SECTIONS = ['GuidedTour', 'LanguageGuide', 'ReferenceManual']

export function listBook(root: string): BookChapter[] {
  const out: BookChapter[] = []
  for (const s of SECTIONS) {
    const dir = join(root, s)
    if (!existsSync(dir)) continue
    for (const f of readdirSync(dir).filter((f) => f.endsWith('.md')).sort()) {
      const text = readFileSync(join(dir, f), 'utf8')
      const title = /^# (.+)$/m.exec(text)?.[1] ?? f.replace(/\.md$/, '')
      out.push({ path: `${s}/${f.replace(/\.md$/, '')}`, title })
    }
  }
  return out
}

/** Read a chapter and strip DocC-only syntax that plain Markdown renderers don't understand. */
export function readChapter(root: string, path: string): string {
  const file = normalize(join(root, `${path}.md`))
  if (!file.startsWith(normalize(root)) || !existsSync(file)) return `Chapter not found: ${path}`
  return readFileSync(file, 'utf8')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/^@\w+(\([^)]*\))?\s*\{[\s\S]*?^\}\s*$/gm, '')
    .replace(/<doc:([\w-]+)(#[\w-]+)?>/g, (_m, name: string) => `**${name.replace(/([a-z])([A-Z])/g, '$1 $2')}**`)
    .replace(/^> (Note|Important|Warning|Experiment|Tip): /gm, '> **$1:** ')
    .replace(/(?<!`)``(?!`)([^`\n]+?)(?<!`)``(?!`)/g, '`$1`')
}
