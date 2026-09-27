`actor Library` has a `let name` and a mutable `books: [String: Int]` (title → copies). Add:
 - `func checkout(_ title: String) -> Bool` (decrement if available)
 - `func add(_ title: String)`
 - `nonisolated var label: String { "Library \(name)" }` — readable **without** `await` because it only touches a `let`

 Ops: `add <t>`, `out <t>`. Return the label first (no await), then `"ok"`/`"unavailable"` per op, then the sorted `"t=n"` inventory.
