protocol Scorer {
    associatedtype Item
    func score(_ item: Item) -> Int
}

extension Scorer {
    func total<S: Sequence>(_ items: S) -> Int where S.Element == Item {
        items.reduce(0) { $0 + score($1) }
    }
}

struct LengthScorer: Scorer {
    func score(_ item: String) -> Int { item.count }
}

struct ParityScorer: Scorer {
    func score(_ item: Int) -> Int { item.isMultiple(of: 2) ? 2 : 1 }
}

func scoreAll(_ ints: [Int], _ words: [String]) -> [Int] {
    [ParityScorer().total(ints), LengthScorer().total(words)]
}
