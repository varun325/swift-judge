actor Library {
    let name: String
    private var books: [String: Int] = [:]

    init(name: String) { self.name = name }

    nonisolated var label: String { "Library \(name)" }

    func add(_ title: String) { books[title, default: 0] += 1 }

    func checkout(_ title: String) -> Bool {
        guard let n = books[title], n > 0 else { return false }
        books[title] = n - 1
        return true
    }

    func inventory() -> [String] { books.sorted { $0.key < $1.key }.map { "\($0.key)=\($0.value)" } }
}

func libraryDemo(_ ops: [String]) async -> [String] {
    let library = Library(name: "Central")
    var out = [library.label]
    for op in ops {
        let p = op.split(separator: " ", maxSplits: 1).map(String.init)
        if p[0] == "add" { await library.add(p[1]); out.append("ok") }
        else { out.append(await library.checkout(p[1]) ? "ok" : "unavailable") }
    }
    return out + (await library.inventory())
}
