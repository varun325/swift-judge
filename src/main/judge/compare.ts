import { parseExact, stringifyExact } from '../../shared/json'
import type { Compare } from '../../shared/types'

function floatEps(mode: string): number | undefined {
  return mode.startsWith('float:') ? Number(mode.slice(6)) : undefined
}

function canonical(v: unknown): string {
  return stringifyExact(sortKeys(v))
}

function sortKeys(v: unknown): unknown {
  if (Array.isArray(v)) return v.map(sortKeys)
  if (v && typeof v === 'object') {
    return Object.fromEntries(
      Object.keys(v as object)
        .sort()
        .map((k) => [k, sortKeys((v as Record<string, unknown>)[k])])
    )
  }
  return v
}

function sortArrays(v: unknown, deep: boolean, top = true): unknown {
  if (Array.isArray(v)) {
    const inner = deep ? v.map((x) => sortArrays(x, deep, false)) : v
    return top || deep ? [...inner].sort((a, b) => (canonical(a) < canonical(b) ? -1 : canonical(a) > canonical(b) ? 1 : 0)) : inner
  }
  if (deep && v && typeof v === 'object') {
    return Object.fromEntries(Object.entries(v as object).map(([k, x]) => [k, sortArrays(x, deep, false)]))
  }
  return v
}

function deepEqual(a: unknown, b: unknown, eps?: number): boolean {
  if (typeof a === 'number' && typeof b === 'number') {
    return eps === undefined ? a === b : Math.abs(a - b) <= eps * Math.max(1, Math.abs(b))
  }
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false
    return a.every((x, i) => deepEqual(x, b[i], eps))
  }
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const ka = Object.keys(a).sort()
    const kb = Object.keys(b).sort()
    if (ka.length !== kb.length || ka.some((k, i) => k !== kb[i])) return false
    return ka.every((k) => deepEqual((a as Record<string, unknown>)[k], (b as Record<string, unknown>)[k], eps))
  }
  return a === b
}

function parseJson(s: string): { ok: true; value: unknown } | { ok: false } {
  try {
    return { ok: true, value: parseExact(s) }
  } catch {
    return { ok: false }
  }
}

/** Compare a JSON-encoded function result. `expected` may be a JSON string or an already-parsed value. */
export function compareJson(actual: string, expected: unknown, mode: Compare = 'json'): boolean {
  const a = parseJson(actual)
  if (!a.ok) return false
  const e = typeof expected === 'string' ? parseJson(expected) : { ok: true as const, value: expected }
  const ev = e.ok ? e.value : expected
  const eps = floatEps(mode)
  if (mode === 'json-unordered' || mode === 'json-unordered-deep') {
    const deep = mode === 'json-unordered-deep'
    return deepEqual(sortArrays(a.value, deep), sortArrays(ev, deep))
  }
  return deepEqual(a.value, ev, eps)
}

function normLines(s: string): string[] {
  const lines = s.replace(/\r\n/g, '\n').split('\n').map((l) => l.replace(/\s+$/, ''))
  while (lines.length && lines[lines.length - 1] === '') lines.pop()
  return lines
}

/** Compare program text output (stdio / predict). */
export function compareText(actual: string, expected: string, mode: Compare = 'trimmed'): boolean {
  if (mode === 'exact') return actual === expected
  const a = normLines(actual)
  const e = normLines(expected)
  if (mode === 'unorderedLines') return [...a].sort().join('\n') === [...e].sort().join('\n')
  const eps = floatEps(mode)
  if (eps !== undefined) {
    const ta = a.join(' ').split(/\s+/).filter(Boolean)
    const te = e.join(' ').split(/\s+/).filter(Boolean)
    if (ta.length !== te.length) return false
    return ta.every((t, i) => {
      const x = Number(t)
      const y = Number(te[i])
      if (!Number.isNaN(x) && !Number.isNaN(y)) return Math.abs(x - y) <= eps * Math.max(1, Math.abs(y))
      return t === te[i]
    })
  }
  return a.join('\n') === e.join('\n')
}

