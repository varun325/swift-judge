import Foundation

enum Route: CustomStringConvertible {
    case profile(Int), post(Int), settings
    var description: String {
        switch self {
        case .profile(let id): "profile(\(id))"
        case .post(let id): "post(\(id))"
        case .settings: "settings"
        }
    }
}

func parse(_ link: String) -> (tab: String, routes: [Route])? {
    guard let c = URLComponents(string: link), c.scheme == "myapp", let host = c.host else { return nil }
    let parts = [host] + c.path.split(separator: "/").map(String.init)
    let tab = c.queryItems?.first { $0.name == "tab" }?.value ?? "home"
    switch parts.count {
    case 1 where parts[0] == "settings": return (tab, [.settings])
    case 2 where parts[0] == "profile": return Int(parts[1]).map { (tab, [.profile($0)]) }
    case 4 where parts[0] == "profile" && parts[2] == "posts":
        guard let id = Int(parts[1]), let post = Int(parts[3]) else { return nil }
        return (tab, [.profile(id), .post(post)])
    default: return nil
    }
}

func routes(_ links: [String]) -> [String] {
    links.map { link in
        guard let r = parse(link) else { return "invalid" }
        return "\(r.tab): \(r.routes.map(\.description).joined(separator: " > "))"
    }
}
