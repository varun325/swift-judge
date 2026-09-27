`Int("42")` returns an `Int?` — it's a **failable initialiser**. Sum only the tokens that parse as integers.

 ```swift
 sumOfNumbers(["3", "x", "-2", "4.5", " 7"])   // 1   (" 7" and "4.5" don't parse)
 ```
