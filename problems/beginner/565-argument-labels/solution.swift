func move(from start: Int, to end: Int, by step: Int) -> [Int] {
    Array(stride(from: start, through: end, by: step))
}
