import SwiftUI

extension Color {
    init?(hex: String) {
        let digits = hex.hasPrefix("#") ? String(hex.dropFirst()) : hex
        guard digits.count == 6, let value = UInt32(digits, radix: 16) else { return nil }
        self.init(
            .sRGB,
            red: Double((value >> 16) & 0xFF) / 255,
            green: Double((value >> 8) & 0xFF) / 255,
            blue: Double(value & 0xFF) / 255
        )
    }
}

@MainActor func components(_ color: Color) -> String {
    let r = color.resolve(in: EnvironmentValues())
    return [r.red, r.green, r.blue].map { String(Int(($0 * 255).rounded())) }.joined(separator: ",")
}

func hexColors(_ hexes: [String]) async -> [String] {
    var out: [String] = []
    for hex in hexes {
        guard let color = Color(hex: hex) else { out.append("invalid"); continue }
        out.append(await components(color))
    }
    return out
}
