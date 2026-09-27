Write `struct Pair<A, B> { let first: A; let second: B }` and make it:
 - `Equatable` when `A: Equatable, B: Equatable`
 - `Hashable` when both are `Hashable`
 - `CustomStringConvertible` always: `"(<first>, <second>)"`

 Build pairs `Pair(a[i], b[i])` (zip), put them in a `Set` to deduplicate, and return the **sorted** descriptions of the unique pairs followed by `"<first pair == last pair>"` (or `"false"` if there are none).
