final class Log { var lines: [String] = [] }

struct FileHandle: ~Copyable {
    let name: String
    let log: Log
    private var closed = false

    init(name: String, log: Log) {
        self.name = name
        self.log = log
    }

    mutating func write(_ text: String) { log.lines.append("write \(text)") }

    consuming func close() {
        log.lines.append("close \(name)")
        closed = true
    }

    deinit {
        if !closed { log.lines.append("auto-close \(name)") }
    }
}

func inspect(_ h: borrowing FileHandle) -> String { "inspect \(h.name)" }

func ownershipDemo(_ writes: [String], closeEarly: Bool) -> [String] {
    let log = Log()
    do {
        var handle = FileHandle(name: "data.txt", log: log)
        log.lines.append(inspect(handle))
        for w in writes { handle.write(w) }
        if closeEarly { handle.close() }
    }
    log.lines.append("done")
    return log.lines
}
