enum SqrtError: Error { case outOfBounds, noRoot }

func integerSqrt(_ n: Int) throws -> Int {
    guard (1...10_000).contains(n) else { throw SqrtError.outOfBounds }
    for i in 1...100 where i * i == n {
        return i
    }
    throw SqrtError.noRoot
}
