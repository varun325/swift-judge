actor Log {
    private(set) var lines: [String] = []
    func add(_ s: String) { lines.append(s) }
}

@MainActor
final class ImageLoader {
    private var task: Task<Void, Never>?
    private let log: Log
    var image: String?

    init(log: Log) { self.log = log }

    func onAppear() {
        task = Task { [weak self, log] in
            try? await Task.sleep(for: .milliseconds(50))
            guard !Task.isCancelled else { await log.add("cancelled"); return }
            guard let self else { return }
            self.image = "loaded"
            await self.log.add("loaded")
        }
    }

    func onDisappear(cancel: Bool) {
        if cancel { task?.cancel() }
    }

    isolated deinit {
        let log = self.log
        Task { await log.add("deinit") }
    }
}

func screenLifecycle(cancelOnDisappear: Bool) async -> [String] {
    let log = Log()
    await MainActor.run {
        var loader: ImageLoader? = ImageLoader(log: log)
        loader?.onAppear()
        loader?.onDisappear(cancel: cancelOnDisappear)
        loader = nil
    }
    try? await Task.sleep(for: .milliseconds(150))
    return await log.lines.sorted()
}
