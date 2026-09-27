infix operator • : MultiplicationPrecedence

struct Vector2: Equatable {
    var x: Double, y: Double

    static func + (l: Vector2, r: Vector2) -> Vector2 { Vector2(x: l.x + r.x, y: l.y + r.y) }
    static func - (l: Vector2, r: Vector2) -> Vector2 { l + -r }
    static prefix func - (v: Vector2) -> Vector2 { Vector2(x: -v.x, y: -v.y) }
    static func * (v: Vector2, k: Double) -> Vector2 { Vector2(x: v.x * k, y: v.y * k) }
    static func * (k: Double, v: Vector2) -> Vector2 { v * k }
    static func += (l: inout Vector2, r: Vector2) { l = l + r }
    static func • (l: Vector2, r: Vector2) -> Double { l.x * r.x + l.y * r.y }
}

func vectorDemo(_ a: [Double], _ b: [Double]) -> [Double] {
    let u = Vector2(x: a[0], y: a[1]), v = Vector2(x: b[0], y: b[1])
    var c = u
    c += v
    return [(u + v).x, (u + v).y, (-u).x, (u * 2).y, (3 * v).x, u • v, u == v ? 1 : 0, c.x]
}
