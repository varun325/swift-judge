struct School {
    static let capacity = 3

    static func enroll(_ roster: inout [String], _ name: String) -> String {
        guard roster.count < capacity else { return "full" }
        roster.append(name)
        return "enrolled \(name) (\(roster.count)/\(capacity))"
    }
}

func schoolRoll(_ names: [String]) -> [String] {
    var roster: [String] = []
    return names.map { School.enroll(&roster, $0) }
}
