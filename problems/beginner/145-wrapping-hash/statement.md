Implement the classic djb2 string hash over the string's **UTF-8 bytes**: start with `5381`, then for each byte `hash = hash * 33 + byte`. The multiplication will overflow for longer strings — use the **wrapping** operators so it wraps around instead of crashing.

 ```swift
 djb2("")    // 5381
 djb2("a")   // 177670
 ```
