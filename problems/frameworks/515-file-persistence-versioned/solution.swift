import Foundation

struct Store: Codable {
    var version: Int
    var todos: [String]
}

func persistTodos(_ sessions: [[String]]) -> [String] {
    let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
    try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
    defer { try? FileManager.default.removeItem(at: dir) }
    let file = dir.appendingPathComponent("store.json")
    var log: [String] = []
    for actions in sessions {
        var store = (try? JSONDecoder().decode(Store.self, from: Data(contentsOf: file))) ?? Store(version: 1, todos: [])
        var changed = false
        var corrupt = false
        for action in actions {
            let p = action.split(separator: " ", maxSplits: 1).map(String.init)
            switch p[0] {
            case "add" where p.count == 2: store.todos.append(p[1]); changed = true
            case "done" where p.count == 2:
                if let i = store.todos.firstIndex(of: p[1]) { store.todos.remove(at: i); changed = true }
            case "corrupt": corrupt = true
            default: break
            }
        }
        if changed { store.version += 1 }
        try? JSONEncoder().encode(store).write(to: file, options: .atomic)
        log.append("v\(store.version): \(store.todos.joined(separator: ","))")
        if corrupt { try? Data("{not json".utf8).write(to: file) }
    }
    return log
}
