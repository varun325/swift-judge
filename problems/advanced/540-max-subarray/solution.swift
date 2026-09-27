func maxSubArray(_ nums: [Int]) -> Int {
    guard let first = nums.first else { return 0 }
    return nums.dropFirst().reduce((current: first, best: first)) { acc, x in
        let current = max(x, acc.current + x)
        return (current, max(acc.best, current))
    }.best
}
