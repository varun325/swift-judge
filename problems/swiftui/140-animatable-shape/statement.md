Swiftful's *Animate Custom Shapes with AnimatableData*: SwiftUI animates a shape by setting its `animatableData` to interpolated values each frame. Implement `struct RoundedCornerRect: Shape` with `var cornerRadius: Double` exposed through `var animatableData: Double { get set }`.

 Simulate an animation: for `t` in `0...steps` (linear), set `shape.animatableData = from + (to - from) * t / steps` and record where the path starts: the x-coordinate of its first `.move` point in a 100×100 rect (it equals the current corner radius). Return those x values rounded to 2 decimals.
