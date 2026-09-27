struct Countdown: AsyncSequence {
    typealias Element = Int
    let start: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var current: Int
        mutating func next() async -> Int? {
            guard current >= 0 else { return nil }
            await Task.yield()
            defer { current -= 1 }
            return current
        }
    }

    func makeAsyncIterator() -> AsyncIterator { AsyncIterator(current: start) }
}

func countdown(from start: Int, keepEvensOnly: Bool) async -> [Int] {
    var out: [Int] = []
    if keepEvensOnly {
        for await n in Countdown(start: start).filter({ $0.isMultiple(of: 2) }) { out.append(n) }
    } else {
        for await n in Countdown(start: start) { out.append(n) }
    }
    return out
}
