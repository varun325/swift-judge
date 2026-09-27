Make values callable like functions:
 - `struct Polynomial { let coefficients: [Int]; func callAsFunction(_ x: Int) -> Int }` — `p(2)` evaluates it (Horner's method, coefficients from highest power)
 - `@dynamicCallable struct Joiner { let separator: String; func dynamicallyCall(withArguments args: [String]) -> String }` — `j("a", "b")`

 For `p = Polynomial(coefficients: [2, 0, 1])` (2x² + 1) return `p(v)` for each value, then `Joiner(separator: "-")("x", "y", "z")`.
