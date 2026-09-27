struct Pair<A, B> {
    let first: A
    let second: B
}

extension Pair: Equatable where A: Equatable, B: Equatable {}
extension Pair: Hashable where A: Hashable, B: Hashable {}
extension Pair: CustomStringConvertible {
    var description: String { "(\(first), \(second))" }
}

func pairDemo(_ a: [Int], _ b: [Int]) -> [String] {
    let pairs = zip(a, b).map { Pair(first: $0, second: $1) }
    let unique = Set(pairs).map(\.description).sorted()
    let same = pairs.first.flatMap { f in pairs.last.map { f == $0 } } ?? false
    return unique + ["\(same)"]
}
