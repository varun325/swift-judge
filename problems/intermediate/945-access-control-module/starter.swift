struct Safe {
    private var code = 42
}

extension Safe {
    func peek() -> Int { code }
}
