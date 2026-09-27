func dedupeSorted(_ nums: inout [Int]) {
    guard !nums.isEmpty else { return }
    var write = 1
    for read in 1..<nums.count where nums[read] != nums[write - 1] {
        nums[write] = nums[read]
        write += 1
    }
    nums.removeLast(nums.count - write)
}
