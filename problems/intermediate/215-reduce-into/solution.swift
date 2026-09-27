func lengthHistogram(_ words: [String]) -> [String: [String]] {
    words.reduce(into: [:]) { groups, word in
        groups[String(word.count), default: []].append(word)
    }
}
