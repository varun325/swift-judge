extension Collection where Element: BinaryInteger {
    var average: Double {
        isEmpty ? 0 : Double(reduce(0, +)) / Double(count)
    }
}

extension Collection where Element: BinaryFloatingPoint {
    var average: Element {
        isEmpty ? 0 : reduce(0, +) / Element(count)
    }
}

func statsDemo(_ ints: [Int], _ doubles: [Double]) -> [Double] {
    [ints.average, Double(doubles.average), Array(ints.prefix(2)).average]
}
