A vending machine (given in the starter) throws `VendingError`. Process each request and report:
 - success → `"got <item>"`
 - `.invalidSelection` **or** `.outOfStock` → `"unavailable"` (one multi-pattern `catch`)
 - `.insufficientFunds(let needed)` → `"insert <needed> more"`
 - anything else → `"error"`
