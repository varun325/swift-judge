func leaderboard(_ entries: [[String]]) -> [String] {
    let rows = entries.map { (name: $0[0], points: Int($0[1])!, wins: Int($0[2])!) }
    return rows.sorted {
        (-$0.points, -$0.wins, $0.name) < (-$1.points, -$1.wins, $1.name)
    }.map(\.name)
}
