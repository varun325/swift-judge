enum Tab: String, CaseIterable { case home, search, inbox, profile }

func tabBar(_ events: [String]) -> [String] {
    var selected = Tab.home
    var badges: [Tab: Int] = [:]
    for e in events {
        let p = e.split(separator: " ").map(String.init)
        switch p[0] {
        case "select":
            guard p.count > 1, let tab = Tab(rawValue: p[1]) else { continue }
            selected = tab
            if tab == .inbox { badges[.inbox] = nil }
        case "notify":
            guard p.count > 2, let tab = Tab(rawValue: p[1]), let n = Int(p[2]) else { continue }
            badges[tab, default: 0] += n
        default:
            selected = .home
            badges.removeAll()
        }
    }
    return Tab.allCases.map { tab in
        let badge = badges[tab] ?? 0
        return "\(tab.rawValue)\(tab == selected ? "*" : "") \(badge == 0 ? "-" : String(badge))"
    }
}
