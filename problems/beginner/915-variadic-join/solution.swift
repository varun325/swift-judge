func joinPath(components: [String], separator: String = "/") -> String {
    let cleaned = components
        .map { $0.trimmingCharacters(in: CharacterSet(charactersIn: "/")) }
        .filter { !$0.isEmpty }
    return separator + cleaned.joined(separator: separator)
}

func joinPath(_ components: String..., separator: String = "/") -> String {
    joinPath(components: components, separator: separator)
}

import Foundation

func paths(_ parts: [[String]]) -> [String] {
    parts.map { joinPath(components: $0) } + [joinPath("a", "b", separator: "::")]
}
