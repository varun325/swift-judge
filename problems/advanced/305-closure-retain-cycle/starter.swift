final class Log { var lines: [String] = [] }

final class Ticker {
    var count = 0
    var onTick: (() -> Void)?
    let log: Log
    init(log: Log) { self.log = log }

    func start() {
        onTick = {
            self.count += 1
            self.log.lines.append("tick \(self.count)")
        }
    }

    deinit { log.lines.append("deinit ticker") }
}

func timerDemo(ticks: Int) -> [String] {
    let log = Log()
    do {
        let ticker = Ticker(log: log)
        ticker.start()
        for _ in 0..<ticks { ticker.onTick?() }
    }
    log.lines.append("end")
    return log.lines
}
