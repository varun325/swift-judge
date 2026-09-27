Compute a shipping cost using a **`let` constant that is assigned in each branch** of an `if` — not a `var`.

 - base rate: `5.0` for express, `2.5` otherwise
 - cost = base rate × weight, but never less than `10.0`

 ```swift
 shippingCost(weightKg: 2, express: false)  // 10.0 (2.5*2 = 5 → minimum 10)
 shippingCost(weightKg: 4, express: true)   // 20.0
 ```
