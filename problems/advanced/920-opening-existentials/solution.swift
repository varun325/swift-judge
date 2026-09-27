protocol Shape {
    associatedtype Measure: Numeric & CustomStringConvertible
    var perimeter: Measure { get }
}

struct Square: Shape {
    let side: Int
    var perimeter: Int { 4 * side }
}

struct Circle: Shape {
    let radius: Double
    var perimeter: Double { 2 * 3 * radius }
}

func report(_ s: some Shape) -> String {
    "\(type(of: s)): \(s.perimeter)"
}

func describeShapes(_ sides: [Int]) -> [String] {
    let shapes: [any Shape] = sides.map { $0 > 0 ? Square(side: $0) as any Shape : Circle(radius: Double(-$0)) }
    return shapes.map { report($0) }
}
