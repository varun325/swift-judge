`struct BankAccount` has `private(set) var funds = 0`, `mutating func deposit(_:)` and `mutating func withdraw(_:) -> Bool` (refuses if `amount > funds` — note your notes' version refused when `funds == amount`).

 Each op is `"d <n>"` or `"w <n>"`. Log `"ok <funds>"` or `"refused <funds>"` after each.
