import SwiftUI

struct RoundedCornerRect: Shape {
    var cornerRadius: Double

    var animatableData: Double {
        get { cornerRadius }
        set { cornerRadius = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var p = Path()
        p.move(to: CGPoint(x: rect.minX + cornerRadius, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        p.addLine(to: CGPoint(x: rect.minX, y: rect.minY + cornerRadius))
        p.addQuadCurve(to: CGPoint(x: rect.minX + cornerRadius, y: rect.minY), control: CGPoint(x: rect.minX, y: rect.minY))
        return p
    }
}

func animateCorner(from: Double, to: Double, steps: Int) async -> [Double] {
    var shape = RoundedCornerRect(cornerRadius: from)
    var xs: [Double] = []
    for t in 0...max(steps, 0) {
        shape.animatableData = steps == 0 ? to : from + (to - from) * Double(t) / Double(steps)
        var firstX = 0.0
        var found = false
        shape.path(in: CGRect(x: 0, y: 0, width: 100, height: 100)).forEach { element in
            if !found, case .move(let point) = element { firstX = point.x; found = true }
        }
        xs.append((firstX * 100).rounded() / 100)
    }
    return xs
}
