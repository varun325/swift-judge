protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}

struct IntBag: Container {
    private var items: [Int] = []
    mutating func append(_ item: Int) { items.append(item) }
    var count: Int { items.count }
    subscript(i: Int) -> Int { items[i] }
}

struct Queue<T>: Container {
    private var items: [T] = []
    init(_ items: [T] = []) { self.items = items }
    mutating func append(_ item: T) { items.append(item) }
    var count: Int { items.count }
    subscript(i: Int) -> T { items[i] }
}

func allItemsMatch<C1: Container, C2: Container>(_ a: C1, _ b: C2) -> Bool
where C1.Item == C2.Item, C1.Item: Equatable {
    guard a.count == b.count else { return false }
    return (0..<a.count).allSatisfy { a[$0] == b[$0] }
}

func containerDemo(_ ints: [Int], _ words: [String]) -> [String] {
    var bag = IntBag()
    ints.forEach { bag.append($0) }
    let queue = Queue(words)
    return ["\(bag.count)", "\(queue.count)", "\(allItemsMatch(bag, Queue(ints)))", "\(allItemsMatch(queue, Queue(Array(words.reversed()))))"]
}
