Build a receipt line: `"<quantity> x <item> @ $<unit> = $<total>"` where money is formatted as dollars with exactly two decimals, computed from **integer cents** (no floating point).

 ```swift
 receiptLine(item: "Coffee", quantity: 3, unitCents: 250)
 // "3 x Coffee @ $2.50 = $7.50"
 ```
