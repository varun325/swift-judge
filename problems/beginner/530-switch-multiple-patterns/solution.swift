func classify(_ text: String) -> [String] {
    text.map { ch -> String in
        switch ch.lowercased() {
        case "a", "e", "i", "o", "u": return "vowel"
        case _ where ch.isNumber: return "digit"
        case " ": return "space"
        case _ where ch.isLetter: return "consonant"
        default: return "other"
        }
    }
}
