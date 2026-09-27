extension Sequence {
    func myFlatMap<S: Sequence>(_ transform: (Element) throws -> S) rethrows -> [S.Element] {
        var result: [S.Element] = []
        for element in self { result.append(contentsOf: try transform(element)) }
        return result
    }
}

func flatDemo(_ sentences: [String]) -> [String] {
    sentences.myFlatMap { $0.split(separator: " ").map(String.init) }
}
