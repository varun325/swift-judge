enum Planet: String, CaseIterable {
    case mercury, venus, earth, mars, jupiter, saturn, uranus, neptune

    var index: Int { Planet.allCases.firstIndex(of: self)! + 1 }
    var isInner: Bool { index <= 4 }
    static var giants: [Planet] { [.jupiter, .saturn, .uranus, .neptune] }
    static func named(_ name: String) -> Planet? { Planet(rawValue: name.lowercased()) }
}

func planetFacts(_ names: [String]) -> [String] {
    names.map { name in
        guard let p = Planet.named(name) else { return "unknown" }
        return "\(p.rawValue) #\(p.index) inner:\(p.isInner) giant:\(Planet.giants.contains(p))"
    }
}
