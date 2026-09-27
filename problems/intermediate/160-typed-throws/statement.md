Write `func withdraw(_ amount: Int, from balance: inout Int) throws(BankError)` using Swift 6 **typed throws**, with `enum BankError: Error { case invalidAmount, insufficientFunds(short: Int) }`.

 Apply each amount in order to a running balance and log `"ok -> <balance>"`, `"invalid"` or `"short by <n>"`. Because the error type is known, your `catch` needs no bare fallback — `error` is already a `BankError`. (Inside a closure, write `do throws(BankError) { … }`.)
