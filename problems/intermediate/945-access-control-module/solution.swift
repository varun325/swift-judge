struct Safe {
    private var code = 42
}

extension Safe {
    func peek() -> Int { code }
}

struct Thief {
    func steal() -> Int { Safe().code }
}
