Build `struct COWArray` that stores its elements in a private `final class Storage { var items: [Int] }` and only **copies the storage when mutated while shared**, using `isKnownUniquelyReferenced(&storage)`. Count copies in a `static`-free way: each `Storage` records `copies` in a shared counter object you pass in.

 Required API: `init(counter:)`, `mutating func append(_:)`, `var items: [Int]`.

 The judge runs: `var a = COWArray(...)`, appends `values`; `var b = a` (no copy yet); appends `extra` to `b`; appends 1 more to `b` (still no extra copy); returns `[a.items, b.items, [counter.copies]]`.
