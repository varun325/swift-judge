func streamDemo(_ values: [Int], limit: Int) async -> [Int] {
    let stream = AsyncStream<Int> { continuation in
        for v in values { continuation.yield(v) }
        continuation.finish()
    }
    var evens: [Int] = []
    for await v in stream where v.isMultiple(of: 2) {
        evens.append(v)
        if evens.count == limit { break }
    }
    return evens
}
