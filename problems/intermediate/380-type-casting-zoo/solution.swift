func castReport(_ items: [String]) -> [String] {
    let values: [Any] = items.map { token -> Any in
        if let i = Int(token) { return i }
        if let d = Double(token) { return d }
        if let b = Bool(token) { return b }
        return token
    }
    var lines = values.map { value -> String in
        switch value {
        case let i as Int: "int \(i)"
        case let d as Double: "double \(d)"
        case let b as Bool: "bool \(b)"
        case let s as String: "string \(s)"
        default: "unknown"
        }
    }
    lines.append("\(values.filter { $0 is String }.count)")
    return lines
}
