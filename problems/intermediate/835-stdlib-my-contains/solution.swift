extension Sequence {
    func myContains(where predicate: (Element) throws -> Bool) rethrows -> Bool {
        for element in self where try predicate(element) { return true }
        return false
    }
}

extension Sequence where Element: Equatable {
    func myContains(_ element: Element) -> Bool {
        myContains { $0 == element }
    }
}

func containsDemo(_ words: [String], target: String, minLength: Int) -> [Bool] {
    [words.myContains(target), words.myContains { $0.count >= minLength }]
}
