import Foundation

func highlight(_ text: String, terms: [String]) -> [String] {
    var attributed = AttributedString(text)
    for term in terms where !term.isEmpty {
        var searchStart = attributed.startIndex
        while searchStart < attributed.endIndex,
              let range = attributed[searchStart...].range(of: term, options: .caseInsensitive) {
            attributed[range].inlinePresentationIntent = .stronglyEmphasized
            searchStart = range.upperBound
        }
    }
    return attributed.runs.map { run in
        let piece = String(attributed[run.range].characters)
        return "\(piece)|\(run.inlinePresentationIntent == .stronglyEmphasized ? "bold" : "plain")"
    }
}
