import SwiftUI

func ringBounds(progress: [Double]) async -> [String] {
    let circle = Path(ellipseIn: CGRect(x: 0, y: 0, width: 100, height: 100))
    return progress.map { p in
        let trimmed = circle.trimmedPath(from: 0, to: min(max(p, 0), 1))
        guard !trimmed.isEmpty else { return "empty" }
        let b = trimmed.boundingRect
        return [b.minX, b.minY, b.width, b.height].map { String(Int($0.rounded())) }.joined(separator: ",")
    }
}
