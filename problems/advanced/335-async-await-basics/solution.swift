func fetchUser(_ id: Int) async -> String {
    try? await Task.sleep(for: .milliseconds(100))
    return "user\(id)"
}

func fetchAll(_ ids: [Int]) async -> [String] {
    await withTaskGroup(of: (Int, String).self) { group in
        for (i, id) in ids.enumerated() {
            group.addTask { (i, await fetchUser(id)) }
        }
        var result = Array(repeating: "", count: ids.count)
        for await (i, user) in group { result[i] = user }
        return result
    }
}
