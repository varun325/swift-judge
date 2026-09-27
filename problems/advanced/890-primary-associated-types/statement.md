Since Swift 5.7, protocols like `Collection` declare a **primary associated type**, so you can write `some Collection<Int>` and `any Sequence<Int>`.
 - `func evens(in values: some Collection<Int>) -> [Int]`
 - `func squares(_ values: [Int]) -> some Sequence<Int>` — return a **lazy** map (the caller only knows it's a sequence of Int)
 - `let sources: [any Sequence<Int>] = [values, values.reversed(), squares(values)]`

 Return `evens(in: values) + Array(squares(values)) + sources.map { $0.reduce(0, +) }`.
