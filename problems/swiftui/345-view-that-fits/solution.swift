func chooseLayouts(idealWidths: [Double], available: [Double]) -> [Int] {
    available.map { width in
        idealWidths.firstIndex { $0 <= width } ?? max(idealWidths.count - 1, 0)
    }
}
