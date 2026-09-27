struct ZoomState {
    private(set) var lastScale = 1.0
    private(set) var currentScale = 1.0

    private func clamp(_ v: Double) -> Double { min(max(v, 1), 4) }

    mutating func change(by magnification: Double) { currentScale = clamp(lastScale * magnification) }
    mutating func end() { lastScale = currentScale }
    mutating func reset() { lastScale = 1; currentScale = 1 }
}

func zoomSession(_ events: [String]) -> [Double] {
    var zoom = ZoomState()
    return events.map { e in
        let p = e.split(separator: " ")
        switch p[0] {
        case "change": zoom.change(by: Double(p[1]) ?? 1)
        case "end": zoom.end()
        default: zoom.reset()
        }
        return (zoom.currentScale * 100).rounded() / 100
    }
}
