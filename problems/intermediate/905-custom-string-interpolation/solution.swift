extension String.StringInterpolation {
    mutating func appendInterpolation(cents value: Int) {
        let sign = value < 0 ? "-" : ""
        let m = value.magnitude
        let fraction = m % 100
        appendLiteral("\(sign)$\(m / 100).\(fraction < 10 ? "0" : "")\(fraction)")
    }
}

func receipts(_ cents: [Int]) -> [String] {
    cents.map { "Total: \(cents: $0)" }
}
