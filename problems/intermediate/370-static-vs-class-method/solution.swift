class Shape {
    class func kind() -> String { "shape" }
    static func library() -> String { "geometry" }
}

final class Circle: Shape {
    override class func kind() -> String { "circle" }
}

func typeNames(_ kinds: [String]) -> [String] {
    kinds.map { k in
        let type: Shape.Type = k == "circle" ? Circle.self : Shape.self
        return "\(type.kind())/\(type.library())"
    }
}
