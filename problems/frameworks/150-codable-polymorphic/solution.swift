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
        case .text(let body): "text: \(body)"
        case .image(_, let width): "image \(width)px"
        case let .poll(q, options): "poll \(q) (\(options.count) options)"
        case .unsupported(let t): "unsupported \(t)"
        }
    }
}

func feed(_ json: String) -> [String] {
    guard let items = try? JSONDecoder().decode([FeedItem].self, from: Data(json.utf8)) else { return ["error"] }
    return items.map(\.summary)
}
