func coinChange(_ coins: [Int], _ amount: Int) -> Int {
    var best: [Int?] = Array(repeating: nil, count: amount + 1)
    best[0] = 0
    guard amount > 0 else { return 0 }
    for value in 1...amount {
        best[value] = coins.compactMap { coin in
            coin <= value ? best[value - coin].map { $0 + 1 } : nil
        }.min()
    }
    return best[amount] ?? -1
}
