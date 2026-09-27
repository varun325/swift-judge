Swiftful's *Timer and onReceive*: the view forwards ticks from `Timer.publish(every: 1, …)` to an `@Observable` view model, which owns the logic. Implement `CountdownModel` with `remaining`, `isRunning`, `func start()`, `pause()`, `reset()`, `tick()` (only counts while running; stops at 0 and marks `finished`) and a computed `display` in `"m:ss"` format.

 Events: `start`, `pause`, `reset`, `tick`. Return `display` (plus `" done"` when finished) after each event.
