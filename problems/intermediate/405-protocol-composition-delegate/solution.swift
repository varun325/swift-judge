final class Log { var lines: [String] = [] }

protocol DownloaderDelegate: AnyObject {
    func didFinish(_ file: String)
}

final class Downloader {
    weak var delegate: DownloaderDelegate?
    let log: Log
    init(log: Log) { self.log = log }

    func download(_ file: String) {
        if let delegate { delegate.didFinish(file) } else { log.lines.append("dropped \(file)") }
    }
}

final class Screen: DownloaderDelegate {
    let log: Log
    init(log: Log) { self.log = log }
    func didFinish(_ file: String) { log.lines.append("shown \(file)") }
}

func downloadDemo(_ files: [String], keepDelegate: Bool) -> [String] {
    let log = Log()
    let downloader = Downloader(log: log)
    var screen: Screen? = Screen(log: log)
    downloader.delegate = screen
    if !keepDelegate { screen = nil }
    files.forEach(downloader.download)
    withExtendedLifetime(screen) {}
    return log.lines
}
