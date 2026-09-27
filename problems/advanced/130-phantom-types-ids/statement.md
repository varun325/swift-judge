Write `struct Length<Unit: LengthUnit>` storing a `Double`, where `protocol LengthUnit { static var metersPerUnit: Double { get } }` and `enum Meters`, `enum Feet` (0.3048) conform. `Unit` is never stored — it's a **phantom type**.

 Add `+` for two lengths of the **same** unit, and `func converted<To>(to: To.Type) -> Length<To>`. Sum all meters, sum all feet, convert the feet total to meters, and return `[meterTotal, feetTotal, meterTotal + feetInMeters]`. (Try `Length<Meters> + Length<Feet>` — it won't compile.)
