final class EventBus {
    private var handlers: [(String) -> Void] = []

    func subscribe(_ handler: @escaping (String) -> Void) {
        handlers.append(handler)
    }

    func publish(_ event: String) {
        for handler in handlers { handler(event) }
    }
}

final class Log { var lines: [String] = [] }

func eventBus(_ events: [String]) -> [String] {
    let bus = EventBus()
    let log = Log()
    bus.subscribe { log.lines.append("A:\($0)") }
    bus.subscribe { log.lines.append("B:\($0)") }
    events.forEach(bus.publish)
    return log.lines
}
