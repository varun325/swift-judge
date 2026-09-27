Build `@dynamicMemberLookup struct Audited<Value>` that wraps a value and records reads/writes. Implement `subscript<T>(dynamicMember keyPath: WritableKeyPath<Value, T>) -> T { get set }` that appends `"get <name>"`/`"set <name>"` to a log — use `"\(keyPath)"`? No — take names from a provided `[PartialKeyPath<Value>: String]`.

 Wrap `struct Settings { var volume = 5; var theme = "light" }`; apply edits `volume=<n>` / `theme=<t>` through `audited.volume = …` syntax, read both at the end, and return the log followed by the final values.
