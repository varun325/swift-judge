func describeAll<each T>(_ value: repeat each T) -> [String] {
    var out: [String] = []
    for v in repeat each value {
        out.append(String(describing: v))
    }
    return out
}

func allNonNil<each T>(_ value: repeat (each T)?) -> Bool {
    for v in repeat each value {
        if v == nil { return false }
    }
    return true
}

func packsDemo() -> [String] {
    describeAll(1, "two", 3.0, true) + ["\(allNonNil(1, "a", 2.5))", "\(allNonNil(1, nil as String?))"]
}
