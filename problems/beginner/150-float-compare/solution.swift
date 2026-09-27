func nearlyEqual(_ a: Double, _ b: Double) -> Bool {
    abs(a - b) <= 1e-9 * max(1, abs(a), abs(b))
}
