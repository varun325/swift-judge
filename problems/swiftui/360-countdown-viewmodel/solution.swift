import Observation

@Observable
final class CountdownModel {
    let total: Int
    private(set) var remaining: Int
    private(set) var isRunning = false
    private(set) var finished = false

    init(seconds: Int) {
        total = seconds
        remaining = seconds
    }

    var display: String { "\(remaining / 60):\(remaining % 60 < 10 ? "0" : "")\(remaining % 60)" }

    func start() { if remaining > 0 { isRunning = true } }
    func pause() { isRunning = false }
    func reset() { remaining = total; isRunning = false; finished = false }

    func tick() {
        guard isRunning, remaining > 0 else { return }
        remaining -= 1
        if remaining == 0 { isRunning = false; finished = true }
    }
}

func countdown(seconds: Int, events: [String]) -> [String] {
    let model = CountdownModel(seconds: seconds)
    return events.map { e in
        switch e {
        case "start": model.start()
        case "pause": model.pause()
        case "reset": model.reset()
        default: model.tick()
        }
        return model.display + (model.finished ? " done" : "")
    }
}
