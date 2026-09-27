Keep timers dumb and models smart: the view does `.onReceive(timer) { _ in model.tick() }`, and all rules live in a testable class. Tests call `tick()` directly instead of waiting for real seconds.
