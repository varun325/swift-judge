`struct Request` has `method = "GET"`, `path = "/"`, `headers: [String: String] = [:]`. Add **non-mutating** fluent methods returning modified copies: `method(_:)`, `path(_:)`, `header(_:_:)`, each `-> Self`.

 Steps look like `"method POST"`, `"path /users"`, `"header Accept json"`. Start from `let base = Request()`, fold the steps with `reduce(base)`, and return `[base.summary, built.summary]` where `summary` = `"<METHOD> <path> <headers sorted as k=v joined by ;>"`.
