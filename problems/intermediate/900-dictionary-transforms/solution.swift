func settings(_ raw: [String: String]) -> [String: Int] {
    raw.compactMapValues { Int($0) }
        .mapValues { $0 * 2 }
        .filter { !$0.key.hasPrefix("_") }
}
