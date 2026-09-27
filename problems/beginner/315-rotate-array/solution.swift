func rotate(_ nums: [Int], by k: Int) -> [Int] {
    guard !nums.isEmpty else { return [] }
    let shift = k % nums.count
    return Array(nums[(nums.count - shift)...] + nums[..<(nums.count - shift)])
}
