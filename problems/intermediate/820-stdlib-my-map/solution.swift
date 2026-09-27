extension Sequence {
    func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T] {
        var result: [T] = []
        result.reserveCapacity(underestimatedCount)
        for element in self { result.append(try transform(element)) }
        return result
    }
}

func mapDemo(_ numbers: [Int]) -> [String] {
    numbers.myMap { "#\($0 * 2)" }
}
