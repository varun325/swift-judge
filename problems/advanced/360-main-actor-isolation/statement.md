`@MainActor final class ViewModel` holds `var items: [String]` and a method `func load(_ names: [String]) async` that fetches uppercased names using a **`nonisolated`** static helper `nonisolated static func transform(_ s: String) async -> String` (runs off the main actor), then appends them on the main actor.

 From `uiDemo` (not main-actor), create the view model and call it with `await`, then read `items` (also with `await`). Return the items plus `"count <n>"`.
