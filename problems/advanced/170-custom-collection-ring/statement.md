Implement `struct RingBuffer<Element>: Collection` with fixed `capacity`: `mutating func append(_:)` overwrites the **oldest** element when full. Conform to `Collection` (`startIndex`, `endIndex`, `index(after:)`, `subscript(position:)`) so it iterates oldest → newest — then `map`, `first`, `count`, `reduce` and slicing come for free.

 The judge sends `{"capacity": n, "values": [...]}` and prints `[Array(buffer), [buffer.first ?? -1], [buffer.count], [buffer.reduce(0, +)], Array(buffer.dropFirst())]`.
