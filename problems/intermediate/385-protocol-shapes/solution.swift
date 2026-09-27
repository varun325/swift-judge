import Foundation

protocol Shape {
    var name: String { get }
    var area: Double { get }
    func perimeter() -> Double
}

struct Square: Shape {
    let side: Double
    var name: String { "square" }
    var area: Double { side * side }
    func perimeter() -> Double { 4 * side }
}

struct Rect: Shape {
    let w: Double, h: Double
    var name: String { "rect" }
    var area: Double { w * h }
    func perimeter() -> Double { 2 * (w + h) }
}

struct Circle: Shape {
    let r: Double
    var name: String { "circle" }
    var area: Double { .pi * r * r }
    func perimeter() -> Double { 2 * .pi * r }
}

func describeShapes(_ specs: [[Double]]) -> [String] {
    let shapes: [any Shape] = specs.map { s in
        if s.count == 2 { return Rect(w: s[0], h: s[1]) }
        return s[0] < 0 ? Circle(r: -s[0]) : Square(side: s[0])
    }
    return shapes.map { "\($0.name) a=\(String(format: "%.2f", $0.area)) p=\(String(format: "%.2f", $0.perimeter()))" }
}
