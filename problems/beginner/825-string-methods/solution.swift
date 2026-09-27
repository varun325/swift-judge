import Foundation

func analyze(_ text: String) -> [String] {
    let capitalized = text.prefix(1).uppercased() + text.dropFirst()
    return [
        text.hasPrefix("http") ? "url" : "text",
        capitalized,
        String(text.localizedCaseInsensitiveContains("swift")),
        text.replacingOccurrences(of: " ", with: "_"),
        "\(text.count)",
    ]
}
