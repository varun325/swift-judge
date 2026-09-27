func average(of numbers: [Double]) -> Double? {
    numbers.isEmpty ? nil : numbers.reduce(0, +) / Double(numbers.count)
}

func average(_ numbers: Double...) -> Double? {
    average(of: numbers)
}

func averages(_ groups: [[Double]]) -> [Double?] {
    precondition(average(1, 2, 3) == 2)
    return groups.map { average(of: $0) }
}
