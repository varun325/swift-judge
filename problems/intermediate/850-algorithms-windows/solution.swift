extension Collection {
    func windows(ofCount k: Int) -> [SubSequence] {
        guard k > 0, k <= count else { return [] }
        var result: [SubSequence] = []
        var start = startIndex
        var end = index(startIndex, offsetBy: k)
        while true {
            result.append(self[start..<end])
            if end == endIndex { break }
            formIndex(after: &start)
            formIndex(after: &end)
        }
        return result
    }

    func adjacentPairs() -> [(Element, Element)] {
        Array(zip(self, dropFirst()))
    }
}

func movingStats(_ values: [Int], window: Int) -> [[Int]] {
    [values.windows(ofCount: window).map { $0.reduce(0, +) }, values.adjacentPairs().map { $1 - $0 }]
}
