Process commands from stdin against a balance starting at 0:
 - `deposit <n>`, `withdraw <n>` (n > 0 integer)

 Model failures with `enum LedgerError: Error { case badCommand(String), badAmount(String), insufficient(needed: Int) }` and a throwing `apply` function. For each line print `"ok <balance>"` or `"error: <description>"` where descriptions are `"unknown command <cmd>"`, `"bad amount <text>"`, `"need <n> more"`. Finish with `"final <balance>"`.
