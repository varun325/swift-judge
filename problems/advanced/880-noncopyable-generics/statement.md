Swift 6 lets generics accept **noncopyable** types via `~Copyable`. Write `struct Ticket: ~Copyable { let id: String }` and a generic `struct Vault<Item: ~Copyable>: ~Copyable` that holds an optional item with `mutating func store(_ item: consuming Item)` and `mutating func take() -> Item?`.

 For each secret, store a ticket, take it back (logging `"took <id>"`), and try taking again (logging `"empty"`).
