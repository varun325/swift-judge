struct __Input: Decodable { let ops: [String]; let words: [String] }
func __run(_ __i: __Input) async throws -> [Bool?] {
    let trie = Trie()
    return zip(__i.ops, __i.words).map { op, word -> Bool? in
        switch op {
        case "insert": trie.insert(word); return nil
        case "search": return trie.search(word)
        default: return trie.startsWith(word)
        }
    }
}
