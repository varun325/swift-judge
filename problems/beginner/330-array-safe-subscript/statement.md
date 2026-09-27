Out-of-range subscripts **crash** in Swift. Add an extension so any `Collection` supports `items[safe: i]`, returning `nil` for an invalid index. Then implement `pick`, which returns `items[safe: i]` for each index.

 ```swift
 pick(["a", "b"], at: [0, 5, -1, 1])  // ["a", nil, nil, "b"]
 ```
