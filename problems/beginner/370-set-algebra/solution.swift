func tagReport(_ a: [String], _ b: [String]) -> [[String]] {
    let sa = Set(a), sb = Set(b)
    return [
        sa.intersection(sb).sorted(),
        sa.subtracting(sb).sorted(),
        sb.subtracting(sa).sorted(),
        sa.symmetricDifference(sb).sorted(),
    ]
}
