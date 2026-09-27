Declaring `: Hashable` is enough — the compiler synthesises `==` and `hash(into:)` from the stored properties because they're all Hashable. Sets and dictionary keys require it.
