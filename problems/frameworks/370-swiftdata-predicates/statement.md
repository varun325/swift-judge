Paul's *Filtering the results from a SwiftData query*. Insert books `[title, author, rating]` and run each query with `#Predicate` (type-checked Swift, not strings):
 - `author <text>` → `$0.author.localizedStandardContains(text)`
 - `min <n>` → rating ≥ n
 - `range <lo> <hi>` → lo ≤ rating ≤ hi **and** title not empty

 Return titles sorted, joined by `,`, and `fetchCount` for the query as `"(<n>)"`.
