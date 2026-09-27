import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
F='https://developer.apple.com/documentation/foundation/'
MAC=['darwin']
MOCK = '''
 /// Offline test server: URLSession requests are answered by `routes` instead of the network.
 final class MockURLProtocol: URLProtocol, @unchecked Sendable {
     nonisolated(unsafe) static var routes: [String: (status: Int, body: String)] = [:]
     nonisolated(unsafe) static var requests: [String] = []
     override class func canInit(with request: URLRequest) -> Bool { true }
     override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
     override func startLoading() {
         let url = request.url!
         let key = "\\(request.httpMethod ?? "GET") \\(url.path)\\(url.query.map { "?" + $0 } ?? "")"
         MockURLProtocol.requests.append(key)
         let route = MockURLProtocol.routes[key] ?? (404, "{}")
         let response = HTTPURLResponse(url: url, statusCode: route.status, httpVersion: nil, headerFields: ["Content-Type": "application/json"])!
         client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
         client?.urlProtocol(self, didLoad: Data(route.body.utf8))
         client?.urlProtocolDidFinishLoading(self)
     }
     override func stopLoading() {}
 }

 func mockSession() -> URLSession {
     let config = URLSessionConfiguration.ephemeral
     config.protocolClasses = [MockURLProtocol.self]
     return URLSession(configuration: config)
 }
'''
P=[]
# ---------------- formatting
P.append(dict(id='format-currency-percent', title='FormatStyle: Currency, Percent & Numbers', topic='Formatting', platforms=MAC, concepts=['fundamental-types'], docs=[('FormatStyle', F+'formatstyle'), ('Data formatting', F+'data-formatting')],
 sig='func formatted(_ values: [Double]) -> [String]',
 statement="""Sean Allen's *Dead Simple Formatting*. For each value return `"<USD> | <EUR in de_DE> | <percent> | <compact>"` using `.formatted(...)` with **explicit locales** (never rely on the device locale in tests):
 - `.currency(code: "USD").locale(en_US)`
 - `.currency(code: "EUR").locale(de_DE)`
 - `.percent.precision(.fractionLength(1)).locale(en_US)` (value interpreted as a fraction)
 - `.number.notation(.compactName).locale(en_US)`""",
 solution="""
 import Foundation

 func formatted(_ values: [Double]) -> [String] {
     let us = Locale(identifier: "en_US")
     let de = Locale(identifier: "de_DE")
     return values.map { v in
         [
             v.formatted(.currency(code: "USD").locale(us)),
             v.formatted(.currency(code: "EUR").locale(de)),
             v.formatted(.percent.precision(.fractionLength(1)).locale(us)),
             v.formatted(.number.notation(.compactName).locale(us)),
         ].joined(separator: " | ")
     }
 }
 """,
 explain="""`FormatStyle` (iOS 15+) replaces most `NumberFormatter` code with composable, value-type styles. Locale changes grouping, decimal separators and symbol placement (`1.234,50 €`). Always pin a locale in tests — output depends on it.""",
 hints=("`value.formatted(style)` with a `.currency`, `.percent` or `.number` style.","Chain `.locale(Locale(identifier: …))` onto each style.","Compact: `.number.notation(.compactName)`."),
 tests=[{'values':[1234.5,0.256,1500000,-3]}, {'values':[]}], hidden=0))
P.append(dict(id='format-measurement', title='Measurements & Unit Conversion', topic='Formatting', platforms=MAC, concepts=['generics','fundamental-types'], docs=[('Measurement', F+'measurement'), ('UnitLength', F+'unitlength')],
 sig='func runs(_ kilometres: [Double]) -> [String]',
 statement="""For each run distance in km, return `"<km formatted> = <miles formatted> in <pace>"` where the pace assumes 5 min 30 s per km, formatted as a `Duration` (`.time(pattern: .hourMinuteSecond)`). Use `Measurement<UnitLength>` conversion and `.formatted(.measurement(width: .abbreviated, usage: .asProvided, numberFormatStyle: .number.precision(.fractionLength(2))).locale(en_US))`.""",
 solution="""
 import Foundation

 func runs(_ kilometres: [Double]) -> [String] {
     let us = Locale(identifier: "en_US")
     let style = Measurement<UnitLength>.FormatStyle(width: .abbreviated, locale: us, usage: .asProvided, numberFormatStyle: .number.precision(.fractionLength(2)))
     return kilometres.map { km in
         let distance = Measurement(value: km, unit: UnitLength.kilometers)
         let miles = distance.converted(to: .miles)
         let pace = Duration.seconds(km * 330)
         return "\\(distance.formatted(style)) = \\(miles.formatted(style)) in \\(pace.formatted(.time(pattern: .hourMinuteSecond)))"
     }
 }
 """,
 explain="""`Measurement` carries its unit in the type (`Measurement<UnitLength>`), so you can't add metres to seconds, and `converted(to:)` does the arithmetic. `usage: .asProvided` keeps your unit; `.road` or `.personHeight` would let the locale choose.""",
 hints=("`Measurement(value:unit:)` and `.converted(to: .miles)`.","Format with a `Measurement<UnitLength>.FormatStyle` pinned to `en_US`.","Pace: `Duration.seconds(km * 330).formatted(.time(pattern: .hourMinuteSecond))`."),
 tests=[{'kilometres':[5,21.0975,0.4]}, {'kilometres':[]}], hidden=0))
P.append(dict(id='format-bytes-lists-names', title='Formatting Bytes, Lists & Names', topic='Formatting', platforms=MAC, concepts=['fundamental-types','string-interpolation'], docs=[('ByteCountFormatStyle', F+'bytecountformatstyle'), ('ListFormatStyle', F+'listformatstyle'), ('PersonNameComponents', F+'personnamecomponents')],
 sig='func describeUpload(files: [String], sizes: [Int], fullName: [String]) -> [String]',
 statement="""Return three strings (locale `en_US`):
 1. `files.formatted(.list(type: .and))` — e.g. `"a.txt, b.txt, and c.txt"`
 2. total size with `.byteCount(style: .file)`
 3. the uploader's name from `PersonNameComponents(givenName:familyName:)` formatted `.name(style: .abbreviated)` (initials) — `fullName` is `[given, family]`""",
 solution="""
 import Foundation

 func describeUpload(files: [String], sizes: [Int], fullName: [String]) -> [String] {
     let us = Locale(identifier: "en_US")
     var name = PersonNameComponents()
     name.givenName = fullName.first
     name.familyName = fullName.count > 1 ? fullName[1] : nil
     return [
         files.formatted(.list(type: .and).locale(us)),
         Int64(sizes.reduce(0, +)).formatted(.byteCount(style: .file).locale(us)),
         name.formatted(.name(style: .abbreviated).locale(us)),
     ]
 }
 """,
 explain="""List formatting handles commas and conjunctions per language (the Oxford comma in English); byte counts pick sensible units; name formatting knows given/family order and initials for each locale. Hand-rolled string joining gets all of these wrong somewhere.""",
 hints=("Arrays of strings can be formatted as a list with `.list(type: .and)`.","Sizes need `Int64` for `.byteCount(style: .file)`.","Build `PersonNameComponents` and format with `.name(style: .abbreviated)`."),
 tests=[{'files':['a.txt','b.txt','c.txt'],'sizes':[1500000,250000],'fullName':['Ada','Lovelace']}, {'files':['solo.md'],'sizes':[0],'fullName':['Prince']}, {'files':[],'sizes':[],'fullName':['A','B']}], hidden=0))
P.append(dict(id='parse-strategies', title='Parsing Input with ParseStrategy', topic='Formatting', diff='medium', platforms=MAC, concepts=['failable-init','error-handling'], docs=[('ParseStrategy', F+'parsestrategy')],
 sig='func parsePrices(_ inputs: [String]) -> [String]',
 statement="""Format styles also **parse**. For each user-typed price, try `Decimal.FormatStyle.Currency(code: "USD", locale: en_US).parseStrategy` and then plain `Double(input)`; return the parsed value in cents (`Int`) or `"invalid"`. Use `Decimal` to avoid binary rounding.""",
 solution="""
 import Foundation

 func parsePrices(_ inputs: [String]) -> [String] {
     let currency = Decimal.FormatStyle.Currency(code: "USD", locale: Locale(identifier: "en_US"))
     return inputs.map { input in
         let trimmed = input.trimmingCharacters(in: .whitespaces)
         let value = (try? currency.parseStrategy.parse(trimmed)) ?? Decimal(string: trimmed, locale: Locale(identifier: "en_US_POSIX"))
         guard let value else { return "invalid" }
         var cents = value * 100
         var rounded = Decimal()
         NSDecimalRound(&rounded, &cents, 0, .plain)
         return "\\(NSDecimalNumber(decimal: rounded).intValue)"
     }
 }
 """,
 explain="""Parsing is the inverse of formatting: `style.parseStrategy.parse(_:)` understands `$1,234.50` in `en_US`. `Decimal` stores base-10 digits, so `19.99 × 100` is exactly `1999` — use it for money, never `Double`.""",
 hints=("A currency format style has a `parseStrategy` that reads `$1,234.50`.","Fall back to `Decimal(string:locale:)` for plain numbers.","Multiply by 100 and round a `Decimal` with `NSDecimalRound`."),
 tests=[{'inputs':['$1,234.50','19.99','  $0.07 ','abc','$-5.00']}, {'inputs':[]}], hidden=0))
# ---------------- dates
P.append(dict(id='date-components-math', title='Calendar Math: Adding Months Safely', topic='Dates & calendars', diff='medium', platforms=MAC, concepts=['fundamental-types','optionals'], docs=[('Calendar', F+'calendar'), ('DateComponents', F+'datecomponents')],
 sig='func addMonths(_ isoDates: [String], months: Int) -> [String]',
 statement="""Adding "one month" isn't adding 30 days. With a Gregorian calendar in **UTC**, add `months` to each ISO date (`yyyy-MM-dd`) using `calendar.date(byAdding: .month, …)`, and return the result as `yyyy-MM-dd` plus the weekday name (`en_US_POSIX`). Watch Jan 31 + 1 month.""",
 solution="""
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
         return "\\(formatter.string(from: result)) \\(weekday.string(from: result))"
     }
 }
 """,
 explain="""`Calendar` handles month lengths, leap years and DST; `date(byAdding: .month)` clamps Jan 31 → Feb 28/29. Always set the calendar's `timeZone` and a POSIX locale for fixed-format parsing, or results change with the user's settings.""",
 hints=("Let `Calendar` do date math — never add seconds for months.","Configure a Gregorian calendar and `DateFormatter` with UTC and `en_US_POSIX`.","`calendar.date(byAdding: .month, value: months, to: date)`."),
 tests=[{'isoDates':['2024-01-31','2023-01-31','2024-12-15','bad'],'months':1}, {'isoDates':['2024-03-31'],'months':-1}, {'isoDates':[],'months':3}], hidden=0))
P.append(dict(id='days-between', title='Days Between Dates & Age Calculation', topic='Dates & calendars', platforms=MAC, concepts=['fundamental-types','tuples'], docs=[('Calendar.dateComponents(_:from:to:)', F+'calendar')],
 sig='func dateFacts(birth: String, today: String) -> [Int]',
 statement="""Given ISO dates (UTC), return `[age in whole years, days lived, days until next birthday]` using `calendar.dateComponents([.year], from:to:)`, `[.day]`, and `nextDate(after:matching:matchingPolicy:)` for the next birthday (Feb 29 birthdays → use `.nextTimePreservingSmallerComponents`). If today **is** the birthday, days until next is 0.""",
 solution="""
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
 """,
 explain="""`dateComponents(_:from:to:)` measures elapsed calendar units correctly (years aren't 365 days). `nextDate(after:matching:)` searches forward for the next matching month/day and a matching policy decides what happens on Feb 29 in non-leap years.""",
 hints=("Ask the calendar for the difference in `.year` and `.day` components.","Extract `[.month, .day]` from the birth date and search forward with `nextDate(after:matching:matchingPolicy:)`.","Handle \"today is the birthday\" as 0 days."),
 tests=[{'birth':'1990-06-15','today':'2024-06-14'}, {'birth':'2000-02-29','today':'2023-03-01'}, {'birth':'2010-01-01','today':'2010-01-01'}, {'birth':'bad','today':'2024-01-01'}], hidden=0))
P.append(dict(id='iso8601-timezones', title='ISO 8601 & Time Zones', topic='Dates & calendars', diff='medium', platforms=MAC, concepts=['fundamental-types','codable'], docs=[('Date.ISO8601FormatStyle', F+'date/iso8601formatstyle'), ('TimeZone', F+'timezone')],
 sig='func localTimes(_ timestamps: [String], zones: [String]) -> [String]',
 statement="""Parse each ISO 8601 timestamp (with offset, e.g. `2024-03-10T01:30:00-08:00`) using `Date.ISO8601FormatStyle`, then show it in each named zone as `"HH:mm zzz"` via a `DateFormatter` (`en_US_POSIX`). Return one line per timestamp: zone renderings joined by ` / `, or `"invalid"`.""",
 solution="""
 import Foundation

 func localTimes(_ timestamps: [String], zones: [String]) -> [String] {
     timestamps.map { ts in
         guard let date = try? Date(ts, strategy: .iso8601) else { return "invalid" }
         return zones.compactMap { TimeZone(identifier: $0) }.map { zone in
             let f = DateFormatter()
             f.locale = Locale(identifier: "en_US_POSIX")
             f.timeZone = zone
             f.dateFormat = "HH:mm zzz"
             return f.string(from: date)
         }.joined(separator: " / ")
     }
 }
 """,
 explain="""A `Date` is an absolute instant — it has no time zone. Zones only matter when parsing or displaying. Storing and transmitting ISO 8601 with an offset (or UTC `Z`) avoids ambiguity; display converts to the viewer's zone.""",
 hints=("`Date(ts, strategy: .iso8601)` parses timestamps with offsets.","A `Date` has no zone; set `DateFormatter.timeZone` to render it in one.","Format with `HH:mm zzz` for each `TimeZone(identifier:)`."),
 tests=[{'timestamps':['2024-03-10T01:30:00-08:00','2024-07-01T12:00:00Z','yesterday'],'zones':['UTC','America/New_York','Asia/Kolkata']}, {'timestamps':[],'zones':['UTC']}], hidden=0))
P.append(dict(id='date-interval-overlap', title='DateInterval: Meeting Overlaps', topic='Dates & calendars', diff='medium', platforms=MAC, concepts=['optionals','sort-custom'], docs=[('DateInterval', F+'dateinterval')],
 sig='func conflicts(_ meetings: [[Int]]) -> [String]',
 statement="""Meetings are `[startMinute, durationMinutes]` on one day (minutes after midnight UTC). Build `DateInterval`s and report every overlapping pair `"i-j <minutes>"` (indices, overlap length in minutes, via `intersection(with:)`). Back-to-back meetings (end == start) don't conflict.""",
 solution="""
 import Foundation

 func conflicts(_ meetings: [[Int]]) -> [String] {
     let day = Date(timeIntervalSince1970: 0)
     let intervals = meetings.map { DateInterval(start: day.addingTimeInterval(Double($0[0] * 60)), duration: Double($0[1] * 60)) }
     var out: [String] = []
     for i in intervals.indices {
         for j in intervals.indices where j > i {
             if let overlap = intervals[i].intersection(with: intervals[j]), overlap.duration > 0 {
                 out.append("\\(i)-\\(j) \\(Int(overlap.duration / 60))")
             }
         }
     }
     return out
 }
 """,
 explain="""`DateInterval` bundles start + duration with `intersects`, `intersection(with:)` and `contains`. Note the intersection of back-to-back intervals is zero-length (they share an endpoint), so check the duration, not just non-nil.""",
 hints=("Build a `DateInterval` per meeting from a fixed reference date.","Compare each pair with `intersection(with:)`.","Only count overlaps with `duration > 0`."),
 tests=[({'meetings':[[540,60],[570,30],[600,30],[700,15]]},['0-1 30']), {'meetings':[]}, {'meetings':[[0,120],[30,30],[60,90]]}]))
# ---------------- Codable advanced
P.append(dict(id='codable-dates-strategies', title='Codable Date Strategies', topic='Codable', diff='medium', platforms=MAC, concepts=['codable','codable-keys'], docs=[('JSONDecoder.DateDecodingStrategy', F+'jsondecoder/datedecodingstrategy')],
 sig='func decodeEvents(_ json: String, strategy: String) -> [String]',
 statement="""Decode `[{"name": …, "at": …}]` into `struct Event: Decodable { let name: String; let at: Date }` using the chosen `dateDecodingStrategy`: `iso8601`, `secondsSince1970`, `millisecondsSince1970`, or `custom` (format `dd/MM/yyyy`, UTC). Return `"<name> <ISO 8601 of at>"` per event, or `["error"]`.""",
 solution="""
 import Foundation

 struct Event: Decodable {
     let name: String
     let at: Date
 }

 func decodeEvents(_ json: String, strategy: String) -> [String] {
     let decoder = JSONDecoder()
     switch strategy {
     case "iso8601": decoder.dateDecodingStrategy = .iso8601
     case "secondsSince1970": decoder.dateDecodingStrategy = .secondsSince1970
     case "millisecondsSince1970": decoder.dateDecodingStrategy = .millisecondsSince1970
     default:
         let f = DateFormatter()
         f.locale = Locale(identifier: "en_US_POSIX")
         f.timeZone = TimeZone(identifier: "UTC")
         f.dateFormat = "dd/MM/yyyy"
         decoder.dateDecodingStrategy = .formatted(f)
     }
     guard let events = try? decoder.decode([Event].self, from: Data(json.utf8)) else { return ["error"] }
     return events.map { "\\($0.name) \\($0.at.ISO8601Format())" }
 }
 """,
 explain="""JSON has no date type; APIs send strings or numbers. The decoder's `dateDecodingStrategy` converts them once, centrally, so your models keep a real `Date`. The default strategy expects seconds since **2001** (Apple's reference date) — a classic source of dates in the wrong decade.""",
 hints=("Set `decoder.dateDecodingStrategy` before decoding.","Use `.iso8601`, `.secondsSince1970`, `.millisecondsSince1970` or `.formatted(dateFormatter)`.","Render with `date.ISO8601Format()`."),
 tests=[({'json':'[{"name":"launch","at":"2024-05-01T10:00:00Z"}]','strategy':'iso8601'},['launch 2024-05-01T10:00:00Z']), {'json':'[{"name":"a","at":0},{"name":"b","at":86400}]','strategy':'secondsSince1970'}, {'json':'[{"name":"ms","at":1700000000000}]','strategy':'millisecondsSince1970'}, {'json':'[{"name":"uk","at":"25/12/2024"}]','strategy':'custom'}, {'json':'[{"name":"x","at":"nope"}]','strategy':'iso8601'}]))
P.append(dict(id='codable-unknown-enum', title='Decoding Unknown Enum Values Safely', topic='Codable', diff='medium', platforms=MAC, concepts=['codable','enums'], docs=[('Decodable', 'https://developer.apple.com/documentation/swift/decodable')],
 sig='func decodeOrders(_ json: String) -> [String]',
 statement="""Servers add new values over time. `enum Status: String, Decodable { case pending, shipped, delivered, unknown }` must decode **any** unexpected string as `.unknown` instead of failing the whole payload. Implement `init(from:)` on the enum. Decode `[{"id": 1, "status": "…"}]` and return `"<id>:<status>"`.""",
 solution="""
 import Foundation

 enum Status: String, Decodable {
     case pending, shipped, delivered, unknown

     init(from decoder: Decoder) throws {
         let raw = try decoder.singleValueContainer().decode(String.self)
         self = Status(rawValue: raw) ?? .unknown
     }
 }

 struct Order: Decodable {
     let id: Int
     let status: Status
 }

 func decodeOrders(_ json: String) -> [String] {
     guard let orders = try? JSONDecoder().decode([Order].self, from: Data(json.utf8)) else { return ["error"] }
     return orders.map { "\\($0.id):\\($0.status.rawValue)" }
 }
 """,
 explain="""Synthesised `Decodable` for a raw-value enum throws on unknown values, and one bad element fails the entire array. A custom single-value `init(from:)` with a fallback keeps old app versions working when the backend evolves — a must for shipped clients.""",
 hints=("One unexpected string shouldn't fail the whole decode.","Write `init(from:)` using a `singleValueContainer()`.","`self = Status(rawValue: raw) ?? .unknown`."),
 tests=[({'json':'[{"id":1,"status":"shipped"},{"id":2,"status":"lost_in_space"}]'},['1:shipped','2:unknown']), {'json':'[]'}, {'json':'[{"id":3}]'}]))
P.append(dict(id='codable-polymorphic', title='Polymorphic JSON with a Type Discriminator', topic='Codable', diff='hard', platforms=MAC, concepts=['codable','associated-values','codable-keys'], docs=[('Encoding and Decoding Custom Types', F+'encoding-and-decoding-custom-types')],
 sig='func feed(_ json: String) -> [String]',
 statement="""A feed mixes item kinds: `{"type": "text", "body": …}`, `{"type": "image", "url": …, "width": …}`, `{"type": "poll", "question": …, "options": [...]}`. Decode into `enum FeedItem: Decodable { case text(String), image(url: String, width: Int), poll(question: String, options: [String]) }` by reading `type` first. Unknown types decode as `.unsupported(type)`. Return `"text: …"`, `"image <width>px"`, `"poll … (<n> options)"`, `"unsupported <type>"`.""",
 solution="""
 import Foundation

 enum FeedItem: Decodable {
     case text(String)
     case image(url: String, width: Int)
     case poll(question: String, options: [String])
     case unsupported(String)

     enum CodingKeys: String, CodingKey { case type, body, url, width, question, options }

     init(from decoder: Decoder) throws {
         let c = try decoder.container(keyedBy: CodingKeys.self)
         let type = try c.decode(String.self, forKey: .type)
         switch type {
         case "text": self = .text(try c.decode(String.self, forKey: .body))
         case "image": self = .image(url: try c.decode(String.self, forKey: .url), width: try c.decode(Int.self, forKey: .width))
         case "poll": self = .poll(question: try c.decode(String.self, forKey: .question), options: try c.decode([String].self, forKey: .options))
         default: self = .unsupported(type)
         }
     }

     var summary: String {
         switch self {
         case .text(let body): "text: \\(body)"
         case .image(_, let width): "image \\(width)px"
         case let .poll(q, options): "poll \\(q) (\\(options.count) options)"
         case .unsupported(let t): "unsupported \\(t)"
         }
     }
 }

 func feed(_ json: String) -> [String] {
     guard let items = try? JSONDecoder().decode([FeedItem].self, from: Data(json.utf8)) else { return ["error"] }
     return items.map(\\.summary)
 }
 """,
 explain="""Heterogeneous JSON maps naturally onto an enum with associated values: decode the discriminator, then switch to decode the right payload. Compared with class hierarchies, the compiler forces every consumer to handle every case.""",
 hints=("Decode the `type` key first, then decide which other keys to read.","Use one `CodingKeys` enum containing every key any variant uses.","Map unknown types to `.unsupported(type)` rather than throwing."),
 tests=[({'json':'[{"type":"text","body":"hi"},{"type":"image","url":"a.png","width":640},{"type":"poll","question":"Tabs?","options":["y","n"]},{"type":"video"}]'},['text: hi','image 640px','poll Tabs? (2 options)','unsupported video']), {'json':'[]'}, {'json':'[{"type":"image","url":"x"}]'}]))
P.append(dict(id='codable-encode-snake-sorted', title='Encoding: snake_case, Sorted & Pretty', topic='Codable', platforms=MAC, concepts=['codable','codable-keys'], docs=[('JSONEncoder', F+'jsonencoder')],
 sig='func encodeProfile(name: String, followerCount: Int, isVerified: Bool, nickname: String?) -> String',
 statement="""Encode `struct Profile: Encodable { let name: String; let followerCount: Int; let isVerified: Bool; let nickname: String? }` with `keyEncodingStrategy = .convertToSnakeCase` and `outputFormatting = [.sortedKeys, .withoutEscapingSlashes]`. Return the JSON string. Note what happens to a `nil` optional.""",
 solution="""
 import Foundation

 struct Profile: Encodable {
     let name: String
     let followerCount: Int
     let isVerified: Bool
     let nickname: String?
 }

 func encodeProfile(name: String, followerCount: Int, isVerified: Bool, nickname: String?) -> String {
     let encoder = JSONEncoder()
     encoder.keyEncodingStrategy = .convertToSnakeCase
     encoder.outputFormatting = [.sortedKeys, .withoutEscapingSlashes]
     let data = (try? encoder.encode(Profile(name: name, followerCount: followerCount, isVerified: isVerified, nickname: nickname))) ?? Data()
     return String(decoding: data, as: UTF8.self)
 }
 """,
 explain="""Synthesised encoding **omits** nil optionals (it uses `encodeIfPresent`), rather than writing `null`. `.sortedKeys` makes output deterministic (great for tests and caching), and the snake-case strategy keeps Swift names idiomatic.""",
 hints=("Configure `keyEncodingStrategy` and `outputFormatting` on the encoder.","`.convertToSnakeCase` turns `followerCount` into `follower_count`.","Decode the `Data` result to a `String` with UTF-8."),
 tests=[{'name':'Ana','followerCount':120,'isVerified':True,'nickname':None}, {'name':'Bo/Co','followerCount':0,'isVerified':False,'nickname':'b'}]))
P.append(dict(id='codable-nested-unkeyed', title='Nested & Unkeyed Containers', topic='Codable', diff='hard', platforms=MAC, concepts=['codable','codable-keys'], docs=[('UnkeyedDecodingContainer', 'https://developer.apple.com/documentation/swift/unkeyeddecodingcontainer')],
 sig='func decodeChart(_ json: String) -> [String]',
 statement="""A charting API sends points as **arrays**, not objects, inside a nested envelope: `{"data": {"series": [{"label": "A", "points": [[0, 1.5], [1, 2.0]]}]}}`. Decode to `struct Series { let label: String; let points: [Point] }` where `struct Point: Decodable { let x: Int; let y: Double }` decodes from a two-element array via an **unkeyed container**. Return `"<label>: <sum of y> over <count> points"` per series.""",
 solution="""
 import Foundation

 struct Point: Decodable {
     let x: Int
     let y: Double

     init(from decoder: Decoder) throws {
         var c = try decoder.unkeyedContainer()
         x = try c.decode(Int.self)
         y = try c.decode(Double.self)
     }
 }

 struct Series: Decodable {
     let label: String
     let points: [Point]
 }

 struct Envelope: Decodable {
     let series: [Series]

     enum CodingKeys: String, CodingKey { case data }
     enum DataKeys: String, CodingKey { case series }

     init(from decoder: Decoder) throws {
         let root = try decoder.container(keyedBy: CodingKeys.self)
         let data = try root.nestedContainer(keyedBy: DataKeys.self, forKey: .data)
         series = try data.decode([Series].self, forKey: .series)
     }
 }

 func decodeChart(_ json: String) -> [String] {
     guard let env = try? JSONDecoder().decode(Envelope.self, from: Data(json.utf8)) else { return ["error"] }
     return env.series.map { "\\($0.label): \\($0.points.reduce(0) { $0 + $1.y }) over \\($0.points.count) points" }
 }
 """,
 explain="""An unkeyed container reads array elements **in order** — ideal for compact tuple-like payloads. A nested keyed container skips the wrapper object without an extra wrapper struct.""",
 hints=("A point is a JSON array, so decode it with `unkeyedContainer()` in order.","Skip the `data` wrapper with `nestedContainer(keyedBy:forKey:)`.","`var c = try decoder.unkeyedContainer(); x = try c.decode(Int.self); y = try c.decode(Double.self)`."),
 tests=[({'json':'{"data":{"series":[{"label":"A","points":[[0,1.5],[1,2.0]]},{"label":"B","points":[]}]}}'},['A: 3.5 over 2 points','B: 0.0 over 0 points']), {'json':'{"data":{"series":[]}}'}, {'json':'{"data":{"series":[{"label":"C","points":[[0]]}]}}'}]))
# ---------------- URLs & networking
P.append(dict(id='url-components-builder', title='Building URLs with URLComponents', topic='Networking', platforms=MAC, concepts=['optionals','fundamental-types'], docs=[('URLComponents', F+'urlcomponents'), ('URLQueryItem', F+'urlqueryitem')],
 sig='func searchURL(query: String, page: Int, filters: [String]) -> String',
 statement="""Build `https://api.example.com/v1/search` with query items `q=<query>`, `page=<page>` (only if > 1) and one `filter=<f>` item per filter, **in that order**. Let `URLComponents` do the percent-encoding (spaces, `&`, emoji). Return `url.absoluteString`.""",
 solution="""
 import Foundation

 func searchURL(query: String, page: Int, filters: [String]) -> String {
     var c = URLComponents()
     c.scheme = "https"
     c.host = "api.example.com"
     c.path = "/v1/search"
     var items = [URLQueryItem(name: "q", value: query)]
     if page > 1 { items.append(URLQueryItem(name: "page", value: String(page))) }
     items += filters.map { URLQueryItem(name: "filter", value: $0) }
     c.queryItems = items
     return c.url?.absoluteString ?? "invalid"
 }
 """,
 explain="""String-concatenating URLs breaks on spaces, `&` and non-ASCII. `URLComponents` percent-encodes each part correctly and supports repeated keys. (Note: it leaves `+` unencoded in queries, which some servers read as a space — encode it yourself if your API needs that.)""",
 hints=("Never build URLs with string interpolation — use `URLComponents`.","Set scheme, host, path and `queryItems` (an array, so order and repeats are kept).","Only add `page` when it's greater than 1."),
 tests=[{'query':'swift & ios','page':1,'filters':[]}, {'query':'café 🦅','page':3,'filters':['video','new']}, {'query':'','page':2,'filters':['a b']}]))
P.append(dict(id='urlsession-get-decode', title='URLSession: GET & Decode (Mocked)', topic='Networking', diff='medium', platforms=MAC, concepts=['async-await','codable','error-handling'], docs=[('URLSession', F+'urlsession'), ('Fetching website data into memory', F+'fetching-website-data-into-memory')],
 sig='func loadUsers(status: Int, body: String) async -> [String]',
 statement="""Swiftful's *Download JSON from API*. Write `func fetchUsers(session: URLSession) async throws -> [User]` calling `GET https://api.example.com/users`, checking the response is an `HTTPURLResponse` with a 2xx status (else throw `APIError.badStatus(code)`), and decoding `[User]` (`id`, `name`).

 The judge wires a **mock `URLProtocol`** (given in the starter) so no real network is used. Return user names, or `"error <APIError or decoding>"`.""",
 starter="import Foundation\n"+MOCK+"""
 struct User: Decodable { let id: Int; let name: String }
 enum APIError: Error { case badStatus(Int) }

 func fetchUsers(session: URLSession) async throws -> [User] {
     return []
 }

 func loadUsers(status: Int, body: String) async -> [String] {
     MockURLProtocol.routes = ["GET /users": (status, body)]
     do {
         return try await fetchUsers(session: mockSession()).map(\\.name)
     } catch let error as APIError {
         return ["error \\(error)"]
     } catch {
         return ["error decoding"]
     }
 }
 """,
 solution="import Foundation\n"+MOCK+"""
 struct User: Decodable { let id: Int; let name: String }
 enum APIError: Error { case badStatus(Int) }

 func fetchUsers(session: URLSession) async throws -> [User] {
     let url = URL(string: "https://api.example.com/users")!
     let (data, response) = try await session.data(from: url)
     guard let http = response as? HTTPURLResponse else { throw APIError.badStatus(-1) }
     guard (200..<300).contains(http.statusCode) else { throw APIError.badStatus(http.statusCode) }
     return try JSONDecoder().decode([User].self, from: data)
 }

 func loadUsers(status: Int, body: String) async -> [String] {
     MockURLProtocol.routes = ["GET /users": (status, body)]
     do {
         return try await fetchUsers(session: mockSession()).map(\\.name)
     } catch let error as APIError {
         return ["error \\(error)"]
     } catch {
         return ["error decoding"]
     }
 }
 """,
 explain="""`session.data(from:)` doesn't throw for 404 or 500 — only for transport failures. You must check `HTTPURLResponse.statusCode` yourself. Injecting the `URLSession` (instead of using `.shared` inside) is what makes this testable with a `URLProtocol` mock.""",
 hints=("`try await session.data(from: url)` returns `(Data, URLResponse)`.","Cast to `HTTPURLResponse` and check `200..<300` — a 404 is not a thrown error.","Decode `[User]` with `JSONDecoder` after the status check."),
 tests=[({'status':200,'body':'[{"id":1,"name":"Ana"},{"id":2,"name":"Bo"}]'},['Ana','Bo']), ({'status':500,'body':'{}'},['error badStatus(500)']), {'status':200,'body':'not json'}, {'status':204,'body':'[]'}]))
P.append(dict(id='urlsession-post-json', title='URLRequest: POST JSON & Headers (Mocked)', topic='Networking', diff='medium', platforms=MAC, concepts=['codable','async-await'], docs=[('URLRequest', F+'urlrequest')],
 sig='func createTodo(title: String, token: String) async -> [String]',
 statement="""Build a `URLRequest` for `POST https://api.example.com/todos` with `Content-Type: application/json`, `Authorization: Bearer <token>`, and a JSON body encoded from `struct NewTodo: Encodable { let title: String; let done: Bool }` (`done: false`). Send it with `session.data(for:)` and decode the response `{"id": …}`.

 Return `[method, content-type header, authorization header, body as sorted-keys JSON, "id <n>"]` — the mock (given) echoes the request so you can verify it.""",
 starter="""import Foundation

 final class EchoURLProtocol: URLProtocol, @unchecked Sendable {
     nonisolated(unsafe) static var last: URLRequest?
     nonisolated(unsafe) static var lastBody = Data()
     override class func canInit(with request: URLRequest) -> Bool { true }
     override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
     override func startLoading() {
         EchoURLProtocol.last = request
         if let stream = request.httpBodyStream {
             stream.open(); var data = Data(); var buffer = [UInt8](repeating: 0, count: 1024)
             while stream.hasBytesAvailable { let n = stream.read(&buffer, maxLength: 1024); if n <= 0 { break }; data.append(buffer, count: n) }
             stream.close(); EchoURLProtocol.lastBody = data
         } else { EchoURLProtocol.lastBody = request.httpBody ?? Data() }
         let response = HTTPURLResponse(url: request.url!, statusCode: 201, httpVersion: nil, headerFields: nil)!
         client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
         client?.urlProtocol(self, didLoad: Data("{\\"id\\": 42}".utf8))
         client?.urlProtocolDidFinishLoading(self)
     }
     override func stopLoading() {}
 }

 struct NewTodo: Encodable { let title: String; let done: Bool }
 struct Created: Decodable { let id: Int }

 func createTodo(title: String, token: String) async -> [String] {
     let config = URLSessionConfiguration.ephemeral
     config.protocolClasses = [EchoURLProtocol.self]
     let session = URLSession(configuration: config)
     // build the request, send it, decode Created
     return []
 }
 """,
 solution="""import Foundation

 final class EchoURLProtocol: URLProtocol, @unchecked Sendable {
     nonisolated(unsafe) static var last: URLRequest?
     nonisolated(unsafe) static var lastBody = Data()
     override class func canInit(with request: URLRequest) -> Bool { true }
     override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
     override func startLoading() {
         EchoURLProtocol.last = request
         if let stream = request.httpBodyStream {
             stream.open(); var data = Data(); var buffer = [UInt8](repeating: 0, count: 1024)
             while stream.hasBytesAvailable { let n = stream.read(&buffer, maxLength: 1024); if n <= 0 { break }; data.append(buffer, count: n) }
             stream.close(); EchoURLProtocol.lastBody = data
         } else { EchoURLProtocol.lastBody = request.httpBody ?? Data() }
         let response = HTTPURLResponse(url: request.url!, statusCode: 201, httpVersion: nil, headerFields: nil)!
         client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
         client?.urlProtocol(self, didLoad: Data("{\\"id\\": 42}".utf8))
         client?.urlProtocolDidFinishLoading(self)
     }
     override func stopLoading() {}
 }

 struct NewTodo: Encodable { let title: String; let done: Bool }
 struct Created: Decodable { let id: Int }

 func createTodo(title: String, token: String) async -> [String] {
     let config = URLSessionConfiguration.ephemeral
     config.protocolClasses = [EchoURLProtocol.self]
     let session = URLSession(configuration: config)

     var request = URLRequest(url: URL(string: "https://api.example.com/todos")!)
     request.httpMethod = "POST"
     request.setValue("application/json", forHTTPHeaderField: "Content-Type")
     request.setValue("Bearer \\(token)", forHTTPHeaderField: "Authorization")
     let encoder = JSONEncoder()
     encoder.outputFormatting = .sortedKeys
     request.httpBody = try? encoder.encode(NewTodo(title: title, done: false))

     guard let (data, _) = try? await session.data(for: request),
           let created = try? JSONDecoder().decode(Created.self, from: data),
           let sent = EchoURLProtocol.last else { return ["failed"] }
     return [
         sent.httpMethod ?? "",
         sent.value(forHTTPHeaderField: "Content-Type") ?? "",
         sent.value(forHTTPHeaderField: "Authorization") ?? "",
         String(decoding: EchoURLProtocol.lastBody, as: UTF8.self),
         "id \\(created.id)",
     ]
 }
 """,
 explain="""`URLRequest` carries method, headers and body; `session.data(for:)` sends it. Encoding the body from an `Encodable` struct keeps request shapes type-checked. (Inside a `URLProtocol`, bodies may arrive as a stream — that's why the mock reads `httpBodyStream`.)""",
 hints=("Configure a `URLRequest`: `httpMethod`, `setValue(_:forHTTPHeaderField:)`, `httpBody`.","Encode `NewTodo` with a sorted-keys `JSONEncoder` as the body.","Send with `session.data(for: request)` and decode `Created`."),
 tests=[{'title':'buy milk','token':'abc123'}, {'title':'','token':'t'}]))
P.append(dict(id='retry-with-backoff', title='Retrying Requests with Backoff', topic='Networking', diff='hard', platforms=MAC, concepts=['async-await','error-handling','generics'], docs=[('Task.sleep(for:)', 'https://developer.apple.com/documentation/swift/task/sleep(for:tolerance:clock:)')],
 sig='func retrying(failuresBeforeSuccess: Int, maxAttempts: Int) async -> [String]',
 statement="""Write a generic `func retry<T>(maxAttempts: Int, baseDelayMs: Int, isRetryable: (Error) -> Bool, _ operation: () async throws -> T) async throws -> T` with exponential backoff (`base × 2^(attempt−1)` ms, use a tiny base like 1 ms). Only `TransientError` is retryable.

 The operation fails with `TransientError` for the first `failuresBeforeSuccess` calls, then returns `"ok"`. Return `[result or "gave up", "attempts <n>", delays joined by ","]`.""",
 solution="""
 struct TransientError: Error {}

 final class Recorder: @unchecked Sendable {
     var attempts = 0
     var delays: [Int] = []
 }

 func retry<T>(
     maxAttempts: Int,
     baseDelayMs: Int,
     recorder: Recorder,
     isRetryable: (Error) -> Bool,
     _ operation: () async throws -> T
 ) async throws -> T {
     var attempt = 1
     while true {
         do {
             return try await operation()
         } catch where attempt < maxAttempts && isRetryable(error) {
             let delay = baseDelayMs * (1 << (attempt - 1))
             recorder.delays.append(delay)
             try await Task.sleep(for: .milliseconds(delay))
             attempt += 1
         }
     }
 }

 func retrying(failuresBeforeSuccess: Int, maxAttempts: Int) async -> [String] {
     let recorder = Recorder()
     let result: String
     do {
         result = try await retry(maxAttempts: maxAttempts, baseDelayMs: 1, recorder: recorder, isRetryable: { $0 is TransientError }) {
             recorder.attempts += 1
             if recorder.attempts <= failuresBeforeSuccess { throw TransientError() }
             return "ok"
         }
     } catch {
         result = "gave up"
     }
     return [result, "attempts \\(recorder.attempts)", recorder.delays.map(String.init).joined(separator: ",")]
 }
 """,
 explain="""`catch where …` retries only retryable errors while attempts remain; anything else propagates immediately. Exponential backoff (1, 2, 4, 8…) avoids hammering a struggling server; production code also adds jitter and respects `Retry-After`.""",
 hints=("Loop: try the operation, and on a retryable error sleep then try again.","`catch where attempt < maxAttempts && isRetryable(error)` retries; otherwise the error escapes.","Delay = `base * (1 << (attempt - 1))`."),
 tests=[({'failuresBeforeSuccess':2,'maxAttempts':5},['ok','attempts 3','1,2']), ({'failuresBeforeSuccess':9,'maxAttempts':3},['gave up','attempts 3','1,2']), {'failuresBeforeSuccess':0,'maxAttempts':1}]))
P[-1]['statement'] = P[-1]['statement'].replace("func retry<T>(maxAttempts: Int, baseDelayMs: Int, isRetryable: (Error) -> Bool, _ operation: () async throws -> T) async throws -> T","func retry<T>(maxAttempts: Int, baseDelayMs: Int, recorder: Recorder, isRetryable: (Error) -> Bool, _ operation: () async throws -> T) async throws -> T")
P.append(dict(id='concurrent-downloads', title='Concurrent Downloads with a Task Group (Mocked)', topic='Networking', diff='hard', platforms=MAC, concepts=['task-group','async-await','codable'], docs=[('URLSession', F+'urlsession')],
 sig='func loadProfiles(_ ids: [Int], failing: [Int]) async -> [String]',
 statement="""Fetch `GET /users/<id>` for every id **concurrently** (task group), decoding `{"name": …}`. Failed requests (status ≥ 400, set up via `failing`) should not cancel the others: return per id, **in input order**, `"<id>: <name>"` or `"<id>: failed"`. The mock server (given) serves the routes.""",
 starter="import Foundation\n"+MOCK+"""
 struct Profile: Decodable { let name: String }

 func loadProfiles(_ ids: [Int], failing: [Int]) async -> [String] {
     MockURLProtocol.routes = [:]
     for id in ids { MockURLProtocol.routes["GET /users/\\(id)"] = failing.contains(id) ? (500, "{}") : (200, "{\\"name\\": \\"user\\(id)\\"}") }
     let session = mockSession()
     // fetch all concurrently, keep input order
     return []
 }
 """,
 solution="import Foundation\n"+MOCK+"""
 struct Profile: Decodable { let name: String }

 func fetchProfile(_ id: Int, session: URLSession) async -> String? {
     guard let (data, response) = try? await session.data(from: URL(string: "https://api.example.com/users/\\(id)")!),
           let http = response as? HTTPURLResponse, http.statusCode < 400,
           let profile = try? JSONDecoder().decode(Profile.self, from: data) else { return nil }
     return profile.name
 }

 func loadProfiles(_ ids: [Int], failing: [Int]) async -> [String] {
     MockURLProtocol.routes = [:]
     for id in ids { MockURLProtocol.routes["GET /users/\\(id)"] = failing.contains(id) ? (500, "{}") : (200, "{\\"name\\": \\"user\\(id)\\"}") }
     let session = mockSession()
     let names = await withTaskGroup(of: (Int, String?).self) { group in
         for (i, id) in ids.enumerated() {
             group.addTask { (i, await fetchProfile(id, session: session)) }
         }
         var results = [String?](repeating: nil, count: ids.count)
         for await (i, name) in group { results[i] = name }
         return results
     }
     return zip(ids, names).map { "\\($0): \\($1 ?? "failed")" }
 }
 """,
 explain="""Making each child task return an **optional** (instead of throwing) isolates failures: one bad request doesn't cancel the group. Tagging results with their index restores input order, because task groups deliver results in completion order.""",
 hints=("Spawn one child task per id; carry the index with the result.","Have each child return `String?` so failures don't cancel siblings.","Put results into an array by index, then format with the ids."),
 tests=[({'ids':[1,2,3],'failing':[2]},['1: user1','2: failed','3: user3']), {'ids':[],'failing':[]}, {'ids':[5,5],'failing':[]}]))
P.append(dict(id='nscache-image-cache', title='NSCache: Memory Cache with Limits', topic='Persistence & caching', diff='medium', platforms=MAC, concepts=['caching','class-definition','generics'], docs=[('NSCache', F+'nscache')],
 sig='func cacheRun(countLimit: Int, ops: [String]) -> [String]',
 statement="""Swiftful's *Download and save images using FileManager and NSCache*. Wrap `NSCache<NSString, Entry>` (keys must be `NSString`, values class instances) in a generic-ish `final class DataCache` with `countLimit`. Ops: `put <key> <value>`, `get <key>` (logs value or `"miss"`), `remove <key>`, `clear`. `NSCache` may evict early under memory pressure, so the judge only checks behaviour that's guaranteed: explicit removal, clearing, and hits for keys still present when well under the limit.""",
 solution="""
 import Foundation

 final class Entry {
     let value: String
     init(_ value: String) { self.value = value }
 }

 final class DataCache {
     private let cache = NSCache<NSString, Entry>()
     init(countLimit: Int) { cache.countLimit = countLimit }
     func put(_ value: String, for key: String) { cache.setObject(Entry(value), forKey: key as NSString) }
     func get(_ key: String) -> String? { cache.object(forKey: key as NSString)?.value }
     func remove(_ key: String) { cache.removeObject(forKey: key as NSString) }
     func clear() { cache.removeAllObjects() }
 }

 func cacheRun(countLimit: Int, ops: [String]) -> [String] {
     let cache = DataCache(countLimit: countLimit)
     var log: [String] = []
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch p[0] {
         case "put" where p.count == 3: cache.put(p[2], for: p[1])
         case "get" where p.count == 2: log.append(cache.get(p[1]) ?? "miss")
         case "remove" where p.count == 2: cache.remove(p[1])
         case "clear": cache.clear()
         default: break
         }
     }
     return log
 }
 """,
 explain="""`NSCache` is thread-safe and evicts automatically under memory pressure — perfect for images and derived data, never for anything you can't recompute. Its limits are **hints**, not guarantees, so tests must not depend on exact eviction. Keys are `NSString` because it's an Objective-C class.""",
 hints=("`NSCache` needs class keys and values — bridge `String` to `NSString`.","Wrap it so callers use plain `String`s.","Use `setObject(_:forKey:)`, `object(forKey:)`, `removeObject(forKey:)`, `removeAllObjects()`."),
 tests=[({'countLimit':10,'ops':['put a 1','put b 2','get a','remove a','get a','get b','clear','get b']},['1','miss','2','miss']), {'countLimit':5,'ops':[]}, {'countLimit':50,'ops':['get x','put x 9','get x']}]))
P.append(dict(id='userdefaults-wrapper', title='UserDefaults with a Typed Wrapper', topic='Persistence & caching', diff='medium', platforms=MAC, concepts=['property-wrappers','generics','codable'], docs=[('UserDefaults', F+'userdefaults')],
 sig='func settingsRoundTrip(_ writes: [String]) -> [String]',
 statement="""Write `@propertyWrapper struct Stored<Value: Codable>` backed by `UserDefaults` (JSON-encoded under a key, with a default). Use it in `struct Preferences { @Stored("theme", default: "system") var theme: String; @Stored("fontSize", default: 14) var fontSize: Int; @Stored("recent", default: []) var recent: [String] }` with a **private suite** `UserDefaults(suiteName:)` (cleared first).

 Writes: `theme=<v>`, `font=<n>`, `recent=<v>` (prepend, keep 3). After all writes, create a **new** `Preferences` (simulating a relaunch) and return its values.""",
 solution="""
 import Foundation

 // A suite named by an absolute path is a private plist file: one per process, in the temp
 // directory, so parallel runs never clobber each other and ~/Library/Preferences stays clean.
 let suiteName = NSTemporaryDirectory() + "swift-judge-stored-\\(ProcessInfo.processInfo.processIdentifier)"

 @propertyWrapper
 struct Stored<Value: Codable> {
     let key: String
     let defaultValue: Value
     let store: UserDefaults

     init(_ key: String, default defaultValue: Value, store: UserDefaults = UserDefaults(suiteName: suiteName)!) {
         self.key = key
         self.defaultValue = defaultValue
         self.store = store
     }

     var wrappedValue: Value {
         get {
             guard let data = store.data(forKey: key), let value = try? JSONDecoder().decode(Value.self, from: data) else { return defaultValue }
             return value
         }
         set { store.set(try? JSONEncoder().encode(newValue), forKey: key) }
     }
 }

 struct Preferences {
     @Stored("theme", default: "system") var theme: String
     @Stored("fontSize", default: 14) var fontSize: Int
     @Stored("recent", default: []) var recent: [String]
 }

 func settingsRoundTrip(_ writes: [String]) -> [String] {
     UserDefaults(suiteName: suiteName)!.removePersistentDomain(forName: suiteName)
     var prefs = Preferences()
     for w in writes {
         let p = w.split(separator: "=", maxSplits: 1).map(String.init)
         guard p.count == 2 else { continue }
         switch p[0] {
         case "theme": prefs.theme = p[1]
         case "font": if let n = Int(p[1]) { prefs.fontSize = n }
         case "recent": prefs.recent = Array(([p[1]] + prefs.recent).prefix(3))
         default: break
         }
     }
     let relaunched = Preferences()
     let out = [relaunched.theme, String(relaunched.fontSize), relaunched.recent.joined(separator: ",")]
     UserDefaults(suiteName: suiteName)!.removePersistentDomain(forName: suiteName)
     try? FileManager.default.removeItem(atPath: suiteName + ".plist")
     return out
 }
 """,
 explain="""`UserDefaults` is a small key–value store for preferences. A generic `Codable` wrapper gives type safety and defaults in one place (SwiftUI's `@AppStorage` is the view-aware version). Injecting a suite keeps tests isolated from real settings.""",
 hints=("A property wrapper can read and write `UserDefaults` in its `wrappedValue`.","Encode values as JSON `Data` so any `Codable` type works; return the default when missing.","A fresh `Preferences()` reads what the previous one saved."),
 tests=[({'writes':['theme=dark','font=18','recent=a','recent=b','recent=c','recent=d']},['dark','18','d,c,b']), {'writes':[]}, {'writes':['font=x','theme=light']}]))
write_all(P, 'frameworks', 100)
