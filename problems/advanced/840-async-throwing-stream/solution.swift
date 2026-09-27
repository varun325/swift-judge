enum DownloadError: Error { case interrupted }

func download(chunks: Int, failAt: Int) -> AsyncThrowingStream<Int, Error> {
    AsyncThrowingStream { continuation in
        for i in stride(from: 1, through: chunks, by: 1) {
            if i == failAt {
                continuation.finish(throwing: DownloadError.interrupted)
                return
            }
            continuation.yield(100 * i / chunks)
        }
        continuation.finish()
    }
}

func downloadProgress(chunks: Int, failAt: Int) async -> [String] {
    var log: [String] = []
    do {
        for try await percent in download(chunks: chunks, failAt: failAt) {
            log.append("\(percent)%")
        }
        log.append("done")
    } catch {
        log.append("error \(error)")
    }
    return log
}
