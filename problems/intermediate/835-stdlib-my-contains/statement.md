Implement two overloads on `Sequence`:
 - `myContains(where predicate:)` — works for any element type
 - `myContains(_ element:)` — only where `Element: Equatable`, implemented **using** the predicate version

 Return `[words.myContains(target), words.myContains { $0.count >= minLength }]`.
