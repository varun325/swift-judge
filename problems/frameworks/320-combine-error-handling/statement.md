Parse tokens as integers with `tryMap` (throw on a bad token). With `recovery`:
 - `"replace"` → `.replaceError(with: -1)` (the stream **ends** after the error)
 - `"catch"` → `.catch { _ in Just(0) }`
 - `"perItem"` → use `flatMap` so each token is parsed in its own inner publisher and errors are replaced per item, letting the outer stream continue

 Log values and a final `"done"`.
