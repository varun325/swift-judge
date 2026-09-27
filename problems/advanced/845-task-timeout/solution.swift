struct TimeoutError: Error {}

func withTimeout<T: Sendable>(ms: Int, _ work: @escaping @Sendable () async throws -> T) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask { try await work() }
        group.addTask {
            try await Task.sleep(for: .milliseconds(ms))
            throw TimeoutError()
        }
        defer { group.cancelAll() }
        return try await group.next()!
    }
}

func withDeadlines(_ jobs: [[Int]]) async -> [String] {
    var out: [String] = []
    for job in jobs {
        let workMs = job[0]
        do {
            out.append(try await withTimeout(ms: job[1]) {
                try await Task.sleep(for: .milliseconds(workMs))
                return "done in \(workMs)"
            })
        } catch {
            out.append("timed out")
        }
    }
    return out
}
