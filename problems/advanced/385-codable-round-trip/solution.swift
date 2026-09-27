import Foundation

enum Event: Codable, Equatable {
    case login(user: String)
    case purchase(item: String, cents: Int)
    case logout
}

func roundTrip(_ events: [String]) -> [String] {
    let parsed: [Event] = events.compactMap { spec in
        let p = spec.split(separator: " ").map(String.init)
        switch (p.first, p.count) {
        case ("login", 2): return .login(user: p[1])
        case ("purchase", 3): return Int(p[2]).map { .purchase(item: p[1], cents: $0) }
        case ("logout", 1): return .logout
        default: return nil
        }
    }
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.sortedKeys]
    guard let data = try? encoder.encode(parsed),
          let back = try? JSONDecoder().decode([Event].self, from: data) else { return ["failed"] }
    return [String(decoding: data, as: UTF8.self), back == parsed ? "equal" : "different"]
}
