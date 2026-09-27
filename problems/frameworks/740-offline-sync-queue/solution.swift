enum Mutation: CustomStringConvertible {
    case create(String)
    case rename(from: String, to: String)
    case delete(String)
    var description: String {
        switch self {
        case .create(let n): "create \(n)"
        case let .rename(a, b): "rename \(a)->\(b)"
        case .delete(let n): "delete \(n)"
        }
    }
}

func coalesce(_ queue: [Mutation]) -> [Mutation] {
    var result: [Mutation] = []
    for m in queue {
        if case .delete(let name) = m, let i = result.lastIndex(where: { if case .create(name) = $0 { return true }; return false }) {
            result.remove(at: i)
            continue
        }
        result.append(m)
    }
    return result
}

func syncQueue(_ events: [String]) -> [String] {
    var online = true
    var pending: [Mutation] = []
    var server: Set<String> = []
    var log: [String] = []

    func flush() {
        for m in coalesce(pending) {
            switch m {
            case .create(let n): server.insert(n); log.append("sent \(m)")
            case let .rename(a, b):
                if server.remove(a) != nil { server.insert(b); log.append("sent \(m)") } else { log.append("dropped \(m)") }
            case .delete(let n):
                if server.remove(n) != nil { log.append("sent \(m)") } else { log.append("dropped \(m)") }
            }
        }
        pending = []
    }

    for e in events {
        let p = e.split(separator: " ").map(String.init)
        switch (p.first ?? "", p.count) {
        case ("create", 2): pending.append(.create(p[1]))
        case ("rename", 3): pending.append(.rename(from: p[1], to: p[2]))
        case ("delete", 2): pending.append(.delete(p[1]))
        case ("offline", 1): online = false
        case ("online", 1): online = true
        case ("status", 1): log.append("server: \(server.sorted().joined(separator: ","))")
        default: break
        }
        if online { flush() }
    }
    return log
}
