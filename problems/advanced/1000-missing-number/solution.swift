func missingNumber(_ nums: [Int]) -> Int {
    nums.enumerated().reduce(nums.count) { $0 ^ $1.offset ^ $1.element }
}
