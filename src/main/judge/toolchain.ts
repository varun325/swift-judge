import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync, renameSync } from 'node:fs'
import { devNull, tmpdir } from 'node:os'
import { join } from 'node:path'
import { run } from './runner'
import { parseDiagnostics } from './diagnostics'
import type { Diagnostic } from '../../shared/types'

let swiftcPath: string | undefined

const isWindows = process.platform === 'win32'
/** Compiled programs need an .exe suffix on Windows. */
export const EXE_SUFFIX = isWindows ? '.exe' : ''

/**
 * macOS: ask xcrun (Xcode or Command Line Tools). Windows/Linux: `swiftc` on PATH — the
 * swift.org installer adds it on Windows (plus SDKROOT, which swiftc reads by itself).
 * SWIFTC overrides both.
 */
export function findSwiftc(): string {
  if (swiftcPath) return swiftcPath
  if (process.env.SWIFTC) return (swiftcPath = process.env.SWIFTC)
  if (process.platform === 'darwin') {
    try {
      return (swiftcPath = execFileSync('xcrun', ['--find', 'swiftc'], { encoding: 'utf8' }).trim())
    } catch {
      /* fall through to PATH */
    }
  }
  return (swiftcPath = isWindows ? 'swiftc.exe' : 'swiftc')
}

let sdkArgs: string[] | undefined

/** The toolchain swiftc (unlike the /usr/bin shim) needs the macOS SDK passed explicitly. */
function sdk(): string[] {
  if (sdkArgs) return sdkArgs
  if (process.platform !== 'darwin') return (sdkArgs = [])
  try {
    const path = execFileSync('xcrun', ['--sdk', 'macosx', '--show-sdk-path'], { encoding: 'utf8' }).trim()
    sdkArgs = path ? ['-sdk', path] : []
  } catch {
    sdkArgs = []
  }
  return sdkArgs
}

export function swiftVersion(): string {
  try {
    return execFileSync(findSwiftc(), ['--version'], { encoding: 'utf8' }).split('\n').find((l) => l.includes('Swift version')) ?? 'unknown'
  } catch (e) {
    return `swiftc not found: ${String(e)}`
  }
}

let cacheRoot = join(tmpdir(), 'swift-judge-cache')
export function setCacheRoot(dir: string): void {
  cacheRoot = dir
}
export function getCacheRoot(): string {
  return cacheRoot
}

export function sha(...parts: string[]): string {
  const h = createHash('sha256')
  for (const p of parts) h.update(p).update('\0')
  return h.digest('hex').slice(0, 32)
}

export interface CompileResult {
  ok: boolean
  binary?: string
  diagnostics: Diagnostic[]
  output: string
  ms: number
  cached: boolean
}

export interface SourceFile {
  name: string
  content: string
}

const COMPILE_TIMEOUT_MS = 60_000

/** Explains a missing toolchain instead of surfacing a raw `spawn ENOENT`. */
function missingToolchain(stderr: string): string | undefined {
  if (!/ENOENT/.test(stderr)) return undefined
  const how =
    process.platform === 'win32'
      ? 'Install Swift for Windows from https://www.swift.org/install/windows/ (it needs the Visual Studio Build Tools with the C++ workload), then restart Swift Judge.'
      : process.platform === 'darwin'
        ? 'Install Xcode or the Command Line Tools (xcode-select --install), then restart Swift Judge.'
        : 'Install Swift from https://www.swift.org/install/ and make sure swiftc is on your PATH, then restart Swift Judge.'
  return `Swift compiler not found (tried "${findSwiftc()}"). ${how} You can also point the SWIFTC environment variable at swiftc.`
}

/**
 * Compile a set of Swift files into an executable. Binaries are content-addressed,
 * so recompiling identical sources (reference solutions, re-submits) is free.
 */
export async function compile(files: SourceFile[], swiftVersionFlag: '5' | '6'): Promise<CompileResult> {
  const key = sha('v1', swiftVersionFlag, ...files.flatMap((f) => [f.name, f.content]))
  const binDir = join(cacheRoot, 'bin')
  mkdirSync(binDir, { recursive: true })
  const binary = join(binDir, key + EXE_SUFFIX)
  if (existsSync(binary)) {
    return { ok: true, binary, diagnostics: [], output: '', ms: 0, cached: true }
  }

  const work = mkdtempSync(join(tmpdir(), 'swj-'))
  try {
    for (const f of files) writeFileSync(join(work, f.name), f.content)
    const tmpOut = join(work, 'prog' + EXE_SUFFIX)
    const res = await run(
      findSwiftc(),
      [
        '-Onone',
        ...sdk(),
        '-swift-version', swiftVersionFlag,
        '-diagnostic-style=llvm',
        '-module-name', 'Solution',
        ...files.map((f) => f.name),
        '-o', tmpOut
      ],
      { cwd: work, timeoutMs: COMPILE_TIMEOUT_MS }
    )
    const missing = missingToolchain(res.stderr)
    if (missing) return { ok: false, diagnostics: [], output: missing, ms: res.ms, cached: false }
    const output = (res.stderr + res.stdout).trim()
    const diagnostics = parseDiagnostics(output)
    if (res.timedOut) {
      return { ok: false, diagnostics, output: output + '\n[compiler timed out]', ms: res.ms, cached: false }
    }
    if (res.code !== 0 || !existsSync(tmpOut)) {
      return { ok: false, diagnostics, output, ms: res.ms, cached: false }
    }
    renameSync(tmpOut, binary)
    return { ok: true, binary, diagnostics, output, ms: res.ms, cached: false }
  } finally {
    rmSync(work, { recursive: true, force: true })
  }
}

/**
 * Diagnostic mode: run the front end through SIL mandatory passes (not just -typecheck), so
 * definite-initialisation, exclusivity and unreachable-code diagnostics are reported too.
 */
export async function typecheck(file: SourceFile, swiftVersionFlag: '5' | '6'): Promise<{ diagnostics: Diagnostic[]; output: string; ms: number }> {
  const work = mkdtempSync(join(tmpdir(), 'swj-'))
  try {
    writeFileSync(join(work, file.name), file.content)
    const res = await run(
      findSwiftc(),
      ['-emit-sil', '-o', devNull, ...sdk(), '-swift-version', swiftVersionFlag, '-diagnostic-style=llvm', file.name],
      { cwd: work, timeoutMs: COMPILE_TIMEOUT_MS }
    )
    const missing = missingToolchain(res.stderr)
    if (missing) throw new Error(missing)
    const output = (res.stderr + res.stdout).trim()
    const diagnostics = parseDiagnostics(output)
    if (res.timedOut || (res.code !== 0 && !diagnostics.some((d) => d.severity === 'error'))) {
      throw new Error(`swiftc failed without a source diagnostic:\n${output || (res.timedOut ? 'timed out' : `exit ${res.code}`)}`)
    }
    return { diagnostics, output, ms: res.ms }
  } finally {
    rmSync(work, { recursive: true, force: true })
  }
}
