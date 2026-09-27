From your notes: `class Employee` with `init(hours:)` and `func summary() -> String` returning `"I work <h> hours a day."`; `class Developer: Employee` overrides it with `"I spend <h> hours a day fighting over tabs vs spaces"`; `class Manager: Employee` overrides it as `"I schedule meetings for <h> hours, then " + super.summary()`.

 Build an `[Employee]` from `roles` (`"dev"`, `"mgr"`, anything else = plain employee) and return each `summary()` — the method chosen at **runtime**.
