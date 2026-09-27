An `inout` parameter is copied in, mutated, and written back when the function returns (copy-in copy-out). Idiomatic alternatives: `pair.swapAt(0, 1)` or `(pair[0], pair[1]) = (pair[1], pair[0])`.
