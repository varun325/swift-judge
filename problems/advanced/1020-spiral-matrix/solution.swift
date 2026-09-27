func spiral(_ matrix: [[Int]]) -> [Int] {
    guard !matrix.isEmpty, !matrix[0].isEmpty else { return [] }
    var top = 0, bottom = matrix.count - 1, left = 0, right = matrix[0].count - 1
    var out: [Int] = []
    while top <= bottom && left <= right {
        for c in stride(from: left, through: right, by: 1) { out.append(matrix[top][c]) }
        top += 1
        for r in stride(from: top, through: bottom, by: 1) { out.append(matrix[r][right]) }
        right -= 1
        if top <= bottom {
            for c in stride(from: right, through: left, by: -1) { out.append(matrix[bottom][c]) }
            bottom -= 1
        }
        if left <= right {
            for r in stride(from: bottom, through: top, by: -1) { out.append(matrix[r][left]) }
            left += 1
        }
    }
    return out
}
