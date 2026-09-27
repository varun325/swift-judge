func summary(_ values: [Double]) -> (mean: Double, median: Double, range: Double)? {
    guard !values.isEmpty else { return nil }
    let s = values.sorted()
    let mid = s.count / 2
    let median = s.count.isMultiple(of: 2) ? (s[mid - 1] + s[mid]) / 2 : s[mid]
    return (s.reduce(0, +) / Double(s.count), median, s.last! - s.first!)
}

func stats(_ values: [Double]) -> [Double] {
    guard let (mean, median, range) = summary(values) else { return [] }
    return [mean, median, range]
}
