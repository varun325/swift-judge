`stride(from:to:by:)` produces the start index of each chunk and `map` turns each into a slice. `min` keeps the last range in bounds — slicing past `endIndex` traps.
