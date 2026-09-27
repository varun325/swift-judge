A senior-level classic. An `actor ImageCache` must not download the same key twice, even when many callers ask **concurrently**. Because actors are **reentrant**, checking a cache dictionary before `await download()` isn't enough — two callers can both miss.

 Store in-flight work as `[String: Task<String, Never>]`: if a task exists, `await task.value`; otherwise create one. The fake `download` sleeps 30 ms and increments a download counter. Request all keys **concurrently** (task group) and return `[sorted distinct results…, "downloads <n>"]`.
