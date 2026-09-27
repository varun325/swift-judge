import SwiftData
import Foundation

@Model
final class Attempt {
    var exact: Int
    init(exact: Int) { self.exact = exact }
}

@Model
final class Game {
    var name: String
    var isComplete: Bool
    @Relationship(deleteRule: .cascade) var attempts: [Attempt] = []
    init(name: String, isComplete: Bool) { self.name = name; self.isComplete = isComplete }
}

@MainActor func run(_ specs: [[String]]) throws -> [String] {
    let container = try ModelContainer(for: Game.self, Attempt.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    for s in specs {
        let g = Game(name: s[0], isComplete: s[1] == "y")
        context.insert(g)
        g.attempts = s[2].split(separator: ",").compactMap { Int($0) }.map { Attempt(exact: $0) }
    }
    try context.save()
    let byName = [SortDescriptor(\Game.name)]
    let completed = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.isComplete }, sortBy: byName))
    let close = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.attempts.contains { $0.exact >= 3 } }, sortBy: byName))
    let quick = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.attempts.count <= 2 }, sortBy: byName))
    return [completed, close, quick].map { $0.map(\.name).joined(separator: ",") }
}

func gameQueries(_ games: [[String]]) async -> [String] {
    (try? await run(games)) ?? ["error"]
}
