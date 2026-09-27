func checkIdentities(_ snapshots: [[String]]) -> [String] {
    var problems: Set<String> = []
    var idForContent: [String: String] = [:]
    for (n, snapshot) in snapshots.enumerated() {
        var seen: Set<String> = []
        for item in snapshot {
            let parts = item.split(separator: ":", maxSplits: 1).map(String.init)
            guard parts.count == 2 else { continue }
            let (id, content) = (parts[0], parts[1])
            if !seen.insert(id).inserted { problems.insert("duplicate \(id) in snapshot \(n)") }
            if let previous = idForContent[content], previous != id { problems.insert("unstable \(content)") }
            idForContent[content] = id
        }
    }
    return problems.isEmpty ? ["ok"] : problems.sorted()
}
