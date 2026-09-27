func extractDates(_ text: String) -> [String] {
    let pattern = /(\d{4})-(\d{2})-(\d{2})/
    return text.matches(of: pattern).compactMap { match in
        let (_, year, month, day) = match.output
        guard let m = Int(month), (1...12).contains(m), let d = Int(day), (1...31).contains(d) else { return nil }
        return "\(day)/\(month)/\(year)"
    }
}
