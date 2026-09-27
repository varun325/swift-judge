Swiftful's *strong & weak references with Async Await*. `@MainActor final class ImageLoader` starts `task = Task { [weak self] in … }` in `onAppear()`, which sleeps 50 ms then (if still alive and not cancelled) sets `self.image = "loaded"`. `onDisappear()` cancels the task if `cancelOnDisappear`. `deinit` logs `"deinit"`.

 The demo creates the loader, calls `onAppear()`, then `onDisappear()`, drops the loader, waits 150 ms, and returns the log. Every write goes through a shared `Log` actor.
