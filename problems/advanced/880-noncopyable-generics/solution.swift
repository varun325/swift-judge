struct Ticket: ~Copyable {
    let id: String
}

struct Vault<Item: ~Copyable>: ~Copyable {
    private var item: Item?

    init() { item = nil }

    mutating func store(_ newItem: consuming Item) {
        item = consume newItem
    }

    mutating func take() -> Item? {
        item.take()
    }
}

func vaultDemo(_ secrets: [String]) -> [String] {
    var log: [String] = []
    for s in secrets {
        var vault = Vault<Ticket>()
        vault.store(Ticket(id: s))
        if let t = vault.take() { log.append("took \(t.id)") }
        log.append(vault.take() == nil ? "empty" : "still full")
    }
    return log
}
