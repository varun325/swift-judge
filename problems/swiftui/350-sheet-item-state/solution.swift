enum ActiveSheet: Identifiable {
    case settings, profile(Int), share(String)

    var id: String {
        switch self {
        case .settings: "settings"
        case .profile(let id): "profile-\(id)"
        case .share(let url): "share-\(url)"
        }
    }
}

func presentations(_ actions: [String]) -> [String] {
    var active: ActiveSheet?
    var log: [String] = []
    for action in actions {
        let p = action.split(separator: " ").map(String.init)
        if p[0] == "dismiss" {
            log.append(active.map { "dismiss \($0.id)" } ?? "nothing to dismiss")
            active = nil
            continue
        }
        let next: ActiveSheet? = switch (p.count > 1 ? p[1] : "", p.count > 2 ? p[2] : "") {
        case ("settings", _): .settings
        case ("profile", let n): Int(n).map(ActiveSheet.profile)
        case ("share", let url): .share(url)
        default: nil
        }
        guard let next else { continue }
        log.append(active.map { "replace \($0.id) with \(next.id)" } ?? "present \(next.id)")
        active = next
    }
    return log
}
