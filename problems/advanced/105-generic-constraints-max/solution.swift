func mostFrequent<T: Hashable & Comparable>(_ items: [T]) -> T? {
    let counts = items.reduce(into: [T: Int]()) { $0[$1, default: 0] += 1 }
    return counts.max { a, b in (a.value, b.key) < (b.value, a.key) }?.key
}

func modeDemo(ints: [Int], words: [String]) -> [String] {
    [mostFrequent(ints).map(String.init) ?? "none", mostFrequent(words) ?? "none"]
}
