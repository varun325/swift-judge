/**
 * Packages the app as dist/mac-arm64/Swift Judge.app (run after `electron-vite build`).
 *   node scripts/package.mjs            # build the .app
 *   node scripts/package.mjs --install  # copy the built .app into /Applications
 *   node scripts/package.mjs --win      # Windows x64: NSIS installer + portable .exe in dist/
 *   node scripts/package.mjs --dmg      # wrap the already built, signed .app in dist/*.dmg
 *
 *   node scripts/package.mjs --portable # the .app for distribution (used by the .dmg)
 *
 * A local build records this project folder in Resources/source-root.json, so the installed app
 * reads problems, notes and docs live from here (keeping the plug-in workflow). Builds meant for
 * other machines (--portable, --win) record nothing: they use only the copy bundled inside the app,
 * so no path from this machine ships in a download.
 */
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const appName = 'Swift Judge.app'
const built = path.join(root, 'dist', 'mac-arm64', appName)
const target = path.join('/Applications', appName)

function recordSourceRoot(local) {
  fs.mkdirSync(path.join(root, 'build'), { recursive: true })
  fs.writeFileSync(path.join(root, 'build', 'source-root.json'), JSON.stringify(local ? { root } : {}, null, 2) + '\n')
  // Cloud sync: bundle the local, git-ignored firebase.config.json when present; otherwise the
  // build is offline-only ({} means "no cloud"). The file never enters git (see check-secrets).
  const firebase = path.join(root, 'firebase.config.json')
  fs.writeFileSync(path.join(root, 'build', 'firebase.config.json'), fs.existsSync(firebase) ? fs.readFileSync(firebase) : '{}\n')
}

if (process.argv.includes('--dmg')) {
  if (!fs.existsSync(built)) throw new Error(`No build at ${built} — run \`npm run package\` first.`)
  // Package the signed .app as-is, so the copy inside the image keeps a valid signature.
  execFileSync('npx', ['electron-builder', '--mac', 'dmg', '--arm64', '--prepackaged', built], { cwd: root, stdio: 'inherit' })
  const dmg = fs.readdirSync(path.join(root, 'dist')).find((f) => f.endsWith('.dmg'))
  execFileSync('hdiutil', ['verify', path.join(root, 'dist', dmg)], { stdio: 'inherit' })
  console.log(`built dist/${dmg}`)
} else if (process.argv.includes('--win')) {
  recordSourceRoot(false)
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
  recordSourceRoot(!process.argv.includes('--portable'))
  execFileSync('npx', ['electron-builder', '--mac', 'dir', '--arm64'], { cwd: root, stdio: 'inherit' })
  // No Developer ID here: ad-hoc sign the whole bundle so Apple Silicon accepts the modified app.
  execFileSync('codesign', ['--force', '--deep', '--sign', '-', built], { stdio: 'inherit' })
  execFileSync('codesign', ['--verify', '--deep', '--strict', built], { stdio: 'inherit' })
  console.log(`built and ad-hoc signed ${built}`)
}
