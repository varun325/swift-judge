Model `indirect enum Expr { case number(Int); case add(Expr, Expr); case multiply(Expr, Expr); case negate(Expr) }` with an `evaluate() -> Int` method.

 Parse **Reverse Polish Notation** tokens (`"3"`, `"+"`, `"*"`, `"neg"`) into an `Expr` using a stack, then evaluate it. Return `nil` if the tokens don't form exactly one expression.

 ```swift
 evaluateRPN(["2", "3", "+", "4", "*"])   // 20
 evaluateRPN(["5", "neg", "1", "+"])      // -4
 ```
