import SwiftUI

enum Route: Hashable, Codable {
    case profile(id: Int)
    case settings
    case detail(String)
}

@MainActor func run(_ commands: [String]) -> [String] {
    var path = NavigationPath()
    var log: [String] = []
    for command in commands {
        let p = command.split(separator: " ").map(String.init)
        switch p[0] {
        case "push" where p.count >= 2:
            switch p[1] {
            case "profile": path.append(Route.profile(id: Int(p.last!) ?? 0))
            case "settings": path.append(Route.settings)
            default: path.append(Route.detail(p.last!))
            }
        case "pop": if !path.isEmpty { path.removeLast() }
        case "root": path = NavigationPath()
        case "save":
            if let codable = path.codable,
               let data = try? JSONEncoder().encode(codable),
               let decoded = try? JSONDecoder().decode(NavigationPath.CodableRepresentation.self, from: data) {
                path = NavigationPath(decoded)
                log.append("restored \(path.count)")
                continue
            }
        default: break
        }
        log.append("depth \(path.count)")
    }
    return log
}

func navigate(_ commands: [String]) async -> [String] {
    await run(commands)
}
