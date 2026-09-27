@globalActor
actor AnalyticsActor {
    static let shared = AnalyticsActor()
}

@AnalyticsActor
final class Tracker {
    var events: [String] = []
}

@AnalyticsActor
func log(_ event: String, to tracker: Tracker) {
    guard !event.isEmpty else { return }
    tracker.events.append(event)
}

@AnalyticsActor
func runAnalytics(_ events: [String]) -> [String] {
    let tracker = Tracker()
    for e in events { log(e, to: tracker) }
    return tracker.events + ["count \(tracker.events.count)"]
}

func analyticsDemo(_ events: [String]) async -> [String] {
    await runAnalytics(events)
}
