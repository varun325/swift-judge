func luckyNumbers(_ numbers: [Int]) -> [String] {
    numbers.filter { !$0.isMultiple(of: 2) }.sorted().map { "\($0) is a lucky number" }
}
