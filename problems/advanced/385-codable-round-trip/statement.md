`enum Event: Codable, Equatable { case login(user: String); case purchase(item: String, cents: Int); case logout }` — Swift synthesises `Codable` for enums with associated values.

 Parse specs (`"login ana"`, `"purchase pen 150"`, `"logout"`), encode the array with `JSONEncoder` (`.sortedKeys`), decode it back, and return: the JSON string, then `"equal"` or `"different"`.
