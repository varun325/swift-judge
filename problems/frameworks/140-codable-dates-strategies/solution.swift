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
    return events.map { "\($0.name) \($0.at.ISO8601Format())" }
}
