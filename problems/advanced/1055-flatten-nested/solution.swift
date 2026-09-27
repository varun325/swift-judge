import Foundation

indirect enum Nested: Decodable {
    case value(Int)
    case list([Nested])

    init(from decoder: Decoder) throws {
        let c = try decoder.singleValueContainer()
        if let v = try? c.decode(Int.self) { self = .value(v) }
        else { self = .list(try c.decode([Nested].self)) }
    }

    var flattened: [Int] {
        switch self {
        case .value(let v): [v]
        case .list(let items): items.flatMap(\.flattened)
        }
    }
}

func flatten(_ json: String) -> [Int] {
    (try? JSONDecoder().decode(Nested.self, from: Data(json.utf8)))?.flattened ?? []
}
