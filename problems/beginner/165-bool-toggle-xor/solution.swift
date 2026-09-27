func exactlyOne(_ a: Bool, _ b: Bool, _ c: Bool) -> Bool {
    [a, b, c].filter { $0 }.count == 1
}
