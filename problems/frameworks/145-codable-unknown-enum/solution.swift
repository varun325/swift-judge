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
    return orders.map { "\($0.id):\($0.status.rawValue)" }
}
