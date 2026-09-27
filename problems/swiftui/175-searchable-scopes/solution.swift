import Foundation

enum SearchScope: String, CaseIterable {
    case all, family, work, friends
}

func search(_ contacts: [[String]], query: String, scope: String) -> [String] {
    let scope = SearchScope(rawValue: scope) ?? .all
    let q = query.trimmingCharacters(in: .whitespaces)
    return contacts
        .filter { scope == .all || $0[1] == scope.rawValue }
        .filter { q.isEmpty || $0[0].localizedStandardContains(q) }
        .map { $0[0] }
        .sorted { $0.localizedStandardCompare($1) == .orderedAscending }
}
