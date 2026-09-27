Set `var x = start`. Create `let byRef = { x }` and `let bySnapshot = { [x] in x }`. Then `x += 5` and return `[byRef(), bySnapshot()]`.
