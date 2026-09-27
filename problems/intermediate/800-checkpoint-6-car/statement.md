Checkpoint 6: create `struct Car` with a constant `model`, a constant `seats`, a constant `maxGears` and a **`private(set)`** current `gear` starting at 1, plus `mutating func changeGear(by delta: Int) -> Bool` that refuses to go below 1 or above `maxGears`.

 Apply each delta and log `"gear <n>"` or `"refused at <n>"`.
