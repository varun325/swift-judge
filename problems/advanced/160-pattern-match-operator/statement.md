Make `switch` understand two custom patterns by overloading `~=`:
 - a `Regex`-free `struct Prefix { let text: String }` matching strings with that prefix
 - a closure pattern `(String) -> Bool`

 Classify each word: `Prefix(text: "un")` → `"negation"`, `{ $0.count > 8 }` → `"long"`, `Prefix(text: "re")` → `"repeat"`, else `"plain"` (checked in that order).
