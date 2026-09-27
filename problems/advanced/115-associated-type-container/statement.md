Define `protocol Container { associatedtype Item; mutating func append(_ item: Item); var count: Int { get }; subscript(i: Int) -> Item { get } }`. Conform `IntBag` (stores `[Int]`) and a generic `Queue<T>`. Then write a generic function `func allItemsMatch<C1: Container, C2: Container>(_ a: C1, _ b: C2) -> Bool where C1.Item == C2.Item, C1.Item: Equatable`.

 Return `["<bag.count>", "<queue.count>", "\(allItemsMatch(bag, Queue(ints)))", "\(allItemsMatch(Queue(words), Queue(words.reversed())))"]` (the reversed comparison uses `Queue` of the reversed words).
