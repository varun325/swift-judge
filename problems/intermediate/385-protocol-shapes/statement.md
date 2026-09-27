Define `protocol Shape { var name: String { get }; var area: Double { get }; func perimeter() -> Double }` and conform `Square(side)`, `Rect(w, h)` and `Circle(r)`.

 Specs: `[s]` → square, `[w, h]` → rect, `[-r]` (a negative single value) → circle of radius `r`. Store them in `[any Shape]` and return `"<name> a=<area> p=<perimeter>"` with both numbers formatted to **2 decimal places** (use `String(format: "%.2f", x)` from Foundation).
