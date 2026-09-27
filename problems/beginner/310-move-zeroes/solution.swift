func moveZeroes(_ nums: inout [Int]) {
    var write = 0
    for read in nums.indices where nums[read] != 0 {
        nums.swapAt(write, read)
        write += 1
    }
}
