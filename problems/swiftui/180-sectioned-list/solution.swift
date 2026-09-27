import Foundation

func sections(_ names: [String]) -> [String] {
    let grouped = Dictionary(grouping: names) { name -> String in
        guard let first = name.first, first.isLetter else { return "#" }
        return String(first).uppercased()
    }
    let keys = grouped.keys.sorted { ($0 == "#" ? 1 : 0, $0) < ($1 == "#" ? 1 : 0, $1) }
    return keys.map { key in
        let members = grouped[key]!.sorted { $0.localizedCaseInsensitiveCompare($1) == .orderedAscending }
        return "\(key): \(members.joined(separator: ", "))"
    }
}
