final class CopyCounter { var copies = 0 }

struct COWArray {
    private final class Storage {
        var items: [Int]
        init(_ items: [Int]) { self.items = items }
    }

    private var storage = Storage([])
    private let counter: CopyCounter

    init(counter: CopyCounter) { self.counter = counter }

    var items: [Int] { storage.items }

    mutating func append(_ x: Int) {
        if !isKnownUniquelyReferenced(&storage) {
            storage = Storage(storage.items)
            counter.copies += 1
        }
        storage.items.append(x)
    }
}
