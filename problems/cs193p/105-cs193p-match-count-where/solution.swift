enum Match: String {
    case nomatch, exact, inexact
}

func markerSummary(_ matches: [String]) -> [Int] {
    let parsed = matches.compactMap(Match.init(rawValue:))
    return [
        parsed.count(where: { $0 == .exact }),
        parsed.count(where: { $0 == .inexact }),
        parsed.count(where: { $0 == .nomatch }),
    ]
}
