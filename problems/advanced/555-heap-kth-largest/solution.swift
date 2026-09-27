struct Heap<Element> {
    private var items: [Element] = []
    private let areSorted: (Element, Element) -> Bool

    init(by areSorted: @escaping (Element, Element) -> Bool) { self.areSorted = areSorted }

    var count: Int { items.count }
    var peek: Element? { items.first }

    mutating func insert(_ x: Element) {
        items.append(x)
        var child = items.count - 1
        while child > 0 {
            let parent = (child - 1) / 2
            guard areSorted(items[child], items[parent]) else { break }
            items.swapAt(child, parent)
            child = parent
        }
    }

    mutating func popTop() -> Element? {
        guard !items.isEmpty else { return nil }
        items.swapAt(0, items.count - 1)
        let top = items.removeLast()
        var parent = 0
        while true {
            let l = 2 * parent + 1, r = l + 1
            var candidate = parent
            if l < items.count, areSorted(items[l], items[candidate]) { candidate = l }
            if r < items.count, areSorted(items[r], items[candidate]) { candidate = r }
            if candidate == parent { break }
            items.swapAt(parent, candidate)
            parent = candidate
        }
        return top
    }
}

func kthLargest(_ nums: [Int], _ k: Int) -> Int {
    var heap = Heap<Int>(by: <)
    for n in nums {
        heap.insert(n)
        if heap.count > k { _ = heap.popTop() }
    }
    return heap.peek!
}
