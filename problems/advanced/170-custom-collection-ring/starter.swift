struct RingBuffer<Element>: Collection {
    init(capacity: Int) {}
    mutating func append(_ element: Element) {}

    var startIndex: Int { 0 }
    var endIndex: Int { 0 }
    func index(after i: Int) -> Int { i + 1 }
    subscript(position: Int) -> Element { fatalError() }
}
