func minMax(_ nums: [Int]) -> (min: Int, max: Int)? {
    return nil
}

func bounds(_ nums: [Int]) -> [Int] {
    guard let result = minMax(nums) else { return [] }
    return [result.min, result.max]
}
