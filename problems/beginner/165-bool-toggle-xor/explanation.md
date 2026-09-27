Since `Bool` doesn't convert to `Int`, count with `filter { $0 }.count` (or `[a, b, c].count(where: \.self)` in Swift 6). For two flags, exactly-one is `a != b` — `!=` on `Bool` is XOR.
