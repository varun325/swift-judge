func countdown(from start: Int, step: Int) -> [Int] {
    Array(stride(from: start, through: 0, by: -step))
}
