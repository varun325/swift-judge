func sum(_ s: Span<Int>) -> Int {
    var total = 0
    for i in s.indices { total += s[i] }
    return total
}

func maxRun(_ s: Span<Int>) -> Int {
    guard !s.isEmpty else { return 0 }
    var best = 1, current = 1
    for i in 1..<s.count {
        current = s[i] == s[i - 1] ? current + 1 : 1
        best = max(best, current)
    }
    return best
}

func spanStats(_ values: [Int]) -> [Int] {
    let span = values.span
    return [sum(span), maxRun(span), span.count]
}
