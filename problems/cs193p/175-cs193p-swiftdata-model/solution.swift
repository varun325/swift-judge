import SwiftData
import Foundation

@Model
final class AttemptRecord {
    var pegs: [String]
    var at: Date
    init(pegs: [String], at: Date) { self.pegs = pegs; self.at = at }
}

@Model
final class GameRecord {
    var name: String
    var pegChoices: [String]
    var lastAttempt: Date?
    @Transient var isSelected = false
    @Relationship(deleteRule: .cascade) var attempts: [AttemptRecord] = []
    init(name: String, pegChoices: [String]) { self.name = name; self.pegChoices = pegChoices }
}

@MainActor func run(_ ops: [String]) throws -> [String] {
    let container = try ModelContainer(for: GameRecord.self, AttemptRecord.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    func game(_ name: String) throws -> GameRecord? {
        try context.fetch(FetchDescriptor<GameRecord>(predicate: #Predicate { $0.name == name })).first
    }
    for op in ops {
        let p = op.split(separator: " ").map(String.init)
        switch (p.first ?? "", p.count) {
        case ("game", 3): context.insert(GameRecord(name: p[1], pegChoices: p[2].map(String.init)))
        case ("attempt", 4):
            guard let g = try game(p[1]) else { break }
            let at = Date(timeIntervalSinceReferenceDate: (Double(p[3]) ?? 0) * 86_400)
            g.attempts.append(AttemptRecord(pegs: p[2].map(String.init), at: at))
            g.lastAttempt = at
        case ("select", 2): try game(p[1])?.isSelected = true
        case ("delete", 2): if let g = try game(p[1]) { context.delete(g) }
        default: break
        }
    }
    try context.save()
    let fresh = ModelContext(container)
    let games = try fresh.fetch(FetchDescriptor<GameRecord>(sortBy: [SortDescriptor(\.name)]))
        .sorted { ($0.lastAttempt ?? .distantPast, $1.name) > ($1.lastAttempt ?? .distantPast, $0.name) }
    return games.map { g in
        let day = g.lastAttempt.map { String(Int($0.timeIntervalSinceReferenceDate / 86_400)) } ?? "never"
        return "\(g.name): \(g.attempts.count) attempts, last \(day), selected \(g.isSelected)"
    }
}

func persistGames(_ ops: [String]) async -> [String] {
    (try? await run(ops)) ?? ["error"]
}
