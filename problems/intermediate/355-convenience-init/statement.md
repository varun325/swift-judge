`final class Color` stores `red`, `green`, `blue` (`Int`, 0…255) via a designated `init(red:green:blue:)`. Add:
 - `convenience init(white: Int)` → all three equal
 - `convenience init?(hex: String)` → parses `"#RRGGBB"` (fails otherwise)

 Specs look like `"white 128"` or `"#1A2B3C"`. Return `"rgb(r,g,b)"` or `"invalid"`.
