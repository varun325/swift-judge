func formatDurations(_ millis: [Int]) -> [String] {
    millis.map { ms in
        let d = Duration.milliseconds(ms) + .seconds(1)
        let (seconds, attoseconds) = d.components
        let totalMs = seconds * 1000 + attoseconds / 1_000_000_000_000_000
        return "\(totalMs / 60_000)m \(totalMs % 60_000 / 1000)s \(totalMs % 1000)ms"
    }
}
