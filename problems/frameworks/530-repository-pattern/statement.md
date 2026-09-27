Separate **where** data comes from from **how** it's used. `protocol ArticleRemote: Sendable { func fetch(_ id: Int) async throws -> String }`. `actor ArticleRepository` takes a remote, caches successful results, and offers `func article(_ id: Int, forceRefresh: Bool) async -> Result<String, Error>`.

 A mock remote returns `"article <id> v<call#>"` and throws for id 0. Requests are `<id>` or `<id>!` (force refresh). Log each result (`"err"` for failures) then `"remote calls <n>"`.
