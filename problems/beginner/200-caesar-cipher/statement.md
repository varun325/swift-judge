Shift every ASCII letter by `shift` places, wrapping around the alphabet and **preserving case**. Everything else is unchanged. `shift` may be negative or larger than 26.

 ```swift
 caesar("Hello, World!", shift: 3)  // "Khoor, Zruog!"
 caesar("abc", shift: -1)           // "zab"
 ```
