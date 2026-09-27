Write `@propertyWrapper struct Stored<Value: Codable>` backed by `UserDefaults` (JSON-encoded under a key, with a default). Use it in `struct Preferences { @Stored("theme", default: "system") var theme: String; @Stored("fontSize", default: 14) var fontSize: Int; @Stored("recent", default: []) var recent: [String] }` with a **private suite** `UserDefaults(suiteName:)` (cleared first).

 Writes: `theme=<v>`, `font=<n>`, `recent=<v>` (prepend, keep 3). After all writes, create a **new** `Preferences` (simulating a relaunch) and return its values.
