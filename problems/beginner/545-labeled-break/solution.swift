func firstPair(_ grid: [[Int]], target: Int) -> [Int] {
    var found: [Int] = []
    search: for (r, row) in grid.enumerated() {
        for (c, value) in row.enumerated() where value == target {
            found = [r, c]
            break search
        }
    }
    return found
}
