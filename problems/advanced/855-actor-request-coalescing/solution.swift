actor ImageCache {
    private var tasks: [String: Task<String, Never>] = [:]
    private(set) var downloads = 0

    func image(for key: String) async -> String {
        if let existing = tasks[key] { return await existing.value }
        let task = Task { await self.download(key) }
        tasks[key] = task
        return await task.value
    }

    private func download(_ key: String) async -> String {
        downloads += 1
        try? await Task.sleep(for: .milliseconds(30))
        return "img:\(key)"
    }
}

func coalesced(_ keys: [String]) async -> [String] {
    let cache = ImageCache()
    let results = await withTaskGroup(of: String.self) { group in
        for key in keys { group.addTask { await cache.image(for: key) } }
        var all: Set<String> = []
        for await r in group { all.insert(r) }
        return all
    }
    return results.sorted() + ["downloads \(await cache.downloads)"]
}
