func pickNumber(_ numbers: [Int]?, index: Int) -> Int {
    numbers.flatMap { $0.isEmpty ? nil : $0[abs(index) % $0.count] } ?? 100
}
