import Foundation

func nextReminders(now: String, rules: [String]) -> [String] {
    var calendar = Calendar(identifier: .gregorian)
    calendar.timeZone = TimeZone(identifier: "UTC")!
    guard let start = try? Date(now, strategy: .iso8601) else { return rules.map { _ in "invalid" } }
    return rules.map { rule in
        let p = rule.split(separator: " ").map(String.init)
        guard let time = p.last?.split(separator: ":").compactMap({ Int($0) }), time.count == 2 else { return "invalid" }
        var components = DateComponents(hour: time[0], minute: time[1], second: 0)
        switch (p.first ?? "", p.count) {
        case ("daily", 2): break
        case ("weekly", 3): components.weekday = Int(p[1])
        case ("monthly", 3): components.day = Int(p[1])
        default: return "invalid"
        }
        guard let next = calendar.nextDate(after: start, matching: components, matchingPolicy: .strict) else { return "invalid" }
        return next.ISO8601Format()
    }
}
