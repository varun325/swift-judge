var rows: [[Int]] = []
while let line = readLine() {
    let row = line.split(separator: " ").compactMap { Int($0) }
    if !row.isEmpty { rows.append(row) }
}
if let width = rows.first?.count {
    for c in 0..<width {
        print(rows.map { String($0[c]) }.joined(separator: " "))
    }
}
