typealias Grid = [[Int]]
typealias Cell = (row: Int, col: Int)

func cells(around c: Cell, in grid: Grid) -> [Cell] {
    var result: [Cell] = []
    for dr in -1...1 {
        for dc in -1...1 where !(dr == 0 && dc == 0) {
            let r = c.row + dr, col = c.col + dc
            if grid.indices.contains(r), grid[r].indices.contains(col) { result.append((r, col)) }
        }
    }
    return result
}

func neighbours(_ grid: [[Int]], row: Int, col: Int) -> [Int] {
    cells(around: (row, col), in: grid).map { grid[$0.row][$0.col] }
}
