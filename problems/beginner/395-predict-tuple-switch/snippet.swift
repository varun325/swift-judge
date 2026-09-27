let points = [(0, 0), (3, 0), (0, -2), (2, 2), (-1, 5)]
for p in points {
    switch p {
    case (0, 0):
        print("origin")
    case (_, 0):
        print("x-axis at \(p.0)")
    case (0, let y):
        print("y-axis at \(y)")
    case let (x, y) where x == y:
        print("diagonal \(x)")
    case (-2...2, _):
        print("near")
    default:
        print("far")
    }
}
