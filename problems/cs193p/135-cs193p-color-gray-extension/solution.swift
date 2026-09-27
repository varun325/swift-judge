import SwiftUI

extension Color {
    static func gray(_ brightness: CGFloat) -> Color {
        let b = Double(min(max(brightness, 0), 1))
        return Color(.sRGB, red: b, green: b, blue: b)
    }
}

@MainActor func components(_ color: Color) -> String {
    let r = color.resolve(in: EnvironmentValues())
    return [r.red, r.green, r.blue].map { String(Int(($0 * 255).rounded())) }.joined(separator: ",")
}

func grays(_ levels: [Double]) async -> [String] {
    var out: [String] = []
    for level in levels { out.append(await components(.gray(CGFloat(level)))) }
    return out
}
