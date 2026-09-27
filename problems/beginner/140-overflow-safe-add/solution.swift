func safeAdd(_ a: Int, _ b: Int) -> Int? {
    let (sum, overflow) = a.addingReportingOverflow(b)
    return overflow ? nil : sum
}
