func roundings(_ value: Double) -> [Double] {
    [value.rounded(), value.rounded(.down), value.rounded(.up), value.rounded(.towardZero), (value * 100).rounded() / 100]
}
