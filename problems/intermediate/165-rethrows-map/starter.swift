extension Array {
    // func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T]
}

struct HasDigits: Error {}

func parse(_ word: String) throws -> String {
    if word.contains(where: \.isNumber) { throw HasDigits() }
    return word
}

func demo(_ words: [String]) -> [String] {
    return []
}
