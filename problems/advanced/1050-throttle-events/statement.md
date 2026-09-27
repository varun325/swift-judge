A search field fires events at the given timestamps (ms, ascending). Return the timestamps at which the handler actually **runs**:
 - `throttle` (leading edge): run on an event if at least `interval` ms have passed since the last *run*
 - `debounce` (trailing edge): run `interval` ms after an event that isn't followed by another event within `interval` — report the run time

 These are the semantics behind Combine's `throttle(latest: false)` and `debounce`.
