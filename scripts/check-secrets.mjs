/**
 * Refuses to let credentials reach git. Scans staged files (or, with --all, every tracked file)
 * for Google/Firebase API keys, private keys and service-account JSON, and for files that must stay
 * local (firebase.config.json, .firebaserc, sessions).
 *   node scripts/check-secrets.mjs          # staged files (used by the pre-commit hook)
 *   node scripts/check-secrets.mjs --all    # everything tracked
 */
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'

const all = process.argv.includes('--all')
const files = execFileSync('git', all ? ['ls-files'] : ['diff', '--cached', '--name-only', '--diff-filter=ACM'], { encoding: 'utf8' })
  .split('\n')
  .filter(Boolean)

const FORBIDDEN_FILES = [/(^|\/)firebase\.config\.json$/, /(^|\/)\.firebaserc$/, /(^|\/)GoogleService-Info\.plist$/, /(^|\/)google-services\.json$/, /session\.bin$/, /\.env(\..*)?$/]
const PATTERNS = [
  ['Google/Firebase API key', /AIza[0-9A-Za-z_-]{35}/],
  ['private key', /-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ['service account credentials', /"type"\s*:\s*"service_account"/],
  ['refresh token', /"refreshToken"\s*:\s*"[A-Za-z0-9_-]{40,}"/]
]

const problems = []
for (const f of files) {
  if (FORBIDDEN_FILES.some((rx) => rx.test(f)) && !f.endsWith('.example.json')) problems.push(`${f}: must stay local (it's git-ignored for a reason)`)
  if (!fs.existsSync(f) || fs.statSync(f).size > 5_000_000) continue
  const text = all ? fs.readFileSync(f, 'utf8') : execFileSync('git', ['show', `:${f}`], { encoding: 'utf8', maxBuffer: 50_000_000 })
  for (const [what, rx] of PATTERNS) if (rx.test(text)) problems.push(`${f}: contains a ${what}`)
}
if (problems.length) {
  console.error(`✗ refusing: sensitive data found\n  ${problems.join('\n  ')}`)
  process.exit(1)
}
console.log(`✓ no secrets in ${files.length} ${all ? 'tracked' : 'staged'} file(s)`)
