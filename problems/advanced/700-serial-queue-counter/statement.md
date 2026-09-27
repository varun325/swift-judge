Before actors, shared state was protected with a **serial** `DispatchQueue`. Write `final class SafeCounter: @unchecked Sendable` with a private `value` and a private serial queue; `increment()` uses `queue.sync { value += 1 }` and `var current: Int` reads with `queue.sync { value }`.

 `hammer` runs `DispatchQueue.concurrentPerform(iterations: threads)`, each iteration calling `increment()` `incrementsEach` times, and returns `current`. (Without the queue, increments would be lost — a data race.)
