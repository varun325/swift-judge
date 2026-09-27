import SwiftUI

func lerp<V: VectorArithmetic>(_ a: V, _ b: V, _ t: Double) -> V {
    var delta = b - a
    delta.scale(by: t)
    return a + delta
}

func interpolatePairs(_ start: [Double], _ end: [Double], _ fractions: [Double]) async -> [[Double]] {
    let a = AnimatablePair(start[0], start[1])
    let b = AnimatablePair(end[0], end[1])
    return fractions.map { t in
        let v = lerp(a, b, t)
        return [v.first, v.second].map { ($0 * 1000).rounded() / 1000 }
    }
}
