import RegexBuilder

func parseLogs(_ lines: [String]) -> [String] {
    let level = Reference(Substring.self)
    let message = Reference(Substring.self)
    let code = Reference(Int.self)
    let regex = Regex {
        "["
        Capture(as: level) { ChoiceOf { "INFO"; "WARN"; "ERROR" } }
        "] "
        Repeat(.digit, count: 4); "-"; Repeat(.digit, count: 2); "-"; Repeat(.digit, count: 2)
        " "
        Capture(as: message) { OneOrMore(.any, .reluctant) }
        " (code "
        TryCapture(as: code) { OneOrMore(.digit) } transform: { Int($0) }
        ")"
    }
    return lines.map { line in
        guard let m = line.wholeMatch(of: regex) else { return "skip" }
        return "\(m[level])|\(m[code])|\(m[message])"
    }
}
