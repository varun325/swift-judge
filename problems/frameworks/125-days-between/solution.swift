import Foundation

func dateFacts(birth: String, today: String) -> [Int] {
    var calendar = Calendar(identifier: .gregorian)
    calendar.timeZone = TimeZone(identifier: "UTC")!
    let f = DateFormatter()
    f.calendar = calendar
    f.timeZone = calendar.timeZone
    f.locale = Locale(identifier: "en_US_POSIX")
    f.dateFormat = "yyyy-MM-dd"
    guard let b = f.date(from: birth), let t = f.date(from: today) else { return [] }
    let age = calendar.dateComponents([.year], from: b, to: t).year ?? 0
    let days = calendar.dateComponents([.day], from: b, to: t).day ?? 0
    let parts = calendar.dateComponents([.month, .day], from: b)
    let isBirthday = calendar.dateComponents([.month, .day], from: t) == parts
    let next = calendar.nextDate(after: t, matching: parts, matchingPolicy: .nextTimePreservingSmallerComponents) ?? t
    let until = isBirthday ? 0 : calendar.dateComponents([.day], from: t, to: next).day ?? 0
    return [age, days, until]
}
