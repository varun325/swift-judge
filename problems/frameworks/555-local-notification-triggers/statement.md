Swiftful's *local Push Notifications*. A calendar trigger fires at the next date matching some `DateComponents`. Compute (in UTC, Gregorian) the next fire date after `now` (ISO 8601) for each rule — what `UNCalendarNotificationTrigger(dateMatching:repeats:)` would do:
 - `daily HH:mm` → hour + minute
 - `weekly <weekday 1-7> HH:mm` (1 = Sunday)
 - `monthly <day> HH:mm` (skip months without that day, e.g. the 31st)

 Return ISO 8601 dates or `"invalid"`.
