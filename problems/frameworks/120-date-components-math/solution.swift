import Foundation

func addMonths(_ isoDates: [String], months: Int) -> [String] {
    var calendar = Calendar(identifier: .gregorian)
    calendar.timeZone = TimeZone(identifier: "UTC")!
    let formatter = DateFormatter()
    formatter.calendar = calendar
    formatter.timeZone = calendar.timeZone
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.dateFormat = "yyyy-MM-dd"
    let weekday = DateFormatter()
    weekday.calendar = calendar
    weekday.timeZone = calendar.timeZone
    weekday.locale = formatter.locale
    weekday.dateFormat = "EEEE"
    return isoDates.map { iso in
        guard let date = formatter.date(from: iso),
              let result = calendar.date(byAdding: .month, value: months, to: date) else { return "invalid" }
        return "\(formatter.string(from: result)) \(weekday.string(from: result))"
    }
}
