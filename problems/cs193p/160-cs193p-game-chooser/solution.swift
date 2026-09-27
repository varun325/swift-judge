import Foundation

struct GameSummary: Identifiable, Hashable {
    let id = UUID()
    var name: String
    var theme: String

    static func == (a: GameSummary, b: GameSummary) -> Bool { a.id == b.id }
    func hash(into hasher: inout Hasher) { hasher.combine(id) }
}

func chooser(_ ops: [String]) -> [String] {
    var games: [GameSummary] = []
    var selection: GameSummary.ID?
    return ops.map { op in
        let p = op.split(separator: " ").map(String.init)
        func index(_ name: String) -> Int? { games.firstIndex { $0.name == name } }
        switch (p.first ?? "", p.count) {
        case ("add", 3): games.append(GameSummary(name: p[1], theme: p[2]))
        case ("rename", 3): if let i = index(p[1]) { games[i].name = p[2] }
        case ("select", 2): selection = index(p[1]).map { games[$0].id }
        case ("remove", 2):
            if let i = index(p[1]) {
                if games[i].id == selection { selection = nil }
                games.remove(at: i)
            }
        default: break
        }
        let selectedName = games.first { $0.id == selection }?.name ?? "none"
        return "\(games.map(\.name).joined(separator: ",")) | selected: \(selectedName)"
    }
}
