final class Trie {
    private final class Node {
        var children: [Character: Node] = [:]
        var isEnd = false
    }

    private let root = Node()

    func insert(_ word: String) {
        var node = root
        for ch in word {
            if let next = node.children[ch] {
                node = next
            } else {
                let next = Node()
                node.children[ch] = next
                node = next
            }
        }
        node.isEnd = true
    }

    private func find(_ prefix: String) -> Node? {
        var node = root
        for ch in prefix {
            guard let next = node.children[ch] else { return nil }
            node = next
        }
        return node
    }

    func search(_ word: String) -> Bool { find(word)?.isEnd ?? false }
    func startsWith(_ prefix: String) -> Bool { find(prefix) != nil }
}
