enum Phase: CaseIterable {
    case idle, lift, spin, drop
    var scale: Double { self == .lift || self == .spin ? 1.2 : 1 }
    var rotation: Int {
        switch self {
        case .idle, .lift: 0
        case .spin: 180
        case .drop: 360
        }
    }
}

func phaseTimeline(triggers: Int, durations: [Double]) -> [String] {
    var t = 0.0
    func line(_ p: Phase) -> String { "\((t * 10).rounded() / 10)s \(p) scale \(p.scale) rot \(p.rotation)" }
    var out = [line(.idle)]
    guard !durations.isEmpty else { return out }
    for _ in 0..<max(triggers, 0) {
        let sequence = Array(Phase.allCases.dropFirst()) + [.idle]
        for (i, phase) in sequence.enumerated() {
            t += durations[i % durations.count]
            out.append(line(phase))
        }
    }
    return out
}
