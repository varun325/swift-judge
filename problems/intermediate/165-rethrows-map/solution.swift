extension Array {
    func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T] {
        var out: [T] = []
        out.reserveCapacity(count)
        for element in self { out.append(try transform(element)) }
        return out
    }
}

struct HasDigits: Error {}

func parse(_ word: String) throws -> String {
    if word.contains(where: \.isNumber) { throw HasDigits() }
    return word
}

func demo(_ words: [String]) -> [String] {
    var result = words.myMap { $0.uppercased() }
    result.append((try? words.myMap(parse)) != nil ? "parsed" : "rejected")
    return result
}
