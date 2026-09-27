func flowRows(widths: [Double], containerWidth: Double, spacing: Double) -> [[Int]] {
    var rows: [[Int]] = []
    var current: [Int] = []
    var x = 0.0
    for (i, w) in widths.enumerated() {
        let needed = current.isEmpty ? w : x + spacing + w
        if !current.isEmpty && needed > containerWidth {
            rows.append(current)
            current = [i]
            x = w
        } else {
            current.append(i)
            x = needed
        }
    }
    if !current.isEmpty { rows.append(current) }
    return rows
}
