Declare `struct Loose { let flag: Bool; let value: Int64; let small: Bool }` and `struct Packed` with the **same fields reordered** to minimise padding. Return `[size, stride, alignment]` for `Loose`, `Packed`, `Int`, `Bool`, `String?` and a class reference `AnyObject` — using `MemoryLayout<T>`.

 Let the compiler tell you the numbers (the expected values come from the real toolchain).
