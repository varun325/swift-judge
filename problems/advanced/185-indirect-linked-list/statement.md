`indirect enum List<T> { case empty; case node(T, List<T>) }`. Add `func prepending(_:)`, `var reversed: List`, and conform to `Sequence` (via `AnyIterator` or a custom iterator).

 Build the list by prepending each value in order, then return `[Array(list), Array(list.reversed), [list.reduce(0, +)]]`.
