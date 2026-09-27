Write `@propertyWrapper struct Clamped<Value: Comparable>` (initialised with `wrappedValue` and a `ClosedRange`) and `@propertyWrapper struct Trimmed` (trims whitespace, lowercases). Also give `Clamped` a **projected value** `$volume` that reports how many times a write was clamped.

 `struct Settings { @Clamped(0...100) var volume = 50; @Trimmed var username = "" }`. Apply each volume and each name, logging `"v=<volume>"` and `"u=<username>"`; finally log `"clamps=<$volume>"`.
