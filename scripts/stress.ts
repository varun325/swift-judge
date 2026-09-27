/**
 * Flakiness hunter: judges reference solutions many times in parallel (to simulate a loaded
 * machine) and reports any run that isn't Accepted. Crashes that only appear under load show up here.
 *   npx tsx scripts/stress.ts <id-filter> [rounds=30] [parallel=10]
 */
import { join } from 'node:path'
import { loadAll, supportedHere } from '../src/main/content/loader'
import { judge } from '../src/main/judge/judge'
import { setCacheRoot } from '../src/main/judge/toolchain'

const root = join(import.meta.dirname, '..')
setCacheRoot(join(root, '.cache'))
const [filter = '', roundsArg = '30', parallelArg = '10'] = process.argv.slice(2)
const rounds = Number(roundsArg)
const parallel = Number(parallelArg)

const { problems } = loadAll(join(root, 'problems'))
const tracks = (process.env.TRACKS ?? '').split(',').filter(Boolean)
const targets = [...problems.values()].filter((p) => (!tracks.length || tracks.includes(p.meta.track)) && p.meta.id.includes(filter) && supportedHere(p) && p.meta.mode === 'function')
const jobs = targets.flatMap((p) => Array.from({ length: rounds }, () => p))
const failures = new Map<string, string[]>()
let done = 0
const t0 = Date.now()
await Promise.all(
  Array.from({ length: parallel }, async () => {
    for (let p = jobs.shift(); p; p = jobs.shift()) {
      const source = p.meta.mode === 'predict' ? '' : p.solution
      const r = await judge(p, source, true)
      if (r.verdict !== 'accepted') {
        const bad = r.tests.find((t) => t.status !== 'passed')
        failures.set(p.meta.id, [...(failures.get(p.meta.id) ?? []), `${r.verdict}: ${(bad?.stderr ?? r.compilerOutput ?? '').split('\n').slice(0, 2).join(' | ')}`])
      }
      done++
    }
  })
)
console.log(`${targets.length} problems × ${rounds} rounds (${parallel} in parallel): ${done} judged in ${((Date.now() - t0) / 1000).toFixed(1)}s`)
for (const [id, errs] of failures) console.log(`✗ ${id}: ${errs.length}/${rounds} failed — ${errs[0]}`)
if (!failures.size) console.log('no failures')
process.exit(failures.size ? 1 : 0)
