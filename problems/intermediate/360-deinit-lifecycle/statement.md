`final class Tracked` logs `"init <name>"` in its initialiser and `"deinit <name>"` in `deinit` into a shared `Log` object passed to `init`.

 In `lifecycle`: inside a `do { }` scope create one `Tracked` per name into an array; then remove the **first** element (log `"removed"`); then leave the scope (log `"after scope"`). Return the log.
