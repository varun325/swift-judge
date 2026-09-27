func wordFrequency(_ text: String) -> [String: Int] {
    var counts: [String: Int] = [:]
    for word in text.lowercased().split(whereSeparator: { !$0.isLetter }) {
        counts[String(word), default: 0] += 1
    }
    return counts
}
