struct Fibonacci: Sequence {
    struct Iterator: IteratorProtocol {
        var a = 0, b = 1
        mutating func next() -> Int? {
            defer { (a, b) = (b, a &+ b) }
            return a
        }
    }
    func makeIterator() -> Iterator { Iterator() }
}

func fibDemo(limit: Int, take: Int) -> [[Int]] {
    [Array(Fibonacci().prefix(take)),
     Array(Fibonacci().lazy.filter { $0.isMultiple(of: 2) }.prefix(while: { $0 <= limit }))]
}
