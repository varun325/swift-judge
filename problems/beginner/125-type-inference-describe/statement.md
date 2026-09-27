Return the names of the types Swift infers for these literals, **in order**, by writing `String(describing: type(of: …))` for each:

 ```swift
 42          3.0          "hi"          true
 [1, 2]      ["a": 1]     (1, "x")      1...3
 ```

 The expected answer is what the real compiler infers — write it with `type(of:)` rather than guessing strings.
