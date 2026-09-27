import Foundation

func timeline(now: String, events: [[String]], hours: Int) -> [String] {
    var calendar = Calendar(identifier: .gregorian)
    calendar.timeZone = TimeZone(identifier: "UTC")!
    guard let start = try? Date(now, strategy: .iso8601) else { return ["invalid"] }
    let upcoming = events.compactMap { e -> (String, Date)? in
        (try? Date(e[1], strategy: .iso8601)).map { (e[0], $0) }
    }.sorted { $0.1 < $1.1 }
    let f = DateFormatter()
    f.timeZone = calendar.timeZone
    f.locale = Locale(identifier: "en_US_POSIX")
    f.dateFormat = "HH:mm"
    let firstHour = calendar.nextDate(after: start, matching: DateComponents(minute: 0), matchingPolicy: .strict) ?? start
    var moments = [start]
    for h in 0..<max(hours, 0) { moments.append(calendar.date(byAdding: .hour, value: h, to: firstHour)!) }
    var entries: [(Date, String)] = []
    for m in moments {
        let title = upcoming.first { $0.1 > m }?.0 ?? "free"
        if entries.last?.1 != title { entries.append((m, title)) }
    }
    var out = entries.map { "\(f.string(from: $0.0)) \($0.1)" }
    out.append("reload after \(f.string(from: calendar.date(byAdding: .hour, value: 1, to: moments.last!)!))")
    return out
}
