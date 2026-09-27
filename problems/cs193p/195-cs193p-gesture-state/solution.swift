struct BoardState {
    private(set) var zoom = 1.0
    private(set) var pan = (x: 0.0, y: 0.0)
    private(set) var gestureZoom = 1.0
    private(set) var gesturePan = (x: 0.0, y: 0.0)

    var renderedZoom: Double { zoom * gestureZoom }
    var renderedPan: (x: Double, y: Double) { (pan.x + gesturePan.x, pan.y + gesturePan.y) }

    mutating func pinch(_ m: Double) { gestureZoom = m }
    mutating func drag(_ dx: Double, _ dy: Double) { gesturePan = (dx, dy) }

    mutating func end() {
        zoom *= gestureZoom
        pan = renderedPan
        cancel()
    }

    mutating func cancel() {
        gestureZoom = 1
        gesturePan = (0, 0)
    }
}

func boardGestures(_ events: [String]) -> [String] {
    var board = BoardState()
    let r = { (v: Double) in String((v * 100).rounded() / 100) }
    return events.map { e in
        let p = e.split(separator: " ").map(String.init)
        switch p[0] {
        case "pinch": board.pinch(Double(p.count > 1 ? p[1] : "") ?? 1)
        case "drag": board.drag(Double(p.count > 1 ? p[1] : "") ?? 0, Double(p.count > 2 ? p[2] : "") ?? 0)
        case "end": board.end()
        default: board.cancel()
        }
        let pan = board.renderedPan
        return "zoom \(r(board.renderedZoom)) pan \(r(pan.x)),\(r(pan.y))"
    }
}
