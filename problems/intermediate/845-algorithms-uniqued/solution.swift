extension Sequence {
    func uniqued<K: Hashable>(on key: (Element) throws -> K) rethrows -> [Element] {
        var seen = Set<K>()
        var result: [Element] = []
        for element in self where seen.insert(try key(element)).inserted {
            result.append(element)
        }
        return result
    }
}

func uniqueByLength(_ words: [String]) -> [String] {
    words.uniqued { $0.count }
}
