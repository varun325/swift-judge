final class LRUCache {
    private final class Node {
        let key: Int
        var value: Int
        var prev: Node?
        var next: Node?
        init(_ key: Int, _ value: Int) { self.key = key; self.value = value }
    }

    private let capacity: Int
    private var map: [Int: Node] = [:]
    private let head = Node(0, 0)   // most recent after head
    private let tail = Node(0, 0)   // least recent before tail

    init(capacity: Int) {
        self.capacity = capacity
        head.next = tail
        tail.prev = head
    }

    deinit {
        // Break the doubly-linked chain so ARC can free every node.
        var node = head.next
        while let n = node { node = n.next; n.prev = nil; n.next = nil }
    }

    private func unlink(_ n: Node) {
        n.prev?.next = n.next
        n.next?.prev = n.prev
    }

    private func pushFront(_ n: Node) {
        n.next = head.next
        n.prev = head
        head.next?.prev = n
        head.next = n
    }

    func get(_ key: Int) -> Int {
        guard let n = map[key] else { return -1 }
        unlink(n)
        pushFront(n)
        return n.value
    }

    func put(_ key: Int, _ value: Int) {
        guard capacity > 0 else { return }
        if let n = map[key] {
            n.value = value
            unlink(n)
            pushFront(n)
            return
        }
        let n = Node(key, value)
        map[key] = n
        pushFront(n)
        if map.count > capacity, let lru = tail.prev, lru !== head {
            unlink(lru)
            map[lru.key] = nil
        }
    }
}
