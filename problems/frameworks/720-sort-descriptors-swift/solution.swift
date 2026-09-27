import Foundation

struct Player {
    let name: String
    let score: Int
    let country: String
}

func sortPlayers(_ rows: [[String]], by keys: [String]) -> [String] {
    let players = rows.map { Player(name: $0[0], score: Int($0[1]) ?? 0, country: $0[2]) }
    let descriptors: [SortDescriptor<Player>] = keys.compactMap { key in
        let descending = key.hasSuffix("-")
        let order: SortOrder = descending ? .reverse : .forward
        switch key.trimmingCharacters(in: CharacterSet(charactersIn: "-")) {
        case "score": return SortDescriptor(\.score, order: order)
        case "name": return SortDescriptor(\.name, comparator: .localizedStandard, order: order)
        case "country": return SortDescriptor(\.country, comparator: .localizedStandard, order: order)
        default: return nil
        }
    }
    return players.sorted(using: descriptors).map(\.name)
}
