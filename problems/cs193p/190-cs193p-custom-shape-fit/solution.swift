import SwiftUI

struct PegRow: Shape {
    let count: Int
    let spacing: Double

    func diameter(in rect: CGRect) -> Double {
        guard count > 0 else { return 0 }
        return max(0, min(rect.height, (rect.width - spacing * Double(count - 1)) / Double(count)))
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let d = diameter(in: rect)
        guard d > 0 else { return path }
        for i in 0..<count {
            let x = rect.minX + Double(i) * (d + spacing)
            path.addEllipse(in: CGRect(x: x, y: rect.midY - d / 2, width: d, height: d))
        }
        return path
    }
}

func pegLayout(width: Double, height: Double, count: Int, spacing: Double) async -> [String] {
    let rect = CGRect(x: 0, y: 0, width: width, height: height)
    let row = PegRow(count: count, spacing: spacing)
    let path = row.path(in: rect)
    guard !path.isEmpty else { return ["empty"] }
    let b = path.boundingRect
    let r = { (v: Double) in String((v * 100).rounded() / 100) }
    return ["diameter \(r(row.diameter(in: rect)))", "bounds \([b.minX, b.minY, b.width, b.height].map(r).joined(separator: ","))"]
}
