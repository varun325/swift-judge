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
    return env.series.map { "\($0.label): \($0.points.reduce(0) { $0 + $1.y }) over \($0.points.count) points" }
}
