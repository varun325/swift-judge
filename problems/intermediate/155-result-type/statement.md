Write `func parseAge(_ s: String) -> Result<Int, AgeError>` where `enum AgeError: Error { case notANumber, negative, unrealistic }` (> 150 is unrealistic). For each input produce `"ok <age>"` or `"fail <error>"` by `switch`ing on the result.

 Then for fun: the **sum** of successful ages should be appended as a final line `"total <n>"`, computed with `compactMap { try? $0.get() }`.
