func maxProfit(_ prices: [Int]) -> Int {
    prices.reduce((minPrice: Int.max, best: 0)) { acc, price in
        (min(acc.minPrice, price), max(acc.best, price - min(acc.minPrice, price)))
    }.best
}
