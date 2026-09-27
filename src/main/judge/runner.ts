import { spawn } from 'node:child_process'

export interface RunOptions {
  cwd?: string
  stdin?: string
  timeoutMs: number
  maxOutputBytes?: number
  /** Kill if no stdout chunk containing `progressMarker` arrives within this many ms. */
  progressTimeoutMs?: number
  progressMarker?: string
}

export interface RunOutput {
  code: number | null
  signal: NodeJS.Signals | null
  stdout: string
  stderr: string
  timedOut: boolean
  truncated: boolean
  ms: number
}

const DEFAULT_MAX_OUTPUT = 1024 * 1024

/** Spawn a process, feed stdin, enforce a wall-clock timeout and an output cap. */
export function run(cmd: string, args: string[], opts: RunOptions): Promise<RunOutput> {
  const max = opts.maxOutputBytes ?? DEFAULT_MAX_OUTPUT
  return new Promise((resolve) => {
    const start = performance.now()
    const child = spawn(cmd, args, { cwd: opts.cwd, stdio: ['pipe', 'pipe', 'pipe'] })
    const out: Buffer[] = []
    const err: Buffer[] = []
    let outBytes = 0
    let errBytes = 0
    let truncated = false
    let timedOut = false

    const kill = (): void => {
      if (child.exitCode === null && child.signalCode === null) child.kill('SIGKILL')
    }
    const timer = setTimeout(() => {
      timedOut = true
      kill()
    }, opts.timeoutMs)
    let watchdog: NodeJS.Timeout | undefined
    const armWatchdog = (): void => {
      if (!opts.progressTimeoutMs) return
      clearTimeout(watchdog)
      watchdog = setTimeout(() => {
        timedOut = true
        kill()
      }, opts.progressTimeoutMs)
    }
    armWatchdog()

    child.stdout.on('data', (b: Buffer) => {
      if (opts.progressMarker && b.includes(opts.progressMarker)) armWatchdog()
      if (outBytes + b.length > max) {
        out.push(b.subarray(0, Math.max(0, max - outBytes)))
        outBytes = max
        truncated = true
        kill()
      } else {
        out.push(b)
        outBytes += b.length
      }
    })
    child.stderr.on('data', (b: Buffer) => {
      if (errBytes < max) {
        err.push(b.subarray(0, max - errBytes))
        errBytes += b.length
      }
    })
    child.on('error', (e) => {
      clearTimeout(timer)
      clearTimeout(watchdog)
      resolve({
        code: -1, signal: null, stdout: '', stderr: String(e), timedOut: false, truncated: false,
        ms: performance.now() - start
      })
    })
    child.on('close', (code, signal) => {
      clearTimeout(timer)
      clearTimeout(watchdog)
      resolve({
        code,
        signal,
        stdout: Buffer.concat(out).toString('utf8'),
        stderr: Buffer.concat(err).toString('utf8'),
        timedOut,
        truncated,
        ms: performance.now() - start
      })
    })
    // The child may exit before reading stdin (EPIPE); that's not our error to report.
    child.stdin.on('error', () => {})
    child.stdin.end(opts.stdin ?? '')
  })
}

/** Run async jobs with bounded parallelism, preserving order. */
export async function mapLimit<T, R>(items: T[], limit: number, fn: (t: T, i: number) => Promise<R>): Promise<R[]> {
  const results = new Array<R>(items.length)
  let next = 0
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (next < items.length) {
      const i = next++
      results[i] = await fn(items[i], i)
    }
  })
  await Promise.all(workers)
  return results
}
