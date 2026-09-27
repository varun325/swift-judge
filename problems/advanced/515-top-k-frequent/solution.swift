func topKFrequent(_ words: [String], _ k: Int) -> [String] {
    let counts = words.reduce(into: [String: Int]()) { $0[$1, default: 0] += 1 }
    return counts
        .sorted { ($1.value, $0.key) < ($0.value, $1.key) }
        .prefix(k)
        .map(\.key)
}
