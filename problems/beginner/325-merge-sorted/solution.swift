func merge(_ a: [Int], _ b: [Int]) -> [Int] {
    var result: [Int] = []
    result.reserveCapacity(a.count + b.count)
    var i = 0, j = 0
    while i < a.count && j < b.count {
        if a[i] <= b[j] { result.append(a[i]); i += 1 }
        else { result.append(b[j]); j += 1 }
    }
    result += a[i...]
    result += b[j...]
    return result
}
