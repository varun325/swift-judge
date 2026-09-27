indirect enum List<T>: Sequence {
    case empty
    case node(T, List<T>)

    func prepending(_ value: T) -> List<T> { .node(value, self) }

    var reversed: List<T> {
        reduce(List.empty) { $0.prepending($1) }
    }

    func makeIterator() -> AnyIterator<T> {
        var current = self
        return AnyIterator {
            guard case let .node(value, next) = current else { return nil }
            current = next
            return value
        }
    }
}

func listDemo(_ values: [Int]) -> [[Int]] {
    let list = values.reduce(List<Int>.empty) { $0.prepending($1) }
    return [Array(list), Array(list.reversed), [list.reduce(0, +)]]
}
