extension Sequence {
    func myCompactMap<T>(_ transform: (Element) throws -> T?) rethrows -> [T] {
        var result: [T] = []
        for element in self {
            if let value = try transform(element) { result.append(value) }
        }
        return result
    }
}

func compactDemo(_ tokens: [String]) -> [Int] {
    tokens.myCompactMap { Int($0) }
}
