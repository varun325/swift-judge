`Duration` is a precise, overflow-resistant time span; arithmetic like `+` works directly. Clocks (`ContinuousClock`, `SuspendingClock`) measure elapsed `Duration`s via `clock.measure { … }`.
