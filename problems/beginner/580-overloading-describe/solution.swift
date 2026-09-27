func describe(_ value: Int) -> String { "int \(value)" }
func describe(_ value: String) -> String { "string '\(value)' (\(value.count))" }
func describe(_ value: Bool) -> String { "bool \(value ? "yes" : "no")" }

func describeAll(ints: [Int], words: [String], flags: [Bool]) -> [String] {
    ints.map(describe) + words.map(describe) + flags.map(describe)
}
