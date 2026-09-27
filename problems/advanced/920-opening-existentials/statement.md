`protocol Shape { associatedtype Measure: Numeric & CustomStringConvertible; var perimeter: Measure { get } }`. `Square` uses `Int`, `Circle` uses `Double`. Store shapes as `[any Shape]` and pass each to a **generic** `func report(_ s: some Shape) -> String` (`"<type>: <perimeter>"`) — Swift 5.7+ opens the existential automatically.

 Side `n > 0` → `Square(side: n)`, `n <= 0` → `Circle(radius: Double(-n))` with perimeter `2 × 3 × r` (use 3 for π to keep it exact).
