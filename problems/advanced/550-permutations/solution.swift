func permute(_ nums: [Int]) -> [[Int]] {
    var result: [[Int]] = []
    var path: [Int] = []
    var used = Array(repeating: false, count: nums.count)

    func backtrack() {
        if path.count == nums.count {
            result.append(path)
            return
        }
        for i in nums.indices where !used[i] {
            used[i] = true
            path.append(nums[i])
            backtrack()
            path.removeLast()
            used[i] = false
        }
    }

    backtrack()
    return result
}
