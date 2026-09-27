Write a generic `func retry<T>(maxAttempts: Int, baseDelayMs: Int, recorder: Recorder, isRetryable: (Error) -> Bool, _ operation: () async throws -> T) async throws -> T` with exponential backoff (`base × 2^(attempt−1)` ms, use a tiny base like 1 ms). Only `TransientError` is retryable.

 The operation fails with `TransientError` for the first `failuresBeforeSuccess` calls, then returns `"ok"`. Return `[result or "gave up", "attempts <n>", delays joined by ","]`.
