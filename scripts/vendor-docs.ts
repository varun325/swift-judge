/**
 * Vendors offline reference material:
 *   docs/swift-book/   — The Swift Programming Language (swiftlang/swift-book, Apache-2.0)
 *   docs/interview/    — Devinterview-io/swift-interview-questions README
 * Re-run any time to refresh; records the commit SHAs in docs/SOURCES.json.
 */
import { execFileSync } from 'node:child_process'
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync, readdirSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const root = join(import.meta.dirname, '..')
const docs = join(root, 'docs')
const work = mkdtempSync(join(tmpdir(), 'swj-vendor-'))

function clone(url: string, name: string): { dir: string; sha: string } {
  const dir = join(work, name)
  execFileSync('git', ['clone', '--depth', '1', url, dir], { stdio: 'inherit' })
  const sha = execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim()
  return { dir, sha }
}

try {
  const book = clone('https://github.com/swiftlang/swift-book.git', 'swift-book')
  const tspl = join(book.dir, 'TSPL.docc')
  const outBook = join(docs, 'swift-book')
  rmSync(outBook, { recursive: true, force: true })
  mkdirSync(outBook, { recursive: true })
  for (const section of ['GuidedTour', 'LanguageGuide', 'ReferenceManual']) {
    if (existsSync(join(tspl, section))) cpSync(join(tspl, section), join(outBook, section), { recursive: true })
  }
  cpSync(join(book.dir, 'LICENSE.txt'), join(outBook, 'LICENSE.txt'))

  const iq = clone('https://github.com/Devinterview-io/swift-interview-questions.git', 'interview')
  const outIq = join(docs, 'interview')
  rmSync(outIq, { recursive: true, force: true })
  mkdirSync(outIq, { recursive: true })
  for (const f of readdirSync(iq.dir)) {
    if (f.toLowerCase().endsWith('.md') || f.toLowerCase().startsWith('license')) cpSync(join(iq.dir, f), join(outIq, f))
  }

  writeFileSync(
    join(docs, 'SOURCES.json'),
    JSON.stringify({
      'swift-book': { repo: 'https://github.com/swiftlang/swift-book', commit: book.sha, license: 'Apache-2.0' },
      interview: { repo: 'https://github.com/Devinterview-io/swift-interview-questions', commit: iq.sha },
      vendoredAt: new Date().toISOString()
    }, null, 2) + '\n'
  )
  console.log('vendored swift-book', book.sha, 'and interview questions', iq.sha)
} finally {
  rmSync(work, { recursive: true, force: true })
}
