extension Collection {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

func pick(_ items: [String], at indices: [Int]) -> [String?] {
    indices.map { items[safe: $0] }
}
