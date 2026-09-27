enum Priority: String, Comparable, CaseIterable {
    case low, medium, high, critical

    static func < (a: Priority, b: Priority) -> Bool {
        allCases.firstIndex(of: a)! < allCases.firstIndex(of: b)!
    }
}

func triage(_ tickets: [String]) -> [String] {
    tickets
        .compactMap { t -> (Priority, String)? in
            let p = t.split(separator: " ", maxSplits: 1).map(String.init)
            guard p.count == 2, let priority = Priority(rawValue: p[0]) else { return nil }
            return (priority, p[1])
        }
        .sorted { ($1.0, $0.1) < ($0.0, $1.1) }
        .map { "[\($0.0.rawValue.uppercased())] \($0.1)" }
}
