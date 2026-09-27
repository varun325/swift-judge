import SwiftUI

func sampleCurves(_ times: [Double]) async -> [[Double]] {
    let curves: [UnitCurve] = [.linear, .easeIn, .easeOut, .easeInOut]
    return times.map { t in curves.map { ($0.value(at: t) * 1000).rounded() / 1000 } }
}
