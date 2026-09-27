func minMax(_ nums: [Int]) -> (min: Int, max: Int)? {
    guard var lo = nums.first else { return nil }
    var hi = lo
    for n in nums.dropFirst() {
        lo = Swift.min(lo, n)
        hi = Swift.max(hi, n)
    }
    return (lo, hi)
}

func bounds(_ nums: [Int]) -> [Int] {
    guard let result = minMax(nums) else { return [] }
    return [result.min, result.max]
}
