L14–L15 write predicates that traverse relationships and hit query limits ("no computed vars in predicates"). Each game is `[name, isComplete "y"/"n", attempts as comma-separated counts of exact matches]`. Store `@Model Game { name, isComplete, attempts: [Attempt] }` with `@Model Attempt { exact: Int }`, then run:
 1. completed games (`#Predicate { $0.isComplete }`), sorted by name
 2. games with **any** attempt having `exact >= 3` — `#Predicate { $0.attempts.contains { $0.exact >= 3 } }`
 3. games with at most 2 attempts — `$0.attempts.count <= 2`

 Return the three lists, names joined by `,`.
