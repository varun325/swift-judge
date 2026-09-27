`struct Vector2: Equatable { var x, y: Double }` with `+`, binary `-`, **prefix** `-`, `*` by a scalar (both orders), `+=`, and a custom infix operator `•` for the dot product (declare `infix operator • : MultiplicationPrecedence`).

 Return `[(a+b).x, (a+b).y, (-a).x, (a*2).y, (3*b).x, a•b, (a == b) ? 1 : 0]` and also compute `var c = a; c += b` and append `c.x`.
