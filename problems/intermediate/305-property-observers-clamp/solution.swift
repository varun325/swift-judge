struct Speaker {
    var log: [String] = []
    var volume = 50 {
        willSet { log.append("will \(volume)->\(newValue)") }
        didSet {
            volume = min(max(volume, 0), 100)
            log.append("did \(volume)")
        }
    }
}

func volumeLog(_ changes: [Int]) -> [String] {
    var speaker = Speaker()
    for change in changes { speaker.volume = change }
    return speaker.log
}
