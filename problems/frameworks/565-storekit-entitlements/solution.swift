enum Tier: Int, Comparable {
    case free, pro, lifetime
    static func < (a: Tier, b: Tier) -> Bool { a.rawValue < b.rawValue }
}

func entitlement(now: Int, transactions: [[String]]) -> [String] {
    let active = transactions.filter { t in
        guard t.count == 4, t[3] == "n" else { return false }
        return t[2] == "-" || (Int(t[2]) ?? 0) > now
    }
    let tier = active.map { t -> Tier in
        switch t[0] {
        case "lifetime": .lifetime
        case "pro.monthly", "pro.yearly": .pro
        default: .free
        }
    }.max() ?? .free
    let renew = active.compactMap { Int($0[2]) }.max()
    return ["\(tier)", active.map { $0[0] }.sorted().joined(separator: ","), renew.map { "renews \($0)" } ?? "no renewal"]
}
