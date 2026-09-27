func firstUniqueIndex(_ s: String) -> Int {
    var counts: [Character: Int] = [:]
    for ch in s { counts[ch, default: 0] += 1 }
    for (i, ch) in s.enumerated() where counts[ch] == 1 {
        return i
    }
    return -1
}
