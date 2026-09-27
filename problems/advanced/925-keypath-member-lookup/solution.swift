@dynamicMemberLookup
struct Audited<Value> {
    private(set) var value: Value
    let names: [PartialKeyPath<Value>: String]
    private(set) var log: [String] = []

    init(_ value: Value, names: [PartialKeyPath<Value>: String]) {
        self.value = value
        self.names = names
    }

    subscript<T>(dynamicMember keyPath: WritableKeyPath<Value, T>) -> T {
        get { value[keyPath: keyPath] }
        set {
            log.append("set \(names[keyPath] ?? "?")")
            value[keyPath: keyPath] = newValue
        }
    }

    mutating func read<T>(_ keyPath: KeyPath<Value, T>) -> T {
        log.append("get \(names[keyPath] ?? "?")")
        return value[keyPath: keyPath]
    }
}

struct Settings {
    var volume = 5
    var theme = "light"
}

func auditDemo(_ edits: [String]) -> [String] {
    var audited = Audited(Settings(), names: [\Settings.volume: "volume", \Settings.theme: "theme"])
    for edit in edits {
        let p = edit.split(separator: "=").map(String.init)
        if p[0] == "volume", let v = Int(p[1]) { audited.volume = v }
        if p[0] == "theme" { audited.theme = p[1] }
    }
    let volume = audited.read(\.volume)
    let theme = audited.read(\.theme)
    return audited.log + ["volume=\(volume)", "theme=\(theme)"]
}
