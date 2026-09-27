extension Sequence {
    func chunked<K: Equatable>(on key: (Element) throws -> K) rethrows -> [[Element]] {
        var chunks: [[Element]] = []
        var lastKey: K?
        for element in self {
            let k = try key(element)
            if let lastKey, lastKey == k {
                chunks[chunks.count - 1].append(element)
            } else {
                chunks.append([element])
            }
            lastKey = k
        }
        return chunks
    }
}

func groupRuns(_ words: [String]) -> [[String]] {
    words.chunked { $0.first.map { String($0).lowercased() } ?? "" }
}
