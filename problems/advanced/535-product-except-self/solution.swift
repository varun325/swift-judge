func productExceptSelf(_ nums: [Int]) -> [Int] {
    var answer = Array(repeating: 1, count: nums.count)
    var prefix = 1
    for i in nums.indices {
        answer[i] = prefix
        prefix *= nums[i]
    }
    var suffix = 1
    for i in nums.indices.reversed() {
        answer[i] *= suffix
        suffix *= nums[i]
    }
    return answer
}
