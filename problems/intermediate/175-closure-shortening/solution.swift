func tNames(_ team: [String]) -> [String] {
    team
        .filter { $0.lowercased().hasPrefix("t") }
        .sorted { ($0.count, $0) < ($1.count, $1) }
}
