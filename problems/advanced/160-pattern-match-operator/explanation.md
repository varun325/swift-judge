An **expression pattern** in a `case` is checked with `pattern ~= value`. The standard library defines it for `Equatable` values and ranges; your overloads extend `switch` to any matching logic.
