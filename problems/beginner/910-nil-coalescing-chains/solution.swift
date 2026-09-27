func profileSummary(nickname: String?, name: String?, tags: [String]?) -> String {
    let display = nickname ?? name ?? "Anonymous"
    let count = tags?.count ?? 0
    let first = tags?.first?.uppercased() ?? "-"
    return "\(display) [\(count)] \(first)"
}
