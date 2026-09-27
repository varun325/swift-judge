struct RingBuffer<Element>: Collection {
    private var storage: [Element] = []
    private var head = 0
    let capacity: Int

    init(capacity: Int) { self.capacity = capacity }

    mutating func append(_ element: Element) {
        guard capacity > 0 else { return }
        if storage.count < capacity {
            storage.append(element)
        } else {
            storage[head] = element
            head = (head + 1) % capacity
        }
    }

    var startIndex: Int { 0 }
    var endIndex: Int { storage.count }
    func index(after i: Int) -> Int { i + 1 }
    subscript(position: Int) -> Element { storage[(head + position) % storage.count] }
}
