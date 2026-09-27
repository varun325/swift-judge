`Result.map` transforms the success value; `flatMap` chains a step that can itself fail; the first failure short-circuits the rest. `Int(s).map(Result.success)` passes an enum case as a function.
