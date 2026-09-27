func merge(_ intervals: [[Int]]) -> [[Int]] {
    var result: [[Int]] = []
    for iv in intervals.sorted(by: { $0[0] < $1[0] }) {
        if let last = result.last, iv[0] <= last[1] {
            result[result.count - 1][1] = max(last[1], iv[1])
        } else {
            result.append(iv)
        }
    }
    return result
}
