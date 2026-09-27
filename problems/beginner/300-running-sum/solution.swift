func runningSum(_ nums: [Int]) -> [Int] {
    var result: [Int] = []
    result.reserveCapacity(nums.count)
    var total = 0
    for n in nums {
        total += n
        result.append(total)
    }
    return result
}
