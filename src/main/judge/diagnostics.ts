import type { Diagnostic } from '../../shared/types'

const LINE = /^(.*?):(\d+):(\d+): (error|warning|note): (.*)$/

export function parseDiagnostics(output: string): Diagnostic[] {
  const diags: Diagnostic[] = []
  for (const raw of output.split('\n')) {
    const m = LINE.exec(raw.trim())
    if (!m) continue
    diags.push({
      file: m[1].split(/[\\/]/).pop() ?? m[1],
      line: Number(m[2]),
      column: Number(m[3]),
      severity: m[4] as Diagnostic['severity'],
      message: m[5]
    })
  }
  return diags
}

/** Strip temp-directory prefixes (POSIX or Windows, spaces allowed) from diagnostic lines. */
export function stripPaths(output: string): string {
  return output
    .split('\n')
    .map((l) => l.replace(/^.*?[\\/]([^\\/:]+\.swift)(?=:\d+:\d+:)/, '$1'))
    .join('\n')
}

/**
 * Make compiler output readable for the learner: strip temp-dir paths, and explain
 * errors that land in the judge's generated driver (usually a signature mismatch).
 */
export function presentCompilerOutput(output: string, userFile: string): string {
  return stripPaths(output)
    .split('\n')
    .map((l) =>
      l.startsWith('main.swift:') && userFile !== 'main.swift'
        ? `[judge driver] ${l}\n  ↳ the judge calls your function with the signature shown in the problem — check its name, labels and types`
        : l
    )
    .join('\n')
}
