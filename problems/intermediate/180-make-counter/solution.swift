func makeCounter(step: Int) -> () -> Int {
    var total = 0
    return {
        total += step
        return total
    }
}

func counterDemo(_ calls: [String]) -> [Int] {
    let a = makeCounter(step: 1)
    let b = makeCounter(step: 10)
    return calls.map { $0 == "a" ? a() : b() }
}
