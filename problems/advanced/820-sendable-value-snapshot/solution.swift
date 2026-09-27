struct OrderSnapshot: Sendable {
    let id: Int
    let total: Int
}

func processOrders(_ totals: [Int]) async -> [String] {
    let snapshots = totals.enumerated().map { OrderSnapshot(id: $0.offset + 1, total: $0.element) }
    let results = await withTaskGroup(of: (Int, String).self) { group in
        for s in snapshots {
            group.addTask { (s.id, "#\(s.id): \(s.total * 8 / 100)") }
        }
        var collected: [(Int, String)] = []
        for await r in group { collected.append(r) }
        return collected
    }
    return results.sorted { $0.0 < $1.0 }.map(\.1)
}
