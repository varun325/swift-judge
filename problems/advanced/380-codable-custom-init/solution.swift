import Foundation

struct Product: Decodable {
    let name: String
    let priceCents: Int
    let tags: [String]

    enum CodingKeys: String, CodingKey { case info, price, tags }
    enum InfoKeys: String, CodingKey { case name }

    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        let info = try c.nestedContainer(keyedBy: InfoKeys.self, forKey: .info)
        name = try info.decode(String.self, forKey: .name)
        let price: Double
        if let d = try? c.decode(Double.self, forKey: .price) {
            price = d
        } else {
            let s = try c.decode(String.self, forKey: .price)
            guard let d = Double(s) else {
                throw DecodingError.dataCorruptedError(forKey: .price, in: c, debugDescription: "bad price \(s)")
            }
            price = d
        }
        priceCents = Int((price * 100).rounded())
        tags = try c.decodeIfPresent([String].self, forKey: .tags) ?? []
    }
}

func decodeProducts(_ json: String) -> [String] {
    do {
        let products = try JSONDecoder().decode([Product].self, from: Data(json.utf8))
        return products.map { "\($0.name) \($0.priceCents) [\($0.tags.joined(separator: ","))]" }
    } catch let error as DecodingError {
        let name = switch error {
        case .keyNotFound: "keyNotFound"
        case .typeMismatch: "typeMismatch"
        case .valueNotFound: "valueNotFound"
        case .dataCorrupted: "dataCorrupted"
        @unknown default: "unknown"
        }
        return ["error: \(name)"]
    } catch {
        return ["error: other"]
    }
}
