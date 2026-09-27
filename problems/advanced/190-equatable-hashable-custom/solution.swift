struct Email: Hashable {
    let raw: String

    private var normalized: String {
        let lower = raw.lowercased()
        guard let at = lower.firstIndex(of: "@") else { return lower }
        var local = lower[..<at]
        if let plus = local.firstIndex(of: "+") { local = local[..<plus] }
        return local.replacingOccurrences(of: ".", with: "") + lower[at...]
    }

    static func == (a: Email, b: Email) -> Bool { a.normalized == b.normalized }
    func hash(into hasher: inout Hasher) { hasher.combine(normalized) }
}

func uniqueEmails(_ raw: [String]) -> Int {
    Set(raw.map(Email.init)).count
}
