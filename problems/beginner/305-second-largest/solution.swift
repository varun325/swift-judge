func secondLargest(_ nums: [Int]) -> Int? {
    var first: Int?
    var second: Int?
    for n in nums {
        if first == nil || n > first! {
            second = first
            first = n
        } else if n != first, second == nil || n > second! {
            second = n
        }
    }
    return second
}
