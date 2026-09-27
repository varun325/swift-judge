Extend `Int` with:
 - `var isPrime: Bool`
 - `var digits: [Int]` (of the magnitude, most significant first; `0` → `[0]`)
 - `func times(_ action: () -> Void)`

 Return `"<n>: prime=<isPrime> digits=<digits> ticks=<count>"` where `ticks` counts calls made by `n.times { … }` (0 for negative `n`).
