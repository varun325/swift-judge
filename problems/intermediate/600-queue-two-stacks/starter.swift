struct TwoStackQueue<Element> {
    mutating func enqueue(_ x: Element) {}
    mutating func dequeue() -> Element? { nil }
    var peek: Element? { nil }
    var count: Int { 0 }
}
