func firstMatch(_ haystacks: [[Int]], target: Int) async -> Int {
    await withTaskGroup(of: Int?.self) { group in
        for (i, hay) in haystacks.enumerated() {
            group.addTask {
                for value in hay {
                    if Task.isCancelled { return nil }
                    if value == target { return i }
                }
                return nil
            }
        }
        var best: Int?
        for await found in group {
            if let found { best = min(best ?? found, found) }
        }
        return best ?? -1
    }
}
