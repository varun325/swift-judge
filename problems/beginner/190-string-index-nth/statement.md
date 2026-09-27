Return the character at integer `offset` (0-based) as a `String`, or `nil` if the offset is out of range (including negative). You can't write `text[offset]` — work with `String.Index`.

 ```swift
 character(in: "Swift", at: 1)   // "w"
 character(in: "🇮🇳ok", at: 0)   // "🇮🇳"
 character(in: "abc", at: 3)     // nil
 ```
