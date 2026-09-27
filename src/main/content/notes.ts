import { existsSync, readFileSync } from 'node:fs'

export interface NotesSection {
  number: string
  title: string
  markdown: string
}

/**
 * Split swift-notes.md on its "## N. Title" headings so a problem's notesRef ("14")
 * can pull in the matching section.
 */
export function loadNotes(paths: string[]): Map<string, NotesSection> {
  const sections = new Map<string, NotesSection>()
  const file = paths.find((p) => existsSync(p))
  if (!file) return sections
  const text = readFileSync(file, 'utf8')
  const re = /^## (\d+)\. (.+)$/gm
  const heads = [...text.matchAll(re)]
  heads.forEach((m, i) => {
    const start = m.index! + m[0].length
    const nextH2 = text.slice(start).search(/^## /m)
    const end = nextH2 >= 0 ? start + nextH2 : text.length
    const stop = i + 1 < heads.length ? Math.min(end, heads[i + 1].index!) : end
    sections.set(m[1], { number: m[1], title: m[2].trim(), markdown: text.slice(start, stop).replace(/\n---\s*$/, '').trim() })
  })
  return sections
}
