Write three overloads of `func describe(_ value: …) -> String`:
 - `Int` → `"int <value>"`
 - `String` → `"string '<value>' (<count>)"`
 - `Bool` → `"bool yes"` / `"bool no"`

 `describeAll` describes all ints, then all words, then all flags. The compiler picks the overload from each argument's static type.
