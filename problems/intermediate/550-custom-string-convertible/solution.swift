struct Money: CustomStringConvertible, CustomDebugStringConvertible {
    let cents: Int

    var description: String {
        let sign = cents < 0 ? "-" : ""
        let abs = cents.magnitude
        let fraction = abs % 100
        return "\(sign)$\(abs / 100).\(fraction < 10 ? "0" : "")\(fraction)"
    }

    var debugDescription: String { "Money(cents: \(cents))" }
}

func describeMoney(_ cents: [Int]) -> [String] {
    cents.flatMap { c -> [String] in
        let money = Money(cents: c)
        return ["\(money)", String(reflecting: money)]
    }
}
