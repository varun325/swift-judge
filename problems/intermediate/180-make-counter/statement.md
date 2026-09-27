Write `func makeCounter(step: Int) -> () -> Int` returning a closure that adds `step` to a **captured** running total and returns it.

 `counterDemo` creates two counters — `a = makeCounter(step: 1)` and `b = makeCounter(step: 10)` — and calls them in the order given by `calls` (`"a"` or `"b"`), returning each result.
