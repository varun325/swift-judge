import type { Signature } from '../../shared/types'

/** Unit separator: can't appear in normal program output, so result lines are unambiguous. */
export const MARK = '\u001F'
export const MARK_RE = /\u001FJUDGE\u001F(\d+)\u001F([\d.]+)\u001F(.*)\n?/g

/**
 * The part of the driver shared by generated and hand-written harnesses.
 * Contract for a custom harness.swift: define
 *   struct __Input: Swift.Decodable { ... }
 *   func __run(_ __i: __Input) async throws -> some Encodable
 */
const DRIVER_LOOP = `
struct __Null: Swift.Encodable {
    func encode(to e: any Swift.Encoder) throws { var c = e.singleValueContainer(); try c.encodeNil() }
}
func __errJSON(_ error: any Swift.Error) -> Swift.String {
    let data = (try? Foundation.JSONEncoder().encode(["$error": Swift.String(describing: error)])) ?? Foundation.Data()
    return Swift.String(decoding: data, as: Swift.UTF8.self)
}
let __data = Foundation.FileHandle.standardInput.readDataToEndOfFile()
var __inputs: [__Input] = []
do {
    __inputs = try Foundation.JSONDecoder().decode([__Input].self, from: __data)
} catch {
    Foundation.FileHandle.standardError.write(Foundation.Data("JUDGE_INPUT_ERROR: \\(error)\\n".utf8))
}
let __enc = Foundation.JSONEncoder()
__enc.outputFormatting = [.sortedKeys, .withoutEscapingSlashes]
for (__k, __in) in __inputs.enumerated() {
    let __t0 = Dispatch.DispatchTime.now().uptimeNanoseconds
    var __json: Swift.String
    do {
        let __r = try await __run(__in)
        __json = Swift.String(decoding: try __enc.encode(__r), as: Swift.UTF8.self)
    } catch {
        __json = __errJSON(error)
    }
    let __ms = Swift.Double(Dispatch.DispatchTime.now().uptimeNanoseconds - __t0) / 1e6
    Swift.print("\\u{1F}JUDGE\\u{1F}\\(__k)\\u{1F}\\(__ms)\\u{1F}\\(__json)")
    // Flush after every case so finished results survive a crash in a later case and the
    // judge's progress watchdog sees them immediately (user print()s share the same buffer,
    // so ordering is preserved).
    _ = fflush(nil)
}
`

// Every name the driver uses is module-qualified, so user types (a custom `FileHandle`,
// `Data`, `Log`…) can't shadow them. The C library module differs per platform.
const PRELUDE = `import Foundation
import Dispatch
#if canImport(Darwin)
import Darwin
_ = setvbuf(stdout, nil, _IONBF, 0)  // unbuffered: even a crashing case's prints are kept
#elseif canImport(Glibc)
import Glibc
_ = setvbuf(stdout, nil, _IONBF, 0)
#elseif canImport(ucrt)
import ucrt  // Windows: stdout is a C macro Swift can't import; rely on the per-case fflush
#endif
`

function callArgs(sig: Signature): string {
  return sig.params
    .map((p) => {
      const value = p.inout ? `&__p_${p.name}` : `__i.${p.name}`
      const label = p.label ?? p.name
      return label === '_' ? value : `${label}: ${value}`
    })
    .join(', ')
}

/** Generate the driver main.swift for a signature-described function problem. */
export function generateDriver(sig: Signature): string {
  const fields = sig.params.map((p) => `    let ${p.name}: ${p.type}`).join('\n')
  const inouts = sig.params.filter((p) => p.inout)
  const prefix = `${sig.throws ? 'try ' : ''}${sig.async ? 'await ' : ''}`
  const call = `${prefix}${sig.name}(${callArgs(sig)})`
  const isVoid = sig.returns === 'Void' || sig.returns === '()'

  let body: string
  let ret: string
  const copies = inouts.map((p) => `    var __p_${p.name} = __i.${p.name}`).join('\n')
  if (isVoid && inouts.length === 1) {
    ret = inouts[0].type
    body = `${copies}\n    ${call}\n    return __p_${inouts[0].name}`
  } else if (isVoid) {
    ret = '__Null'
    body = `${copies}\n    ${call}\n    return __Null()`
  } else {
    ret = sig.returns
    body = `${copies}\n    let __r: ${sig.returns} = ${call}\n    return __r`
  }

  return `${PRELUDE}
struct __Input: Swift.Decodable {
${fields}
}
func __run(_ __i: __Input) async throws -> ${ret} {
${body}
}
${DRIVER_LOOP}`
}

/** Wrap a problem's hand-written harness.swift with the shared driver loop. */
export function wrapCustomHarness(harness: string): string {
  return `${PRELUDE}\n${harness}\n${DRIVER_LOOP}`
}

export interface ParsedCase {
  index: number
  json: string
  ms: number
  stdout: string
}

/** Split driver output into per-test results; also returns output after the last marker. */
export function parseDriverOutput(stdout: string): { cases: ParsedCase[]; trailing: string } {
  const cases: ParsedCase[] = []
  let last = 0
  for (const m of stdout.matchAll(MARK_RE)) {
    cases.push({ index: Number(m[1]), ms: Number(m[2]), json: m[3], stdout: stdout.slice(last, m.index) })
    last = (m.index ?? 0) + m[0].length
  }
  return { cases, trailing: stdout.slice(last) }
}
