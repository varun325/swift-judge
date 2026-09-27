func sink(_ grid: inout [[Character]], _ r: Int, _ c: Int) {
    var queue = [(r, c)]
    grid[r][c] = "0"
    while !queue.isEmpty {
        let (y, x) = queue.removeLast()
        for (dy, dx) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let ny = y + dy, nx = x + dx
            guard grid.indices.contains(ny), grid[ny].indices.contains(nx), grid[ny][nx] == "1" else { continue }
            grid[ny][nx] = "0"
            queue.append((ny, nx))
        }
    }
}

func numIslands(_ grid: [String]) -> Int {
    var g = grid.map(Array.init)
    var count = 0
    for r in g.indices {
        for c in g[r].indices where g[r][c] == "1" {
            count += 1
            sink(&g, r, c)
        }
    }
    return count
}
