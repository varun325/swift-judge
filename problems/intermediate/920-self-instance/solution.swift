struct Vector {
    var x: Int
    var y: Int

    init(x: Int, y: Int) {
        self.x = x
        self.y = y
    }

    func isEqual(to other: Vector) -> Bool {
        self.x == other.x && self.y == other.y
    }

    mutating func flip() {
        self = Vector(x: y, y: x)
    }
}

func vectors(_ pairs: [[Int]]) -> [String] {
    pairs.map { p in
        let original = Vector(x: p[0], y: p[1])
        var v = original
        v.flip()
        return "(\(v.x), \(v.y)) same:\(v.isEqual(to: original))"
    }
}
