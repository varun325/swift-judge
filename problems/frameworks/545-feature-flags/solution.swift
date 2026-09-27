import Foundation

enum Flag: String, CaseIterable { case newCheckout, darkIcons, aiSearch }

struct RemoteFlag: Decodable {
    let enabled: Bool
    let rolloutPercent: Int?
}

func flags(remoteJSON: String, overrides: [String], userBucket: Int) -> [String] {
    let defaults: [Flag: Bool] = [.newCheckout: false, .darkIcons: true, .aiSearch: false]
    let remote = (try? JSONDecoder().decode([String: RemoteFlag].self, from: Data(remoteJSON.utf8))) ?? [:]
    let local = Dictionary(overrides.compactMap { o -> (String, Bool)? in
        let p = o.split(separator: "=").map(String.init)
        guard p.count == 2, p[1] == "on" || p[1] == "off" else { return nil }
        return (p[0], p[1] == "on")
    }, uniquingKeysWith: { _, last in last })
    return Flag.allCases.map { flag in
        if let o = local[flag.rawValue] { return "\(flag.rawValue)=\(o ? "on" : "off") (override)" }
        if let r = remote[flag.rawValue] {
            let on = r.enabled && userBucket < (r.rolloutPercent ?? 100)
            return "\(flag.rawValue)=\(on ? "on" : "off") (remote)"
        }
        return "\(flag.rawValue)=\(defaults[flag]! ? "on" : "off") (default)"
    }
}
