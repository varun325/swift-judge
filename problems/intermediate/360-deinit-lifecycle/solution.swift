final class Log { var lines: [String] = [] }

final class Tracked {
    let name: String
    let log: Log
    init(_ name: String, log: Log) {
        self.name = name
        self.log = log
        log.lines.append("init \(name)")
    }
    deinit { log.lines.append("deinit \(name)") }
}

func lifecycle(_ names: [String]) -> [String] {
    let log = Log()
    do {
        var items = names.map { Tracked($0, log: log) }
        if !items.isEmpty {
            items.removeFirst()
            log.lines.append("removed")
        }
    }
    log.lines.append("after scope")
    return log.lines
}
