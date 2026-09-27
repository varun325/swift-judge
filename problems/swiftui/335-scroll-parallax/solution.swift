func headerEffects(_ offsets: [Double], headerHeight h: Double) -> [[Double]] {
    offsets.map { y in
        let height = y < 0 ? h - y : h
        let offsetY = max(y, 0) / 2
        let opacity = 1 - min(max(y, 0) / h, 1)
        return [height, offsetY, opacity].map { ($0 * 100).rounded() / 100 }
    }
}
