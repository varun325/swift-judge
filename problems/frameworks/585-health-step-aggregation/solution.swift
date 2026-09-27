import Foundation

func dailySteps(_ samples: [[String]], timeZone: String) -> [String] {
    var calendar = Calendar(identifier: .gregorian)
    guard let zone = TimeZone(identifier: timeZone) else { return ["invalid zone"] }
    calendar.timeZone = zone
    var totals: [Date: Int] = [:]
    for s in samples {
        guard let date = try? Date(s[0], strategy: .iso8601), let n = Int(s[1]) else { continue }
        totals[calendar.startOfDay(for: date), default: 0] += n
    }
    guard let first = totals.keys.min(), let last = totals.keys.max() else { return [] }
    let f = DateFormatter()
    f.calendar = calendar
    f.timeZone = zone
    f.locale = Locale(identifier: "en_US_POSIX")
    f.dateFormat = "yyyy-MM-dd"
    var out: [String] = []
    var day = first
    while day <= last {
        out.append("\(f.string(from: day)) \(totals[day] ?? 0)")
        day = calendar.date(byAdding: .day, value: 1, to: day)!
    }
    return out
}
