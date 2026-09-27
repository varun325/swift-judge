Implement `func withTimeout<T: Sendable>(ms: Int, _ work: @escaping @Sendable () async throws -> T) async throws -> T`: race `work` against a sleeping task in a throwing task group; whichever finishes first wins and the other is cancelled. Throw `TimeoutError()` if the timer wins.

 Each job is `[workMs, timeoutMs]` where the work sleeps `workMs` then returns `"done in <workMs>"`. Return the result or `"timed out"` per job.
