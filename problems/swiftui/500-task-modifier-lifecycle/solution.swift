actor Log {
    private(set) var lines: [String] = []
    func add(_ s: String) { lines.append(s) }
}

@MainActor
final class TaskRunner {
    private var task: Task<Void, Never>?
    private var currentID: String?
    let log: Log
    init(log: Log) { self.log = log }

    func start(_ id: String) {
        task?.cancel()
        currentID = id
        let log = self.log
        task = Task {
            try? await Task.sleep(for: .milliseconds(20))
            if Task.isCancelled { await log.add("cancelled \(id)") } else { await log.add("loaded \(id)") }
        }
    }

    func appear(_ id: String) { start(id) }
    func change(_ id: String) { if id != currentID { start(id) } }
    func disappear() { task?.cancel(); task = nil; currentID = nil }
}

func taskLifecycle(_ events: [String]) async -> [String] {
    let log = Log()
    let runner = await TaskRunner(log: log)
    for e in events {
        let p = e.split(separator: " ", maxSplits: 1).map(String.init)
        switch p[0] {
        case "appear": await runner.appear(p.count > 1 ? p[1] : "")
        case "change": await runner.change(p.count > 1 ? p[1] : "")
        default: await runner.disappear()
        }
    }
    try? await Task.sleep(for: .milliseconds(80))
    return await log.lines.sorted()
}
