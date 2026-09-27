Make a `@dynamicMemberLookup struct Config` wrapping `[String: String]` so that `config.host` returns `config.storage["host"]`. Also add a dotted-path helper for nested keys stored flat as `"db.port"`: `config.db.port` — hint: return another `Config` scoped to the prefix when the key isn't found directly.

 For each path like `"db.port"`, walk it with **dynamic member syntax** via a helper (`func value(at path: String) -> String?` that uses `self[dynamicMember:]`) and return the value or `"missing"`.
