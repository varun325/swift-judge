final class Counter: @unchecked Sendable {
    var value = 0
}

func batch(items: Int, cancelEarly: Bool) async -> [String] {
    let counter = Counter()
    let task = Task {
        for _ in 0..<items {
            try Task.checkCancellation()
            counter.value += 1
            await Task.yield()
        }
        return counter.value
    }
    if cancelEarly { task.cancel() }
    do {
        return ["processed \(try await task.value)"]
    } catch is CancellationError {
        return ["cancelled after \(counter.value == 0 ? 0 : counter.value)"]
    } catch {
        return ["error"]
    }
}
