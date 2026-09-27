Swiftful's *What is Object Oriented Programming for Swift*. `class Account` has `let id: String`, a `private(set) var balance` and `func withdraw(_:) -> Bool`. `final class SavingsAccount: Account` overrides `withdraw` to refuse if the balance would drop below 100. Both have `deposit(_:)`.

 Ops: `open <id> <checking|savings>`, `dep <id> <n>`, `wd <id> <n>`, `show <id>`. For each op output `"ok"`, `"refused"`, `"no account"` or (for `show`) `"<id>: <balance>"`. Accounts live in `[String: Account]`.
