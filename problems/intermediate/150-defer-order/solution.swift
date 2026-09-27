final class Log { var lines: [String] = [] }

func open(_ steps: ArraySlice<String>, _ log: Log) {
    guard let name = steps.first else { return }
    if name == "fail" {
        log.lines.append("failing")
        return
    }
    log.lines.append("open \(name)")
    defer { log.lines.append("close \(name)") }
    open(steps.dropFirst(), log)
}

func runSteps(_ steps: [String]) -> [String] {
    let log = Log()
    open(steps[...], log)
    return log.lines
}
