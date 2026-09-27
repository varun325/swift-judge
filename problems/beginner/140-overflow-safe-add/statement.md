Plain `a + b` **crashes** on overflow. Return the sum, or `nil` if it would overflow `Int`.

 ```swift
 safeAdd(2, 3)            // 5
 safeAdd(Int.max, 1)      // nil
 safeAdd(Int.min, -1)     // nil
 ```
