struct UserModel {
    let name: String
    let points: Int
    let isVerified: Bool
}

func topVerified(_ rows: [[String]]) -> [String] {
    rows
        .map { UserModel(name: $0[0], points: Int($0[1]) ?? 0, isVerified: $0[2] == "true") }
        .filter { $0.isVerified && $0.points >= 50 }
        .sorted { ($1.points, $0.name) < ($0.points, $1.name) }
        .map { "\($0.name) (\($0.points))" }
}
