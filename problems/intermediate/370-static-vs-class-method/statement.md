`class Shape` has `class func kind() -> String { "shape" }` and `static func library() -> String { "geometry" }`. `final class Circle: Shape` **overrides** `kind()` to return `"circle"`. (Try overriding `library()` — you can't.)

 For each input (`"shape"` / `"circle"`), pick the **metatype** (`Shape.self` or `Circle.self` stored as `Shape.Type`) and return `"<kind()>/<library()>"`.
