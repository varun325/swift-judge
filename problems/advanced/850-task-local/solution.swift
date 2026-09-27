enum Trace {
    @TaskLocal static var requestID = "none"
}

func handle() async -> [String] {
    await withTaskGroup(of: String.self) { group in
        for step in ["db", "cache"] {
            group.addTask { "\(Trace.requestID):\(step)" }
        }
        var lines: [String] = []
        for await line in group { lines.append(line) }
        return lines
    }
}

func tracedRequests(_ ids: [String]) async -> [String] {
    var logs = ["\(Trace.requestID):outside"]
    for id in ids {
        logs += await Trace.$requestID.withValue(id) { await handle() }
    }
    return logs.sorted()
}
