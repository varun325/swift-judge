func adaptiveColumns(containerWidths: [Double], minimum: Double, spacing: Double) -> [[Double]] {
    containerWidths.map { w in
        let count = max(1, ((w + spacing) / (minimum + spacing)).rounded(.down))
        let width = (w - spacing * (count - 1)) / count
        return [count, (width * 100).rounded() / 100]
    }
}
