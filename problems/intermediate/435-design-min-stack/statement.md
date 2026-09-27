Implement `struct MinStack` with `mutating func push(_ x: Int)`, `mutating func pop() -> Int?`, `func top() -> Int?` and `func min() -> Int?` — all **O(1)**.

 The judge drives it LeetCode-style from a list of operations and prints each result (`nil` shows as `null`):
 ```
 ops:  push push push min pop min top
 args: [-2] [0]  [-3]  []  []  []  []
 out:  null null null -3  -3  -2  0
 ```
