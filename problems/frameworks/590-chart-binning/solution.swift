func histogram(_ values: [Double], binWidth w: Double) -> [String] {
    guard w > 0, !values.isEmpty else { return [] }
    var counts: [Int: Int] = [:]
    for v in values { counts[Int((v / w).rounded(.down)), default: 0] += 1 }
    let lo = counts.keys.min()!, hi = counts.keys.max()!
    func fmt(_ x: Double) -> String { x == x.rounded() ? String(Int(x)) : String(x) }
    return (lo...hi).map { k in "\(fmt(Double(k) * w))-\(fmt(Double(k + 1) * w)): \(counts[k] ?? 0)" }
}
