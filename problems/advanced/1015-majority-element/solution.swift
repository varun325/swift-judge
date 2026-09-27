func majority(_ nums: [Int]) -> Int? {
    var candidate: Int?
    var votes = 0
    for n in nums {
        if votes == 0 { candidate = n }
        votes += n == candidate ? 1 : -1
    }
    guard let c = candidate, nums.count(where: { $0 == c }) * 2 > nums.count else { return nil }
    return c
}
