import Foundation

struct GameClock {
    private(set) var elapsedBeforePause: TimeInterval = 0
    private(set) var startTime: Date?

    mutating func start(at now: Date) { if startTime == nil { startTime = now } }

    mutating func pause(at now: Date) {
        guard let start = startTime else { return }
        elapsedBeforePause += now.timeIntervalSince(start)
        startTime = nil
    }

    func elapsed(at now: Date) -> TimeInterval {
        elapsedBeforePause + (startTime.map { now.timeIntervalSince($0) } ?? 0)
    }
}

func elapsed(_ events: [[String]]) -> [String] {
    var clock = GameClock()
    var out: [String] = []
    let reference = Date(timeIntervalSinceReferenceDate: 0)
    for e in events {
        let now = reference.addingTimeInterval(Double(e[1]) ?? 0)
        switch e[0] {
        case "start": clock.start(at: now)
        case "pause": clock.pause(at: now)
        default:
            let total = Int(clock.elapsed(at: now))
            out.append("\(total / 60):\(total % 60 < 10 ? "0" : "")\(total % 60)")
        }
    }
    return out
}
