struct TransientError: Error {}

final class Recorder: @unchecked Sendable {
    var attempts = 0
    var delays: [Int] = []
}

func retry<T>(
    maxAttempts: Int,
    baseDelayMs: Int,
    recorder: Recorder,
    isRetryable: (Error) -> Bool,
    _ operation: () async throws -> T
) async throws -> T {
    var attempt = 1
    while true {
        do {
            return try await operation()
        } catch where attempt < maxAttempts && isRetryable(error) {
            let delay = baseDelayMs * (1 << (attempt - 1))
            recorder.delays.append(delay)
            try await Task.sleep(for: .milliseconds(delay))
            attempt += 1
        }
    }
}

func retrying(failuresBeforeSuccess: Int, maxAttempts: Int) async -> [String] {
    let recorder = Recorder()
    let result: String
    do {
        result = try await retry(maxAttempts: maxAttempts, baseDelayMs: 1, recorder: recorder, isRetryable: { $0 is TransientError }) {
            recorder.attempts += 1
            if recorder.attempts <= failuresBeforeSuccess { throw TransientError() }
            return "ok"
        }
    } catch {
        result = "gave up"
    }
    return [result, "attempts \(recorder.attempts)", recorder.delays.map(String.init).joined(separator: ",")]
}
