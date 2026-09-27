Write `func average(_ numbers: Double...) -> Double?` (nil for no numbers). Variadic parameters can't receive an existing array, so also write `func average(of numbers: [Double]) -> Double?` and have the variadic one call it. `averages` returns `average(of:)` for each group.

 Bonus: `averages` must call the variadic version at least once — e.g. `average(1, 2, 3)` — to check it compiles.
