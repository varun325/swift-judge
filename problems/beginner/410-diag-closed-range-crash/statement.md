Some mistakes are caught at compile time, some only at runtime. Here's one the compiler *can* catch: declare a constant **of type `Range<Int>`** and try to initialise it with a *closed* range literal, `0...5`.

 You pass when the compiler reports a type mismatch mentioning `ClosedRange`.
