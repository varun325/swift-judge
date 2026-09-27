struct Version: Comparable, CustomStringConvertible {
    let parts: [Int]
    let description: String

    init?(_ text: String) {
        let pieces = text.split(separator: ".", omittingEmptySubsequences: false)
        guard (1...3).contains(pieces.count) else { return nil }
        var nums: [Int] = []
        for piece in pieces {
            guard let n = Int(piece), n >= 0 else { return nil }
            nums.append(n)
        }
        parts = nums + Array(repeating: 0, count: 3 - nums.count)
        description = text
    }

    static func == (a: Version, b: Version) -> Bool { a.parts == b.parts }
    static func < (a: Version, b: Version) -> Bool { a.parts.lexicographicallyPrecedes(b.parts) }
}

func sortVersions(_ versions: [String]) -> [String] {
    var result: [Version] = []
    for v in versions.compactMap(Version.init).sorted() where result.last != v {
        result.append(v)
    }
    return result.map(\.description)
}
