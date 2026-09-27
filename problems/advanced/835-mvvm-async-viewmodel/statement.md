Swiftful's *MVVM with Async Await*. Define `protocol DataService: Sendable { func fetchTitles() async throws -> [String] }` and a `@MainActor final class TitlesViewModel` with `enum State { case idle, loading, loaded([String]), failed(String) }` and `func load() async`.

 For each behaviour (`ok`, `empty`, `fail`) build a mock service, run `load()`, and record every state the view model passes through, formatted `idle → loading → loaded(3)` / `failed(offline)` / `loaded(0)`.
