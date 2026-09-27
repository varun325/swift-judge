protocol Building {
    var kind: String { get }
    var rooms: Int { get }
    var cost: Int { get }
    var agent: String { get }
    func salesSummary() -> String
}

extension Building {
    func salesSummary() -> String { "\(kind) with \(rooms) rooms, $\(cost), sold by \(agent)" }
}

struct House: Building {
    let rooms: Int, cost: Int
    var kind: String { "House" }
    var agent: String { "Ana" }
}

struct Office: Building {
    let rooms: Int, cost: Int
    var kind: String { "Office" }
    var agent: String { "Bo" }
}

func listings(_ specs: [[Int]]) -> [String] {
    specs.map { s -> String in
        let b: any Building = s[0] == 0 ? House(rooms: s[1], cost: s[2]) : Office(rooms: s[1], cost: s[2])
        return b.salesSummary()
    }
}
