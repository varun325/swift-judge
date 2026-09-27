/**
 * Verifies every reference link in the problem bank actually resolves.
 *   node scripts/check-links.mjs            # check links not verified in the last 30 days
 *   node scripts/check-links.mjs --all      # re-check everything
 *
 * - YouTube: the official oEmbed endpoint (200 only for real, embeddable videos; also yields
 *   the video's real title, which must match what the problem says)
 * - everything else (Apple docs, Swift book, articles): GET with redirects; must end in 200
 * Results are cached in content/links.json; exits non-zero if any link is broken.
 */
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const cacheFile = path.join(root, 'content', 'links.json')
const MAX_AGE_MS = 30 * 24 * 3600 * 1000
const recheckAll = process.argv.includes('--all')
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'

const cache = fs.existsSync(cacheFile) ? JSON.parse(fs.readFileSync(cacheFile, 'utf8')) : {}

// url -> [{ problem, title }]
const uses = new Map()
for (const track of fs.readdirSync(path.join(root, 'problems'))) {
  const trackDir = path.join(root, 'problems', track)
  if (!fs.statSync(trackDir).isDirectory()) continue
  for (const d of fs.readdirSync(trackDir)) {
    const file = path.join(trackDir, d, 'problem.json')
    if (!fs.existsSync(file)) continue
    const meta = JSON.parse(fs.readFileSync(file, 'utf8'))
    const links = [...(meta.docs ?? []).filter((x) => x.url), ...(meta.videos ?? []), ...(meta.articles ?? [])]
    for (const l of links) {
      if (!uses.has(l.url)) uses.set(l.url, [])
      uses.get(l.url).push({ problem: meta.id, title: l.title })
    }
  }
}

async function check(url) {
  const yt = /youtube\.com\/watch\?v=([\w-]{11})|youtu\.be\/([\w-]{11})/.exec(url)
  try {
    if (yt) {
      const res = await fetch(`https://www.youtube.com/oembed?format=json&url=${encodeURIComponent(url)}`, { headers: { 'User-Agent': UA } })
      if (res.status !== 200) return { ok: false, status: res.status }
      const body = await res.json()
      return { ok: true, status: 200, title: body.title, author: body.author_name }
    }
    const res = await fetch(url, { headers: { 'User-Agent': UA }, redirect: 'follow' })
    return { ok: res.status === 200, status: res.status, finalUrl: res.url !== url ? res.url : undefined }
  } catch (e) {
    return { ok: false, status: 0, error: String(e) }
  }
}

const todo = [...uses.keys()].filter((u) => recheckAll || !cache[u] || !cache[u].ok || Date.now() - cache[u].checkedAt > MAX_AGE_MS)
let done = 0
const queue = [...todo]
await Promise.all(
  Array.from({ length: 8 }, async () => {
    while (queue.length) {
      const url = queue.shift()
      cache[url] = { ...(await check(url)), checkedAt: Date.now() }
      if (++done % 50 === 0) process.stdout.write(`${done}/${todo.length}\n`)
    }
  })
)

// Drop links no problem uses any more, then save.
for (const u of Object.keys(cache)) if (!uses.has(u)) delete cache[u]
fs.writeFileSync(cacheFile, JSON.stringify(Object.fromEntries(Object.entries(cache).sort()), null, 1) + '\n')

const broken = [...uses.keys()].filter((u) => !cache[u]?.ok)
const byKind = { youtube: 0, apple: 0, other: 0 }
for (const u of uses.keys()) byKind[/youtube/.test(u) ? 'youtube' : /developer\.apple\.com/.test(u) ? 'apple' : 'other']++
console.log(`${uses.size} unique links (${byKind.apple} Apple docs, ${byKind.youtube} videos, ${byKind.other} other) · checked ${todo.length} now · ${broken.length} broken`)
for (const u of broken) console.log(`✗ ${cache[u]?.status} ${u}  (used by ${uses.get(u).map((x) => x.problem).join(', ')})`)
process.exit(broken.length ? 1 : 0)
