enum Planet: Int {
    case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
}

func planetNames(_ positions: [Int]) -> [String] {
    positions.map { Planet(rawValue: $0).map { "\($0)" } ?? "unknown" }
}
