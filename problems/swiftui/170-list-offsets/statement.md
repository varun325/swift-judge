Swiftful's *Add, edit, move, and delete items in a List*. SwiftUI hands you an `IndexSet` for deletes and `(IndexSet, Int)` for moves; SwiftUI extends `Array` with `remove(atOffsets:)` and `move(fromOffsets:toOffset:)`.

 Edits: `del 0 2` (delete offsets 0 and 2), `move 3 0` (move offset 3 to destination 0), `move 0 2 4` (move offsets 0 and 2 to destination 4 — the destination is in terms of the **original** indices). Return the final array.
