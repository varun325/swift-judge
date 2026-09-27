Swift never converts numeric types implicitly — `Int * Double` doesn't compile. `Double(celsius)` converts once, and the literals `9`, `5`, `32` are then inferred as `Double`.
