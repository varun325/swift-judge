`final class Ticker` stores `var onTick: (() -> Void)?`. In `start()` it sets `onTick` to a closure that increments `self.count` and logs `"tick <count>"`. Starter captures `self` strongly — the ticker never deinits.

 Fix `start()` with a capture list so `timerDemo` logs `"deinit ticker"` before `"end"`. Keep the closure working: calling `onTick` `ticks` times must still log every tick.
