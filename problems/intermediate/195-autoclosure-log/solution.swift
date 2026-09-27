final class Log { var lines: [String] = [] }

func debugLog(_ message: @autoclosure () -> String, level: Int, into log: Log) {
    guard level >= 2 else { return }
    log.lines.append("LOG \(message())")
}

func loggingDemo(level: Int) -> [String] {
    let log = Log()
    func expensive(_ x: String) -> String {
        log.lines.append("computed \(x)")
        return "msg \(x)"
    }
    debugLog(expensive("A"), level: level, into: log)
    debugLog(expensive("B"), level: 3, into: log)
    return log.lines
}
