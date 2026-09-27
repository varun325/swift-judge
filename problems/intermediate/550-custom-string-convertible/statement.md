`struct Money: CustomStringConvertible, CustomDebugStringConvertible` stores `cents`. `description` is `"$12.05"` (negative as `"-$0.50"`); `debugDescription` is `"Money(cents: 1205)"`.

 Return, for each amount, `"\(money)"` and `String(reflecting: money)` — two entries per amount.
