func sumOfNumbers(_ tokens: [String]) -> Int {
    tokens.compactMap { Int($0) }.reduce(0, +)
}
