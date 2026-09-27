func makeDiscount(code: String) -> (Int) -> Int {
    switch code {
    case "HALF": return { $0 / 2 }
    case "TENOFF": return { max(0, $0 - 10) }
    case "FREE": return { _ in 0 }
    default: return { $0 }
    }
}

func discounts(_ prices: [Int], codes: [String]) -> [Int] {
    zip(prices, codes).map { makeDiscount(code: $1)($0) }
}
