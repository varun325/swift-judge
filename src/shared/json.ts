/**
 * JSON that round-trips 64-bit integers exactly. Swift `Int` goes up to 2^63-1, but
 * JavaScript numbers lose precision past 2^53, so unsafe integer literals become BigInt.
 */
type ReviverContext = { source?: string }
type JsonWithRaw = typeof JSON & { rawJSON?: (text: string) => unknown }

export function parseExact(text: string): unknown {
  return JSON.parse(text, function (_key, value: unknown, ctx?: ReviverContext) {
    if (typeof value === 'number' && Number.isInteger(value) && !Number.isSafeInteger(value) && ctx?.source && /^-?\d+$/.test(ctx.source)) {
      return BigInt(ctx.source)
    }
    return value
  } as Parameters<typeof JSON.parse>[1])
}

export function stringifyExact(value: unknown, space?: number): string {
  const raw = (JSON as JsonWithRaw).rawJSON
  return JSON.stringify(value, (_k, v: unknown) => (typeof v === 'bigint' ? (raw ? raw(v.toString()) : v.toString()) : v), space)
}
