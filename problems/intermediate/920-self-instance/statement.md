`struct Vector { var x: Int; var y: Int }` with:
 - `init(x: Int, y: Int)` written by hand, using `self.x = x`
 - `func isEqual(to other: Vector) -> Bool` comparing `self` with `other`
 - `mutating func flip() { self = Vector(x: y, y: x) }` — assigning a whole new value to `self`

 For each pair create a vector, flip it, and return `"(x, y) same:<isEqual(to: original)>"`.
