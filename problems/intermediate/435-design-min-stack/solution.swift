struct MinStack {
    private var items: [(value: Int, min: Int)] = []

    mutating func push(_ x: Int) {
        items.append((x, Swift.min(x, items.last?.min ?? x)))
    }

    mutating func pop() -> Int? {
        items.popLast()?.value
    }

    func top() -> Int? { items.last?.value }
    func min() -> Int? { items.last?.min }
}
