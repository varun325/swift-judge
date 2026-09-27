final class Node {
    let value: Int
    var next: Node?
    init(_ value: Int) { self.value = value }
}

func hasCycle(_ values: [Int], loopTo: Int) -> [String] {
    let nodes = values.map(Node.init)
    for (a, b) in zip(nodes, nodes.dropFirst()) { a.next = b }
    if loopTo >= 0, loopTo < nodes.count { nodes.last?.next = nodes[loopTo] }
    defer { nodes.last?.next = nil }   // break the strong reference cycle so ARC can free the nodes

    var slow = nodes.first, fast = nodes.first
    while let f = fast?.next?.next, let s = slow?.next {
        slow = s
        fast = f
        if s === f {
            var start = nodes.first
            var meet: Node? = s
            while start !== meet { start = start?.next; meet = meet?.next }
            return ["cycle at \(nodes.firstIndex { $0 === start } ?? -1)"]
        }
    }
    return ["no cycle"]
}
