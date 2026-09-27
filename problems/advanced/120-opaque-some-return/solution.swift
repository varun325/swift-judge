protocol Drawable { func draw() -> String }

struct Triangle: Drawable {
    let size: Int
    func draw() -> String { (1...max(size, 1)).map { String(repeating: "*", count: $0) }.joined(separator: "/") }
}

struct Flipped<D: Drawable>: Drawable {
    let base: D
    func draw() -> String { base.draw().split(separator: "/").reversed().joined(separator: "/") }
}

func makeTriangle(_ n: Int) -> some Drawable { Triangle(size: n) }
func flipped(_ d: some Drawable) -> some Drawable { Flipped(base: d) }

func drawAll(_ sizes: [Int]) -> [String] {
    sizes.map { flipped(makeTriangle($0)).draw() }
}
