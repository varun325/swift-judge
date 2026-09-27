func intersect(_ a: [Int], _ b: [Int]) -> [Int] {
    var counts = a.reduce(into: [Int: Int]()) { $0[$1, default: 0] += 1 }
    return b.filter { n in
        guard let c = counts[n], c > 0 else { return false }
        counts[n] = c - 1
        return true
    }
}
