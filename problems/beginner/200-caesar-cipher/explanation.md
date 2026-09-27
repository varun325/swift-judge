`Character.asciiValue` is `UInt8?` — `nil` for non-ASCII. `((shift % 26) + 26) % 26` normalises negative shifts because Swift's `%` keeps the sign of the dividend (`-1 % 26 == -1`).
