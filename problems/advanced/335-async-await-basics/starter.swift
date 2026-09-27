func fetchUser(_ id: Int) async -> String {
    try? await Task.sleep(for: .milliseconds(100))
    return "user\(id)"
}

func fetchAll(_ ids: [Int]) async -> [String] {
    var users: [String] = []
    for id in ids { users.append(await fetchUser(id)) }
    return users
}
