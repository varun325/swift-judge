enum Field: String, CaseIterable {
    case username, email, password
}

extension Optional where Wrapped == Field {
    func next() -> Field? {
        guard let current = self else { return Field.allCases.first }
        let i = Field.allCases.firstIndex(of: current)!
        return i + 1 < Field.allCases.count ? Field.allCases[i + 1] : nil
    }

    func previous() -> Field? {
        guard let current = self, let i = Field.allCases.firstIndex(of: current), i > 0 else { return self }
        return Field.allCases[i - 1]
    }
}

func focusSequence(_ actions: [String]) -> [String] {
    var focused: Field? = nil
    return actions.map { action in
        let p = action.split(separator: " ").map(String.init)
        switch p[0] {
        case "submit": focused = focused.next()
        case "back": focused = focused.previous()
        case "tap": focused = p.count > 1 ? Field(rawValue: p[1]) ?? focused : focused
        default: focused = nil
        }
        return focused?.rawValue ?? "none"
    }
}
