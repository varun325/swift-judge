enum AppPhase: String { case active, inactive, background }

func lifecycleSaves(_ phases: [String], edits: [Int]) -> [String] {
    var current = AppPhase.active
    var pending = 0
    return zip(phases, edits).map { raw, newEdits in
        pending += newEdits
        guard let next = AppPhase(rawValue: raw), next != current else { return "-" }
        defer { current = next }
        switch (current, next) {
        case (_, .background) where pending > 0:
            defer { pending = 0 }
            return "save \(pending)"
        case (.background, .active): return "refresh"
        default: return "-"
        }
    }
}
