func twoSum(_ nums: [Int], target: Int) -> [Int] {
    var seen: [Int: Int] = [:]
    for (i, n) in nums.enumerated() {
        if let j = seen[target - n] { return [j, i] }
        seen[n] = i
    }
    return []
}
