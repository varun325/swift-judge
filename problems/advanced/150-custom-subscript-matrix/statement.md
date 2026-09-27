`struct Matrix` with `rows`, `cols`, flat `grid: [Int]` and a **two-parameter** subscript `subscript(row: Int, col: Int) -> Int { get set }` that uses `precondition` to check bounds. Add a `static func *` for matrix multiplication (precondition on dimensions).

 Apply each `[r, c, v]` in `sets` to an all-zero matrix `m`, then return `(m * transpose(m))` as nested arrays, where you also write `var transposed: Matrix`.
