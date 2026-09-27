func fibAndGcd(_ n: Int, _ a: Int, _ b: Int) -> [Int] {
    var (x, y) = (0, 1)
    for _ in 0..<n { (x, y) = (y, x + y) }
    var (p, q) = (a, b)
    while q != 0 { (p, q) = (q, p % q) }
    return [x, p]
}
