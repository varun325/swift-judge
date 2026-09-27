struct Matrix {
    let rows: Int, cols: Int
    private(set) var grid: [Int]

    init(rows: Int, cols: Int) {
        self.rows = rows
        self.cols = cols
        grid = Array(repeating: 0, count: rows * cols)
    }

    subscript(row: Int, col: Int) -> Int {
        get {
            precondition(row >= 0 && row < rows && col >= 0 && col < cols, "index out of range")
            return grid[row * cols + col]
        }
        set {
            precondition(row >= 0 && row < rows && col >= 0 && col < cols, "index out of range")
            grid[row * cols + col] = newValue
        }
    }

    var transposed: Matrix {
        var t = Matrix(rows: cols, cols: rows)
        for r in 0..<rows { for c in 0..<cols { t[c, r] = self[r, c] } }
        return t
    }

    var nested: [[Int]] { (0..<rows).map { r in (0..<cols).map { self[r, $0] } } }

    static func * (a: Matrix, b: Matrix) -> Matrix {
        precondition(a.cols == b.rows, "dimension mismatch")
        var out = Matrix(rows: a.rows, cols: b.cols)
        for i in 0..<a.rows { for j in 0..<b.cols { for k in 0..<a.cols { out[i, j] += a[i, k] * b[k, j] } } }
        return out
    }
}

func matrixDemo(rows: Int, cols: Int, sets: [[Int]]) -> [[Int]] {
    var m = Matrix(rows: rows, cols: cols)
    for s in sets { m[s[0], s[1]] = s[2] }
    return (m * m.transposed).nested
}
