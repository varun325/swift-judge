struct TwoStackQueue<Element> {
    private var inbox: [Element] = []
    private var outbox: [Element] = []

    mutating func enqueue(_ x: Element) { inbox.append(x) }

    mutating func dequeue() -> Element? {
        if outbox.isEmpty {
            outbox = inbox.reversed()
            inbox.removeAll()
        }
        return outbox.popLast()
    }

    var peek: Element? { outbox.last ?? inbox.first }
    var count: Int { inbox.count + outbox.count }
}
