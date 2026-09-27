func lengthOfLongestSubstring(_ s: String) -> Int {
    var lastSeen: [Character: Int] = [:]
    var start = 0
    var best = 0
    for (i, ch) in s.enumerated() {
        if let prev = lastSeen[ch], prev >= start { start = prev + 1 }
        lastSeen[ch] = i
        best = max(best, i - start + 1)
    }
    return best
}
