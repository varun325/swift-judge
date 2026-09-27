func zipWith(_ a: [Int], _ b: [Int], _ f: (Int, Int) -> Int) -> [Int] {
    zip(a, b).map(f)
}

func combine(_ a: [Int], _ b: [Int], op: String) -> [Int] {
    switch op {
    case "add": zipWith(a, b, +)
    case "max": zipWith(a, b, max)
    default:
        zipWith(a, b) { base, exponent in
            (0..<max(0, exponent)).reduce(1) { acc, _ in acc * base }
        }
    }
}
