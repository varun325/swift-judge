Make `actor Account` with a private `balance` and `func deposit(_ amount: Int)`, plus `var current: Int`. Deposit every amount from a **separate child task** (all at once, via a task group) and return the final balance.

 With a plain class this would be a data race — and in Swift 6 language mode it won't even compile. Try it.
