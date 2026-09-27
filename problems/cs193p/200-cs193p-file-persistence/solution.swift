import Foundation

struct SavedGame: Codable, Equatable {
    var name: String
    var master: [String]
    var attempts: [[String]]
}

func saveAndLoad(_ games: [[String]]) -> [String] {
    let models = games.map { g in
        SavedGame(name: g[0], master: g[1].map(String.init), attempts: g[2].split(separator: ",").map { $0.map(String.init) })
    }
    let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
    defer { try? FileManager.default.removeItem(at: dir) }
    do {
        try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        let url = dir.appendingPathComponent("games.json")
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        let data = try encoder.encode(models)
        try data.write(to: url, options: .atomic)
        let loaded = try JSONDecoder().decode([SavedGame].self, from: Data(contentsOf: url))
        return ["\(data.count) bytes", "round trip \(loaded == models ? "equal" : "different")", loaded.map(\.name).joined(separator: ",")]
    } catch {
        return ["error \(error)"]
    }
}
