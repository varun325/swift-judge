import SwiftUI

struct Star: Shape {
    let corners: Int
    let smoothness: Double

    func path(in rect: CGRect) -> Path {
        guard corners >= 2 else { return Path() }
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let outer = min(rect.width, rect.height) / 2
        var path = Path()
        for i in 0..<(corners * 2) {
            let radius = i.isMultiple(of: 2) ? outer : outer * smoothness
            let angle = Double(i) * .pi / Double(corners) - .pi / 2
            let point = CGPoint(x: center.x + radius * cos(angle), y: center.y + radius * sin(angle))
            if i == 0 { path.move(to: point) } else { path.addLine(to: point) }
        }
        path.closeSubpath()
        return path
    }
}

func starInfo(points: Int, size: Double) async -> [String] {
    let rect = CGRect(x: 0, y: 0, width: size, height: size)
    let path = Star(corners: points, smoothness: 0.45).path(in: rect)
    var vertices = 0
    path.forEach { element in
        switch element {
        case .move, .line: vertices += 1
        default: break
        }
    }
    // An empty path's boundingRect is CGRect.null (infinite) — never convert that to Int.
    let top = path.isEmpty ? "none" : String(Int(path.boundingRect.minY.rounded()))
    return ["vertices \(vertices)", "center in:\(path.contains(CGPoint(x: size / 2, y: size / 2)))", "top y:\(top)"]
}
