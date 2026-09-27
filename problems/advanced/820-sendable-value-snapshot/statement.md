Model `struct OrderSnapshot: Sendable { let id: Int; let total: Int }` and process snapshots concurrently in a task group, each child returning `"#<id>: <tax>"` where tax = total × 8 / 100 (integer). Return results sorted by id.

 Try replacing the struct with a `final class` holding a `var total` — Swift 6 rejects sending it into child tasks.
