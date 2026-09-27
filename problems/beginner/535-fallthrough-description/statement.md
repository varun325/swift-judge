Reproduce the Swift book's example: start with `"The number \(n) is"`. If `n` is one of the primes `2, 3, 5, 7, 11, 13, 17, 19`, append `" a prime number, and also"` and then **`fallthrough`** to `default`, which appends `" an integer."`.

 ```swift
 describe(5)   // "The number 5 is a prime number, and also an integer."
 describe(4)   // "The number 4 is an integer."
 ```
