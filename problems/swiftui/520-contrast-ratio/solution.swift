import Foundation

func luminance(_ hex: String) -> Double? {
    let digits = hex.hasPrefix("#") ? String(hex.dropFirst()) : hex
    guard digits.count == 6, let v = UInt32(digits, radix: 16) else { return nil }
    let channels = [(v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF].map { Double($0) / 255 }
    let linear = channels.map { $0 <= 0.03928 ? $0 / 12.92 : pow(($0 + 0.055) / 1.055, 2.4) }
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
}

func contrastChecks(_ pairs: [[String]]) -> [String] {
    pairs.map { p in
        guard let a = luminance(p[0]), let b = luminance(p[1]) else { return "invalid" }
        let ratio = (max(a, b) + 0.05) / (min(a, b) + 0.05)
        let grade = ratio >= 4.5 ? "AA" : ratio >= 3 ? "AA-large" : "fail"
        return "\((ratio * 100).rounded() / 100) \(grade)"
    }
}
