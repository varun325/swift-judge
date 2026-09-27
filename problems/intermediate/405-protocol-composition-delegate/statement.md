`protocol DownloaderDelegate: AnyObject { func didFinish(_ file: String) }`. `final class Downloader` has `weak var delegate: DownloaderDelegate?` and `func download(_ file: String)` that calls `delegate?.didFinish(file)`; if there's no delegate it records `"dropped <file>"` in its own log.

 A `final class Screen: DownloaderDelegate` logs `"shown <file>"`. In `downloadDemo`, create the downloader and a screen, set the delegate, and if `keepDelegate` is `false` **release the screen** (set your only strong reference to `nil`) before downloading. Return the combined log (a shared `Log` object).
