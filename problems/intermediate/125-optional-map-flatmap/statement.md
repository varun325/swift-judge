Given an optional CSV line, return the square of its **first** field if it parses as an integer. Use `Optional.flatMap` / `Optional.map` rather than `if let` — no `!` and no `if`.

 ```swift
 squaredFirstNumber("4,x,y")  // 16
 squaredFirstNumber("x,4")    // nil
 squaredFirstNumber(nil)      // nil
 ```
