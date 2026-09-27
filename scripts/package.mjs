/**
 * Packages the app as dist/mac-arm64/Swift Judge.app (run after `electron-vite build`).
 *   node scripts/package.mjs            # build the .app
 *   node scripts/package.mjs --install  # copy the built .app into /Applications
 *   node scripts/package.mjs --win      # Windows x64: NSIS installer + portable .exe in dist/
 *   node scripts/package.mjs --dmg      # wrap the already built, signed .app in dist/*.dmg
 *
 * The packaged app records this project folder in Resources/source-root.json, so it reads
 * problems, notes and docs live from here (and keeps the plug-in workflow). A copy is also
 * bundled inside the app as a fallback if the project folder moves.
 */
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const appName = 'Swift Judge.app'
const built = path.join(root, 'dist', 'mac-arm64', appName)
const target = path.join('/Applications', appName)

function recordSourceRoot() {
  fs.mkdirSync(path.join(root, 'build'), { recursive: true })
  fs.writeFileSync(path.join(root, 'build', 'source-root.json'), JSON.stringify({ root }, null, 2) + '\n')
}

if (process.argv.includes('--dmg')) {
  if (!fs.existsSync(built)) throw new Error(`No build at ${built} — run \`npm run package\` first.`)
  // Package the signed .app as-is, so the copy inside the image keeps a valid signature.
  execFileSync('npx', ['electron-builder', '--mac', 'dmg', '--arm64', '--prepackaged', built], { cwd: root, stdio: 'inherit' })
  const dmg = fs.readdirSync(path.join(root, 'dist')).find((f) => f.endsWith('.dmg'))
  execFileSync('hdiutil', ['verify', path.join(root, 'dist', dmg)], { stdio: 'inherit' })
  console.log(`built dist/${dmg}`)
} else if (process.argv.includes('--win')) {
  // On Windows the recorded macOS path won't exist, so the app uses its bundled problems.
  recordSourceRoot()
  execFileSync('npx', ['electron-builder', '--win', '--x64'], { cwd: root, stdio: 'inherit' })
  for (const f of fs.readdirSync(path.join(root, 'dist')).filter((f) => f.endsWith('.exe'))) console.log(`built dist/${f}`)
} else if (process.argv.includes('--install')) {
  if (!fs.existsSync(built)) throw new Error(`No build at ${built} — run \`npm run package\` first.`)
  try {
    execFileSync('pgrep', ['-f', `${target}/Contents/MacOS/`], { stdio: 'pipe' })
    console.error('Swift Judge is running — quit it first, then run this again.')
    process.exit(1)
  } catch {
    /* not running */
  }
  fs.rmSync(target, { recursive: true, force: true })
  // ditto preserves the bundle's symlinks, permissions and code signature.
  execFileSync('ditto', [built, target], { stdio: 'inherit' })
  console.log(`installed ${target}`)
} else {
  recordSourceRoot()
  execFileSync('npx', ['electron-builder', '--mac', 'dir', '--arm64'], { cwd: root, stdio: 'inherit' })
  // No Developer ID here: ad-hoc sign the whole bundle so Apple Silicon accepts the modified app.
  execFileSync('codesign', ['--force', '--deep', '--sign', '-', built], { stdio: 'inherit' })
  execFileSync('codesign', ['--verify', '--deep', '--strict', built], { stdio: 'inherit' })
  console.log(`built and ad-hoc signed ${built}`)
}
