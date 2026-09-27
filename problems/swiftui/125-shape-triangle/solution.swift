import SwiftUI

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var p = Path()
        p.move(to: CGPoint(x: rect.midX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        p.closeSubpath()
        return p
    }
}

func triangleInfo(width: Double, height: Double, points: [[Double]]) async -> [String] {
    let path = Triangle().path(in: CGRect(x: 0, y: 0, width: width, height: height))
    let box = path.boundingRect
    return ["\(Int(box.width))×\(Int(box.height))"] + points.map { path.contains(CGPoint(x: $0[0], y: $0[1])) ? "in" : "out" }
}
