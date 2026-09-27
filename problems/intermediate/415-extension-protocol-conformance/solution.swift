protocol Summarizable {
    var summary: String { get }
}

extension Int: Summarizable {
    var summary: String { "int(\(self))" }
}

extension String: Summarizable {
    var summary: String { "str(\(count))" }
}

extension Array: Summarizable where Element: Summarizable {
    var summary: String { "[" + map(\.summary).joined(separator: ",") + "]" }
}

func summaries(ints: [Int], words: [String], flags: [Bool]) -> [String] {
    [ints.summary, words.summary, flags.map { $0 ? 1 : 0 }.summary]
}
