`stride(from: 1, through: upTo, by: 1)` is simply empty when `upTo < 1`, whereas `1...upTo` would trap. `compactMap { Int($0) }` parses and drops anything that isn't a number.
