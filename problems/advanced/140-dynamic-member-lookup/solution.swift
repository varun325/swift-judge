@dynamicMemberLookup
struct Config {
    let storage: [String: String]
    let prefix: String

    init(_ storage: [String: String], prefix: String = "") {
        self.storage = storage
        self.prefix = prefix
    }

    var value: String? { storage[prefix] }

    subscript(dynamicMember member: String) -> Config {
        Config(storage, prefix: prefix.isEmpty ? member : "\(prefix).\(member)")
    }

    func value(at path: String) -> String? {
        path.split(separator: ".").reduce(self) { $0[dynamicMember: String($1)] }.value
    }
}

func jsonPaths(_ json: [String: String], paths: [String]) -> [String] {
    let config = Config(json)
    precondition(config.db.port.value == json["db.port"])
    return paths.map { config.value(at: $0) ?? "missing" }
}
