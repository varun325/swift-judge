func scrollTargets(ids: [String], commands: [String]) -> [String] {
    commands.map { c in
        let p = c.split(separator: " ", maxSplits: 1).map(String.init)
        let arg = p.count > 1 ? p[1] : ""
        let target: String?
        var anchor = "top"
        switch p[0] {
        case "bottom": target = ids.last; anchor = "bottom"
        case "top": target = ids.first
        case "unread":
            if let i = ids.firstIndex(of: arg), i + 1 < ids.count { target = ids[i + 1] } else { target = ids.last }
        default: target = ids.first { $0.localizedCaseInsensitiveContains(arg) }
        }
        return target.map { "\($0) @\(anchor)" } ?? "none"
    }
}

import Foundation
