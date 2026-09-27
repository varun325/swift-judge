func targetPages(_ gestures: [[Double]], pageWidth: Double, pageCount: Int) -> [Int] {
    gestures.map { g in
        let position = g[0] / pageWidth
        let page: Double
        if g[1] > 0.5 { page = position.rounded(.down) + 1 }
        else if g[1] < -0.5 { page = position.rounded(.up) - 1 }
        else { page = position.rounded() }
        return min(max(Int(page), 0), max(pageCount - 1, 0))
    }
}
