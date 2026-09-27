func longestConsecutive(_ nums: [Int]) -> Int {
    let set = Set(nums)
    var best = 0
    for n in set where !set.contains(n - 1) {
        var length = 1
        while set.contains(n + length) { length += 1 }
        best = max(best, length)
    }
    return best
}
