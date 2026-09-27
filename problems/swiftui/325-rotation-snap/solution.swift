import SwiftUI

func snap(_ angle: Angle) -> Angle {
    let snapped = (angle.degrees / 90).rounded() * 90
    // Adding 360 and taking the remainder again maps negatives into range and turns -0.0 into +0.0.
    let normalised = (snapped.truncatingRemainder(dividingBy: 360) + 360).truncatingRemainder(dividingBy: 360)
    return .degrees(normalised)
}

func snapAngles(_ degrees: [Double]) async -> [Double] {
    degrees.map { snap(.degrees($0)).degrees }
}
