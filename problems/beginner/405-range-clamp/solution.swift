extension Comparable {
    func clamped(to range: ClosedRange<Self>) -> Self {
        min(max(self, range.lowerBound), range.upperBound)
    }
}

func clampAll(_ values: [Int], low: Int, high: Int) -> [Int] {
    values.map { $0.clamped(to: low...high) }
}
