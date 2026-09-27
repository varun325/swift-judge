struct Prefix { let text: String }

func ~= (pattern: Prefix, value: String) -> Bool { value.hasPrefix(pattern.text) }
func ~= (pattern: (String) -> Bool, value: String) -> Bool { pattern(value) }

func classifyAll(_ words: [String]) -> [String] {
    let isLong: (String) -> Bool = { $0.count > 8 }
    return words.map { word in
        switch word {
        case Prefix(text: "un"): "negation"
        case isLong: "long"
        case Prefix(text: "re"): "repeat"
        default: "plain"
        }
    }
}
