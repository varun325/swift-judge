Simulate opening resources. For each step name, log `"open <name>"` and register a `defer` that logs `"close <name>"`. If a step is named `"fail"`, log `"failing"` and stop (return early). Return the full log, including the `close` lines produced as the function exits.

 Hint: `defer` inside a `for` body runs at the end of **each iteration** — so recurse (or use a helper) to keep the resources nested.
