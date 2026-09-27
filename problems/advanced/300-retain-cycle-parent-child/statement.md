`final class Parent` holds `var children: [Child]`; `final class Child` holds a back-reference `parent`. Both log `"deinit <name>"` in `deinit` (into a shared `Log`).

 Starter code leaks: nothing is ever deinitialised. Fix it so that when `cycleDemo`'s inner `do { }` scope ends, **every** object is freed. The log should end with `"end"`.
