# Swift Fundamentals — Working Notes

> **How to read this file.** Each section starts with **Your notes** (the code you wrote, uncommented and cleaned up), then **What this shows** (bullet-point explanation of the concept), then **Going deeper** (the API surface, idioms and quirks that weren't in today's notes but that you'll hit constantly in real code).

---

## Contents

1. [Value types & reference semantics](#1-value-types--reference-semantics)
2. [Strings](#2-strings)
3. [Numbers](#3-numbers)
4. [Booleans](#4-booleans)
5. [String interpolation](#5-string-interpolation)
6. [Arrays](#6-arrays)
7. [Dictionaries](#7-dictionaries)
8. [Sets](#8-sets)
9. [Enums](#9-enums)
10. [Type annotations & inference](#10-type-annotations--inference)
11. [Conditionals](#11-conditionals)
12. [Switch](#12-switch)
13. [Ternary operator](#13-ternary-operator)
14. [Loops](#14-loops)
15. [Functions](#15-functions)
16. [Tuples](#16-tuples)
17. [Parameter labels](#17-parameter-labels)
18. [Default parameter values](#18-default-parameter-values)
19. [Error handling](#19-error-handling)
20. [Closures](#20-closures)
21. [Structs](#21-structs)
22. [Classes & inheritance](#22-classes--inheritance)
23. [Protocols](#23-protocols)
24. [Extensions](#24-extensions)
25. [Optionals](#25-optionals)
26. [Appendix — Style notes](#appendix--style-notes-on-your-code)

---

## Flagged lines — demos vs. worth confirming

Everything in this file was checked against **Apple Swift 6.4** (`swiftc`), so the error texts and printed output below are the real thing rather than from memory.

Some lines in your notes exist precisely *to* fail — that's how you see what a modifier does. Those are the first table, with the exact compiler output as the payoff. The second table is behaviour that compiles and runs, where the result may or may not be what you were going for; you'll know which.

### Demonstration lines — the error *is* the lesson

| Line | What the compiler says | Why |
|---|---|---|
| `account.funds += 1` after `private(set) var funds` | `error: left side of mutating operator isn't mutable: 'funds' setter is inaccessible` | `private(set)` exposes the getter and hides the setter, so writes are legal only inside the type |
| `super.init(...)` placed *before* `self.isConvertible = ...` | `error: immutable value 'self.isConvertible' may only be initialized once` | two-phase init: own properties first, then `super.init` ([§22](#22-classes--inheritance)) |
| `class Truck: Vehicle { var axles: Int }` | `error: class 'Truck' has no initializers` | a new stored property with no default stops initialiser inheritance |
| `vehicle.openSunroof()` inside `commute` | `error: value of type 'any Vehicle' has no member 'openSunroof'` | a protocol type only exposes the protocol's own members ([§23](#23-protocols)) |
| `func f()` in a subclass without `override` | `error: overriding declaration requires an 'override' keyword` | Swift refuses accidental shadowing |

### Behaviour worth confirming is what you intended

| Line | What actually happens | If you wanted otherwise |
|---|---|---|
| `while i >= 0 { … continue; … i -= 1 }` | **Never terminates** — `continue` jumps past the decrement, so `i` sticks at 0 on `1.jpeg` | decrement before `continue`, or let `for`-`in` own the counter ([§14](#14-loops)) |
| `set { vacationAllowed = vacationTaken - newValue }` | Setting `5` stores `-5`; reading back gives `-5`, so the round trip doesn't hold | `vacationTaken + newValue` |
| `if temp > 20 \|\| temp < 39` | Always true for every `Int` | `&&`, or `(21...38).contains(temp)` |
| `let canVote = age > 18 ? true : false` | `false` at exactly 18 | `age >= 18` — and the ternary is redundant either way |
| `withdraw(amount: 100)` when `funds == 100` | Returns `false`; the balance is untouched | `funds >= amount` (unless refusing to empty the account is deliberate) |
| `switch forecast` with `default:` | Adding a `case snow` later still compiles, silently hitting `default` | list every case and drop `default` to get a compile error instead ([§12](#12-switch)) |

## 1. Value types & reference semantics

### Your notes

```swift
struct Person {
    var person: String
    init(person: String) {
        self.person = person
        print("Create a new reference of Person")
    }
}

let person1 = Person(person: "John")
let person2 = person1
```

### What this shows

- **`struct` is a value type.** `let person2 = person1` does **not** create a new reference — it makes a *copy*. The initialiser runs exactly once, so `"Create a new reference of Person"` prints once, not twice.
- The print message is therefore slightly misleading. It's a *new value*, not a new reference.
- Because they're independent copies, mutating one never affects the other:

```swift
struct Person { var name: String }

var a = Person(name: "John")
var b = a          // copy
b.name = "Jane"

print(a.name)      // "John"  ← untouched
print(b.name)      // "Jane"
```

- Swap `struct` for `class` and the behaviour flips completely — now you *do* have two references to one object:

```swift
class PersonRef { var name: String; init(name: String) { self.name = name } }

let a = PersonRef(name: "John")
let b = a          // same object, shared
b.name = "Jane"

print(a.name)      // "Jane"  ← changed through b!
```

- Note the sneaky detail: `b` above is declared with `let`, and you can *still* mutate `b.name`. With a class, `let` freezes the *reference*, not the object's contents. With a struct, `let` freezes everything.

### Going deeper

**The decision table you'll use for the rest of your Swift career:**

| | `struct` (value) | `class` (reference) |
|---|---|---|
| Assignment | copies | shares |
| Inheritance | ✗ | ✓ |
| `deinit` | ✗ | ✓ |
| Identity (`===`) | ✗ | ✓ |
| Mutation with `let` | blocked entirely | properties still mutable |
| Thread safety | safe by default (no sharing) | needs synchronisation |
| Memberwise init | free | must write it |
| Reference cycles / leaks possible | ✗ | ✓ |

**Default to `struct`.** Reach for `class` when you need identity (this *specific* object), inheritance, `deinit`, or genuinely shared mutable state. All of SwiftUI's `View`s are structs; `ObservableObject` view models are classes precisely *because* they need to be shared.

**Copy-on-write (COW).** Copying a `String`, `Array`, `Dictionary` or `Set` looks expensive but isn't. Swift shares the underlying buffer until someone writes:

```swift
var one = [1, 2, 3]
var two = one       // O(1) — no copy yet, buffer is shared
two.append(4)       // O(n) — *now* the buffer is cloned
```

So passing big arrays around is cheap as long as you don't mutate. Your own structs don't get COW automatically — they get it for free only for the COW-backed properties they contain.

**`mutating` and value semantics are the same idea.** A struct method that changes `self` has to say so (see [Structs](#21-structs)). A class method never does, because it isn't changing the reference.

---

## 2. Strings

### Your notes

```swift
let actor = "Tom Cruise"
let quote = "He tapped a sign saying \"Believe\" and walked away."

let movie = """
the life of an apple engineer
"""

print(actor.count)              // 10
print(quote.hasPrefix("He"))    // true
```

### What this shows

- **Escaping.** `\"` puts a literal double-quote inside a `"…"` literal. Other escapes: `\n` newline, `\t` tab, `\\` backslash, `\u{1F600}` Unicode scalar.
- **Multi-line strings** use `"""` on their own lines. The delimiters *must* be alone on their lines — content can't start on the opening `"""` line.
- **`count`** returns the number of user-visible characters.
- **`hasPrefix` / `hasSuffix`** are case-*sensitive* substring checks at the ends.

### Going deeper

**Raw strings** — kill escaping entirely with `#"…"#`. Priceless for regex, JSON and Windows paths:

```swift
let regex = #"\d{3}-\d{4}"#         // no need to write \\d
let json  = #"{"name": "Taylor"}"#  // no need to escape the quotes
let both  = #"Interpolation still works: \#(actor)"#   // note \#( )
```

**Multi-line indentation rules** — the indentation of the *closing* `"""` is stripped from every line. And a trailing `\` joins lines without a newline:

```swift
let message = """
    Dear Varun,
        indented relative to the closing quotes
    This line and the next are \
    actually one line.
    """
// Leading 4 spaces are removed; "indented" keeps its extra 4.
```

**`count` is O(n) — never use it to test for emptiness:**

```swift
if name.count == 0 { }   // ❌ walks the whole string
if name.isEmpty { }      // ✅ O(1)
```

**A `Character` is a grapheme cluster, not a byte.** This is why `count` is O(n), and it makes Swift more correct than most languages:

```swift
"é".count                       // 1  (even when stored as e + combining accent)
"👨‍👩‍👧‍👦".count                // 1  (one family emoji, 25 bytes)
"héllo".utf8.count              // 6  bytes
"héllo".unicodeScalars.count    // 5
```

**You cannot subscript a String with an `Int`.** This trips up everyone coming from other languages:

```swift
let s = "Hello"
// s[0]                                  ❌ doesn't compile
s.first                                  // Optional("H")
s[s.startIndex]                          // "H"
s[s.index(s.startIndex, offsetBy: 1)]    // "e"
Array(s)[1]                              // "e"  — easy, but O(n) and allocates
```

**Every-day String API you'll reach for:**

```swift
let raw = "  Hello, Swift World  "

raw.isEmpty                                          // false
raw.uppercased()                                     // "  HELLO, SWIFT WORLD  "
raw.lowercased()
"hello world".capitalized                            // "Hello World"

// Trimming (needs Foundation)
raw.trimmingCharacters(in: .whitespacesAndNewlines)  // "Hello, Swift World"

// Searching
raw.contains("Swift")                                // true
raw.hasPrefix("  He")                                // true
raw.firstIndex(of: ",")                              // Optional(index)
raw.lowercased().contains("swift")                   // case-insensitive trick

// Splitting & joining
"a,b,,c".split(separator: ",")                       // ["a", "b", "c"]  — drops empties!
"a,b,,c".split(separator: ",", omittingEmptySubsequences: false)
                                                     // ["a", "b", "", "c"]
["a", "b", "c"].joined(separator: "-")               // "a-b-c"

// Replacing
"hello".replacingOccurrences(of: "l", with: "L")     // "heLLo"  (Foundation)
"hello".replacing("l", with: "L")                    // iOS 16+ / Swift 5.8+

// Building
String(repeating: "-", count: 20)                    // "--------------------"
String("hello".reversed())                           // "olleh"  (String() init required)
"hello".prefix(3)                                    // "hel"   (a Substring)
"hello".dropLast(2)                                  // "hel"   (a Substring)

// Converting
Int("42")            // Optional(42)
Int("42abc")         // nil  ← always an Optional, never trust user input
Double("3.14")       // Optional(3.14)
String(42)           // "42"
```

**Gotcha: `split` and `prefix` return `Substring`, not `String`.** A `Substring` is a *view* into the parent string — it keeps the entire original alive in memory. Fine for transient work, dangerous if you store it:

```swift
let parts = hugeLogFile.split(separator: "\n")
let firstLine = parts[0]              // Substring — pins the whole log in RAM
let safe = String(parts[0])           // ✅ convert when storing
```

Function signatures should usually take `some StringProtocol` or plain `String`, and return `String`.

**Gotcha: `==` compares Unicode *meaning*, not bytes.** Two strings that are byte-different can be equal:

```swift
let precomposed = "café"              // é as one scalar U+00E9
let decomposed  = "cafe\u{301}"       // e + combining acute
precomposed == precomposed            // true
precomposed == decomposed            // true! canonically equivalent
precomposed.utf8.count                // 5
decomposed.utf8.count                 // 6   ← different bytes
```

**Formatting numbers into strings** — prefer `formatted()` over `String(format:)` on modern OSes:

```swift
let price = 1234.5
price.formatted()                                     // "1,234.5"  (iOS 15+)
price.formatted(.currency(code: "INR"))               // "₹1,234.50"
String(format: "%.2f", price)                         // "1234.50"  (Foundation, C-style)
```

**Iterating:**

```swift
for ch in "abc" { print(ch) }                        // a b c
for (i, ch) in "abc".enumerated() { print(i, ch) }   // 0 a / 1 b / 2 c
```

Strings are value types with COW, exactly like arrays — copying is cheap, mutating a copy clones.

---

## 3. Numbers

### Your notes

```swift
let score = 10
let higherScore = score + 10
let halvedScore = score / 2

var counter = 10
counter += 10

let number = 120
print(number.isMultiple(of: 3))   // true

let id = Int.random(in: 1...1000)
let score2 = 3.0                  // this is a Double, not an Int
```

### What this shows

- Integer literals infer to `Int`; literals with a decimal point infer to `Double`. `let score = 10` and `let score = 3.0` are **different types**.
- `+ - * /` work as expected; `+= -= *= /=` are the compound forms.
- `isMultiple(of:)` is a readable, safe replacement for `number % 3 == 0`.
- `Int.random(in:)` takes a range and is cryptographically-adequate for games/IDs (it uses the system RNG).

### Going deeper

**Integer division truncates.** This is the #1 numeric surprise in Swift:

```swift
10 / 3          // 3    ← not 3.333
10 / 4          // 2
-7 / 2          // -3   ← truncates toward zero
Double(10) / 3  // 3.3333333333333335
10.0 / 3        // 3.3333333333333335
```

Your `score / 2` is `5` because `score` is an `Int`. If it had been `10.0`, you'd get `5.0`.

**No implicit numeric conversion — ever.** Swift will not silently widen `Int` to `Double`:

```swift
let i = 5
let d = 2.5
// let sum = i + d        ❌ Binary operator '+' cannot be applied to 'Int' and 'Double'
let sum = Double(i) + d   // ✅ 7.5
```

Literals are the exception, because they're untyped until inferred: `let x: Double = 5` is fine.

**`Int(someDouble)` truncates, it doesn't round:**

```swift
Int(3.9)              // 3
Int(-3.9)             // -3
(3.9).rounded()       // 4.0
(3.4).rounded(.up)    // 4.0   — .up / .down / .towardZero / .toNearestOrEven
Int((3.9).rounded())  // 4     ← what you usually meant
```

**Overflow traps by default.** Swift crashes rather than silently wrapping. If you genuinely want wrapping, use the `&` operators:

```swift
Int.max                 // 9223372036854775807
// Int.max + 1          💥 runtime crash: arithmetic overflow
Int.max &+ 1            // Int.min — deliberate wraparound
let (v, didOverflow) = Int.max.addingReportingOverflow(1)   // safe check
```

**Doubles are not exact.** Never compare them with `==`:

```swift
0.1 + 0.2 == 0.3                          // false! (it's 0.30000000000000004)
abs((0.1 + 0.2) - 0.3) < 0.0001           // ✅ compare within a tolerance
```

For money, use `Decimal` (Foundation) or store integer paise/cents. Never `Double`.

**`%` with negatives, and why `isMultiple(of:)` is better:**

```swift
7 % 3                    //  1
-7 % 3                   // -1   ← Swift keeps the sign of the dividend
(-9).isMultiple(of: 3)   // true — no sign confusion
// 7 % 0                 💥 crash — division by zero
```

**Literal readability:**

```swift
let million = 1_000_000      // underscores are ignored
let hex     = 0xFF           // 255
let binary  = 0b1010         // 10
let octal   = 0o17           // 15
let sci     = 1.5e3          // 1500.0
```

**The utility belt:**

```swift
abs(-5)                          // 5
max(3, 9), min(3, 9)             // 9, 3
(17).quotientAndRemainder(dividedBy: 5)   // (quotient: 3, remainder: 2)
(2.0).squareRoot()               // 1.414...
Int(pow(2.0, 10.0))              // 1024 (Foundation)
(7).signum()                     // 1  (-1, 0, or 1)
5.clamped                        // ✗ doesn't exist — write min(max(x, lo), hi)

// Stepping by something other than 1
for i in stride(from: 0, to: 10, by: 2) { }      // 0 2 4 6 8   (exclusive)
for i in stride(from: 0, through: 10, by: 2) { } // 0 2 4 6 8 10 (inclusive)
for i in stride(from: 10, to: 0, by: -1) { }     // counting down

// Randomness
Int.random(in: 1...6)
Double.random(in: 0..<1)
Bool.random()
[1, 2, 3].randomElement()        // Optional — the array might be empty
[1, 2, 3].shuffled()
```

**Fixed-width types exist but you rarely want them.** `Int8/16/32/64`, `UInt`, `Float` (32-bit), `Double` (64-bit), `CGFloat` (UI code — it's a `Double` on 64-bit). Use `Int` and `Double` unless an API or binary format forces otherwise. `Int` is 64-bit on every device you'll ship to.

---

## 4. Booleans

### Your notes

```swift
let goodDog = true
let gameOver = false

var isSaved = false
isSaved.toggle()      // now true
```

### What this shows

- `Bool` has exactly two values. `toggle()` flips in place — cleaner than `isSaved = !isSaved`.
- The `is…`/`has…`/`can…`/`should…` naming convention for booleans is a strong Swift idiom. `isSaved` reads well at a call site; `saved` doesn't.

### Going deeper

**Swift has no truthiness.** Conditions must be an actual `Bool`:

```swift
let count = 0
// if count { }           ❌ 'Int' is not convertible to 'Bool'
if count != 0 { }         // ✅ be explicit
if !items.isEmpty { }     // ✅ idiomatic
```

**Short-circuiting.** `&&` stops at the first `false`, `||` at the first `true`. This is what makes the guard-then-use pattern safe:

```swift
if !names.isEmpty && names[0] == "Varun" { }   // indexing never runs on an empty array
```

**Booleans as the return of a comparison — skip the ternary:**

```swift
let isAdult = age >= 18 ? true : false   // ❌ redundant
let isAdult = age >= 18                  // ✅ same thing
```

**A stored `Bool` pair is often an enum in disguise.** Two `Bool`s allow four states, and usually only three are legal:

```swift
// Smell: isLoading + hasError can both be true
struct State { var isLoading: Bool; var hasError: Bool }

// Better: exactly the states that exist
enum LoadState { case idle, loading, loaded([Item]), failed(Error) }
```

---

## 5. String interpolation

### Your notes

```swift
let name = "Taylor"
let age = 26
let message = "I'm \(name) and I am \(age) years old"
```

### What this shows

- `\(…)` embeds any expression in a string literal and calls its `description`/`String(describing:)`.
- It's type-safe and compile-checked — no `%@`/`%d` format-specifier mismatches like in Objective-C.

### Going deeper

**Any expression works, not just variables:**

```swift
"\(name.uppercased()) is \(age * 12) months old"
"Total: \(items.count) item\(items.count == 1 ? "" : "s")"   // pluralisation inline
"\(2 + 2)"                                                    // "4"
```

**Optionals interpolate ugly** — this is the most common cosmetic bug in Swift logs:

```swift
let nickname: String? = "Tay"
print("Hi \(nickname)")                      // "Hi Optional("Tay")"  ⚠️ warns
print("Hi \(nickname ?? "friend")")          // "Hi Tay"              ✅
print("Hi \(String(describing: nickname))")  // silences the warning, still ugly
```

**Controlling precision:**

```swift
let pi = 3.14159
"\(pi)"                                       // "3.14159"
"\(String(format: "%.2f", pi))"               // "3.14"
"\(pi.formatted(.number.precision(.fractionLength(2))))"   // "3.14"  iOS 15+
```

**Multi-line + interpolation is the nicest way to build a block of text:**

```swift
let summary = """
Name: \(name)
Age:  \(age)
Tags: \(tags.joined(separator: ", "))
"""
```

**Custom types print better with `CustomStringConvertible`:**

```swift
struct Album: CustomStringConvertible {
    let title: String, artist: String
    var description: String { "\(title) by \(artist)" }
}
print("Now playing \(red)")   // "Now playing Red by Taylor Swift"
```

Without it you get the struct dump `Album(title: "Red", artist: "Taylor Swift")`.

---

## 6. Arrays

### Your notes

```swift
var colors = ["Red", "Green", "Blue"]
let numbers = [4, 8, 15, 16]
var readings = [0.1, 0.5, 0.8]

print(colors[0])        // "Red"
print(readings[2])      // 0.8

colors.append("tartan")
colors.remove(at: 0)

print(colors.count)              // 3
print(colors.contains("Octarine"))  // false
```

### What this shows

- Arrays are **ordered**, allow **duplicates**, are **zero-indexed**, and are **homogeneous** — `[String]`, `[Int]`, `[Double]` are distinct types inferred from the literal.
- `var` vs `let` matters: `numbers` is `let`, so `numbers.append(…)` wouldn't compile. `append`, `remove`, `insert` are all `mutating`.
- `remove(at:)` shifts everything after it down — it's O(n).
- `contains` on an array is a **linear scan** — O(n). Fine for 3 colours, wrong for 100,000 (use a `Set`).

### Going deeper

**⚠️ Indexing out of bounds crashes.** There is no `nil` fallback like a dictionary:

```swift
let items = ["a", "b"]
// items[5]                     💥 Fatal error: Index out of range
items.first                     // Optional("a")  ✅ safe
items.last                      // Optional("b")  ✅ safe
items.indices.contains(5)       // false — check first
items[safe: 5]                  // ✗ not in the stdlib; people add it via extension:
```

```swift
extension Collection {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}
```

**Adding & removing:**

```swift
var xs = [1, 2, 3]

xs.append(4)                     // [1, 2, 3, 4]
xs += [5, 6]                     // [1, 2, 3, 4, 5, 6]
xs.append(contentsOf: [7, 8])
xs.insert(0, at: 0)              // O(n)

let removed = xs.remove(at: 0)   // returns the element it removed
xs.removeLast()                  // 💥 crashes on an empty array
xs.popLast()                     // Optional — safe on empty  ✅
xs.removeFirst()                 // 💥 also crashes on empty
xs.removeAll(where: { $0 % 2 == 0 })   // filter-in-place, keeps odds
xs.removeAll()
```

**Transforming — this is where you'll spend most of your time:**

```swift
let nums = [1, 2, 3, 4, 5]

nums.map { $0 * 2 }                    // [2, 4, 6, 8, 10]      same count, new type ok
nums.filter { $0.isMultiple(of: 2) }   // [2, 4]                subset
nums.reduce(0, +)                      // 15                    collapse to one value
nums.reduce(0) { $0 + $1 * $1 }        // 55                    sum of squares
nums.forEach { print($0) }             // like for-in, but can't `break`

["1", "x", "3"].compactMap { Int($0) } // [1, 3]     map + drop the nils
[[1, 2], [3]].flatMap { $0 }           // [1, 2, 3]  flatten one level

nums.sorted()                          // [1, 2, 3, 4, 5]
nums.sorted(by: >)                     // [5, 4, 3, 2, 1]
nums.sorted { $0 % 3 < $1 % 3 }        // custom comparator
var m = nums; m.sort()                 // in-place, needs var
nums.reversed()                        // lazy view; Array(nums.reversed()) to materialise
nums.shuffled()
```

**Searching & testing:**

```swift
nums.contains(3)                       // true
nums.contains { $0 > 4 }               // true  — predicate version
nums.first { $0 > 3 }                  // Optional(4)
nums.firstIndex(of: 3)                 // Optional(2)
nums.firstIndex { $0 > 3 }             // Optional(3)
nums.allSatisfy { $0 > 0 }             // true
nums.min(), nums.max()                 // Optionals
nums.isEmpty                           // ✅ prefer over count == 0
```

**Slicing (all return lazy `ArraySlice`, cheap views):**

```swift
nums.prefix(2)        // [1, 2]
nums.suffix(2)        // [4, 5]
nums.dropFirst()      // [2, 3, 4, 5]
nums.dropLast(2)      // [1, 2, 3]
nums.prefix(while: { $0 < 3 })   // [1, 2] — stops at the first failure
nums[1...3]           // [2, 3, 4]
```

**⚠️ The biggest array gotcha in Swift: slice indices are inherited.** A slice keeps the *parent's* indices, so its `startIndex` is not 0:

```swift
let all = [10, 20, 30, 40]
let tail = all.dropFirst()      // [20, 30, 40]
tail.startIndex                 // 1  ← not 0!
// tail[0]                      💥 Fatal error: Index out of range
tail.first                      // Optional(20)  ✅
Array(tail)[0]                  // 20            ✅ re-index by converting
```

Rule of thumb: the moment a slice leaves the expression that made it, wrap it in `Array(…)`.

**`enumerated()` gives you *offsets*, not indices.** Safe on `Array`, wrong on slices:

```swift
for (i, v) in ["a", "b"].enumerated() { print(i, v) }   // 0 a / 1 b

// On a slice the offset and the real index diverge:
for (i, v) in all.dropFirst().enumerated() { print(i, v) }   // 0 20 / 1 30 / 2 40
// use zip(slice.indices, slice) when you need the true index
```

**`zip` — pair two sequences, stopping at the shorter one:**

```swift
let names = ["a", "b", "c"]
let scores = [90, 80]
Array(zip(names, scores))        // [("a", 90), ("b", 80)]   — "c" dropped
```

**Other things worth knowing:**

```swift
Array(repeating: 0, count: 5)          // [0, 0, 0, 0, 0]
Array(1...5)                           // [1, 2, 3, 4, 5]
var grid = Array(repeating: Array(repeating: 0, count: 3), count: 3)   // 2D
[[1, 2], [3]].joined()                 // flatten (lazy)
["a", "b"].joined(separator: ", ")     // "a, b"  — strings only
xs.swapAt(0, 1)
xs.reserveCapacity(1000)               // avoid repeated reallocation in a hot loop
Array(Set(duplicates))                 // dedupe — but loses order!
```

**Deduping while keeping order** (no stdlib helper for this — write it once):

```swift
extension Array where Element: Hashable {
    func uniqued() -> [Element] {
        var seen = Set<Element>()
        return filter { seen.insert($0).inserted }
    }
}
```

**Performance summary:** `append` amortised O(1); `remove(at:)`/`insert(at:)` O(n); `contains`/`firstIndex` O(n); `sorted` O(n log n) and **not guaranteed stable** — if equal elements must keep their relative order, sort on a tuple with a tiebreaker.

---

## 7. Dictionaries

### Your notes

```swift
let employee = [
    "name": "Taylor",
    "job": "Singer"
]

print(employee["job", default: "Unknown"])   // "Singer"
```

### What this shows

- A dictionary maps unique **keys** to **values** — here `[String: String]`, inferred from the literal.
- The plain subscript `employee["job"]` returns an **Optional** (`String?`) because the key might not exist.
- The `default:` subscript unwraps for you: if the key is missing you get the default instead of `nil`. It's the tidiest way to avoid `??` everywhere.

### Going deeper

**⚠️ Dictionaries are unordered.** Iteration order is arbitrary and can differ between runs of the same binary (hash seeding is randomised per process). If you need order, sort explicitly:

```swift
for (k, v) in employee.sorted(by: { $0.key < $1.key }) { print(k, v) }
```

**The subscript is an Optional in both directions** — and assigning `nil` deletes:

```swift
var scores = ["varun": 10]

scores["varun"]                    // Optional(10)
scores["nobody"]                   // nil   — no crash, unlike an array
scores["asha"] = 8                 // insert
scores["asha"] = 9                 // overwrite
scores["asha"] = nil               // ⚠️ removes the key entirely
scores.removeValue(forKey: "asha") // same thing, returns the old value
scores.updateValue(11, forKey: "varun")   // returns Optional(10), the previous value
```

**The counting idiom** — `default:` plus `+=` is the single most useful dictionary trick:

```swift
let words = ["a", "b", "a", "c", "a"]
var counts: [String: Int] = [:]
for w in words { counts[w, default: 0] += 1 }
// ["a": 3, "b": 1, "c": 1]
```

It works because the `default:` subscript is both a getter *and* a setter.

**`Dictionary(grouping:by:)` — reach for this constantly:**

```swift
let names = ["Ana", "Bo", "Amit", "Bela"]
let byLetter = Dictionary(grouping: names) { $0.first! }
// ["A": ["Ana", "Amit"], "B": ["Bo", "Bela"]]
```

**Building a dictionary from pairs:**

```swift
let pairs = [("a", 1), ("b", 2)]
Dictionary(uniqueKeysWithValues: pairs)        // 💥 crashes on a duplicate key
Dictionary(pairs, uniquingKeysWith: { $1 })    // ✅ last wins
Dictionary(pairs, uniquingKeysWith: +)         // ✅ sum the collisions
```

**Transforming:**

```swift
let prices = ["apple": 100, "banana": 40]

prices.mapValues { $0 * 2 }                // ["apple": 200, "banana": 80]
prices.filter { $0.value > 50 }            // ["apple": 100]  — returns a Dictionary
prices.compactMapValues { $0 > 50 ? $0 : nil }   // drops nils *and* unwraps
prices.keys.sorted()                       // ["apple", "banana"]
Array(prices.values)                       // [100, 40] in some order
prices.count, prices.isEmpty
prices.merging(["cherry": 200]) { old, _ in old }   // combine two dictionaries
prices.reduce(0) { $0 + $1.value }         // 140 — total
prices.min(by: { $0.value < $1.value })    // Optional(("banana", 40))
```

**Iteration destructures into a tuple:**

```swift
for (fruit, price) in prices { print("\(fruit): \(price)") }
for fruit in prices.keys { }
```

**Keys must be `Hashable`.** `String`, `Int`, `Double`, `Bool`, enums without associated values, and any struct whose stored properties are all Hashable (add `: Hashable` and the compiler synthesises it):

```swift
struct Coordinate: Hashable { let x: Int, y: Int }
var visited: [Coordinate: Bool] = [:]
visited[Coordinate(x: 1, y: 2)] = true
```

**⚠️ Never use a mutable class as a key**, and never mutate a key object after insertion — the hash changes and the entry becomes unreachable.

**Empty dictionary syntax:**

```swift
var a: [String: Int] = [:]
var b = [String: Int]()        // identical
```

---

## 8. Sets

### Your notes

```swift
var numbers = Set([1, 1, 3, 5, 7, 9])

print(numbers)            // e.g. [5, 9, 1, 3, 7] — order is arbitrary
numbers.insert(10)
numbers.contains(11)      // ⚠️ result unused → compiler warning
```

### What this shows

- A `Set` holds **unique**, **unordered** elements. The duplicate `1` is silently dropped, so the count is 5, not 6.
- `contains` is **O(1)** because it hashes, versus **O(n)** for an array. That's the whole reason sets exist.
- `numbers.contains(11)` on its own line produces *"Result of call to 'contains' is unused"*. Either use the value or discard it with `_ = numbers.contains(11)`.

### Going deeper

**`insert` returns a tuple, which is genuinely useful:**

```swift
var seen = Set<String>()
let result = seen.insert("a")
result.inserted              // true  — it wasn't there before
seen.insert("a").inserted    // false — already present
```

That's the mechanism behind the `uniqued()` extension in the Arrays section.

**Set algebra — clean code for "which items changed":**

```swift
let a: Set = [1, 2, 3, 4]
let b: Set = [3, 4, 5]

a.union(b)                // [1, 2, 3, 4, 5]
a.intersection(b)         // [3, 4]
a.subtracting(b)          // [1, 2]        — in a, not in b
a.symmetricDifference(b)  // [1, 2, 5]     — in exactly one

a.isSubset(of: b)         // false
a.isSuperset(of: [1, 2])  // true
a.isDisjoint(with: [9])   // true          — no overlap
```

Each has a mutating `form…` twin: `formUnion`, `formIntersection`, `subtract`, `formSymmetricDifference`.

**A real-world use — diffing state:**

```swift
let oldIDs: Set<Int> = [1, 2, 3]
let newIDs: Set<Int> = [2, 3, 4]

let added   = newIDs.subtracting(oldIDs)   // [4]
let deleted = oldIDs.subtracting(newIDs)   // [1]
let kept    = oldIDs.intersection(newIDs)  // [2, 3]
```

**Removing & converting:**

```swift
var s: Set = [1, 2, 3]
s.remove(2)                // returns Optional(2), nil if absent
s.removeFirst()            // arbitrary element — 💥 crashes on empty
Array(s)                   // order arbitrary
s.sorted()                 // [Int] in order — the way to display a Set
```

**When to use what:**

| Need | Use |
|---|---|
| Order matters, duplicates allowed | `Array` |
| Fast membership tests, uniqueness | `Set` |
| Key → value lookup | `Dictionary` |
| Insertion order *and* uniqueness | `Array` + `Set` together (see `uniqued()`) |

**Gotchas:** no subscripting (`s[0]` doesn't compile), no `append` (`insert`), elements must be `Hashable`, and `print` order is unreliable — never write a test that asserts on a set's printed order.

---

## 9. Enums

### Your notes

```swift
enum Weekday {
    case monday, tuesday, wednesday, thursday, friday
}

var day: Weekday = Weekday.monday
day = .friday               // type already known, so the prefix is optional
print(day)                  // "friday"
```

### What this shows

- An enum defines a **closed set of values**. The compiler now knows `day` can only ever be one of five things — impossible states become uncompilable.
- Once the type is known, use the **leading-dot shorthand**: `day = .friday`. This works anywhere the type is inferable (assignments, function arguments, `switch` cases, array literals).
- Enums are value types, `Equatable`-comparable with `==`, and `Hashable` for free when they have no associated values (so they work as dictionary keys).

### Going deeper

**Raw values** — back each case with a `String` or `Int` for serialisation:

```swift
enum Weekday: String {
    case monday, tuesday          // raw values default to the case name
    case wednesday = "Wed"        // or set them explicitly
}

Weekday.monday.rawValue           // "monday"
Weekday(rawValue: "monday")       // Optional(.monday)  ← failable init!
Weekday(rawValue: "funday")       // nil
```

```swift
enum Priority: Int {
    case low = 1, medium, high    // Int raw values auto-increment: 1, 2, 3
}
```

**`CaseIterable`** — free `allCases`, perfect for pickers and tests:

```swift
enum Weekday: CaseIterable { case mon, tue, wed, thu, fri }

Weekday.allCases           // [.mon, .tue, .wed, .thu, .fri]
Weekday.allCases.count     // 5
Weekday.allCases.randomElement()
```

Synthesised only when no case has associated values.

**Associated values** — each case can carry its own payload. This is the feature that makes Swift enums far more powerful than C enums:

```swift
enum Result {
    case success(data: Data)
    case failure(code: Int, message: String)
    case loading
}

let r = Result.failure(code: 404, message: "Not found")

switch r {
case .success(let data):
    print("Got \(data.count) bytes")
case .failure(let code, let message):
    print("\(code): \(message)")
case .failure(let code, _) where code >= 500:
    print("server error")            // ⚠️ unreachable — the case above already matched
case .loading:
    break
}
```

Order your cases most-specific-first, and prefer `where` clauses over a second bare case.

**Extracting one case without a full switch:**

```swift
if case .failure(let code, _) = r { print(code) }
guard case .success(let data) = r else { return }

// Filtering a collection by case:
for case .failure(let code, _) in results { print(code) }
```

**Methods and computed properties are allowed; stored instance properties are not:**

```swift
enum Weekday: String, CaseIterable {
    case mon, tue, wed, thu, fri

    var isStartOfWeek: Bool { self == .mon }

    var displayName: String { rawValue.capitalized }

    func next() -> Weekday {
        let all = Self.allCases
        let i = all.firstIndex(of: self)!
        return all[(i + 1) % all.count]
    }

    static let workdayCount = 5      // static stored is fine
    // var note = ""                 ❌ enums can't have stored instance properties
}
```

**`indirect` for recursive enums** (trees, expression parsers, linked lists):

```swift
indirect enum Expr {
    case number(Int)
    case add(Expr, Expr)
    case multiply(Expr, Expr)
}

func eval(_ e: Expr) -> Int {
    switch e {
    case .number(let n):        return n
    case .add(let l, let r):    return eval(l) + eval(r)
    case .multiply(let l, let r): return eval(l) * eval(r)
    }
}
eval(.add(.number(2), .multiply(.number(3), .number(4))))   // 14
```

**Conformances you get cheaply:**

```swift
enum Size: Int, Comparable, CaseIterable, Codable {
    case small, medium, large
    static func < (a: Size, b: Size) -> Bool { a.rawValue < b.rawValue }
}
Size.small < Size.large            // true
[Size.large, .small].sorted()      // [.small, .large]
```

With a raw value, `Codable` conformance is free. Without one, associated-value enums can still be `Codable` — the compiler synthesises it as of Swift 5.5.

**Enum vs struct vs class:** enum = "one of these"; struct = "all of these together"; class = "an identity that changes over time".

**Real-world pattern — the state machine.** Any time you find yourself with several `Bool`s or Optionals that should be mutually exclusive, it's an enum:

```swift
enum ViewState {
    case loading
    case loaded([Item])
    case empty
    case failed(Error)
}
```

Now `loaded` and `failed` simultaneously isn't a bug you have to test for — it's a state that cannot be expressed.

---

## 10. Type annotations & inference

### Your notes

```swift
var score: Double = 0

let player: String = "roy"
let luckyNumber: Int = 13
let pi: Double = 3.14
var isEnabled: Bool = true

var albums: Array<String> = ["Red", "Fearless"]
var user: Dictionary<String, String> = ["id": "@twostraws"]

var albums2: [String] = ["Red", "Fearless"]        // sugar — preferred
var user2: [String: String] = ["id": "@twostraws"]

var teams: [String] = [String]()
var clues = [String]()
```

### What this shows

- `: Type` is an **annotation** — you're telling the compiler instead of letting it infer.
- `var score: Double = 0` is the case where the annotation actually *matters*: without it, `0` infers to `Int`. This is the most common legitimate reason to annotate.
- `[String]` / `[String: String]` are **syntactic sugar** for `Array<String>` / `Dictionary<String, String>`. Identical types; always use the sugar.
- `[String]()` calls the initialiser for an empty array. `var teams: [String] = [String]()` says the same thing twice — write one or the other.

### Going deeper

**Annotate when the literal is ambiguous or wrong, otherwise let inference work:**

```swift
let player = "roy"              // ✅ obviously a String; the annotation is noise
let luckyNumber = 13            // ✅ obviously an Int
var score: Double = 0           // ✅ annotation needed — 0 would be an Int
let ids: [Int] = []             // ✅ needed — an empty literal has no type to infer
let ratio: CGFloat = 1          // ✅ needed for the API it feeds
var delegate: MyDelegate?       // ✅ needed — nil alone has no type
```

**Empty-collection syntax, pick one style and stay consistent:**

```swift
var a = [String]()              // initialiser style
var b: [String] = []            // annotation style
var c = [String: Int]()
var d: [String: Int] = [:]
var e = Set<String>()
```

**`let` unless you need `var`.** The compiler warns on a `var` that's never mutated, and `let` is what makes value semantics safe. Reach for `var` only when you actually reassign or call a `mutating` method.

**Type inference has limits** — it stops at the statement boundary, and can get slow or ambiguous with mixed numeric literals:

```swift
// let x = 1 + 2.5 * 3          works (literals are flexible)
let items = [1, "two"]          // infers [Any] — almost never what you want
let ok: [Any] = [1, "two"]      // ✅ be explicit if you truly mean it
```

**`Any` and `AnyObject`** exist but are escape hatches. Every use costs you compile-time safety and forces a cast:

```swift
let values: [Any] = [1, "two", 3.0]
for v in values {
    if let i = v as? Int { print("int \(i)") }        // conditional cast → Optional
    else if v is String { print("a string") }          // type test
}
// v as! Int                                           💥 force cast, crashes if wrong
```

**Type aliases** make signatures readable:

```swift
typealias JSON = [String: Any]
typealias Completion = (Result<Data, Error>) -> Void

func fetch(_ url: URL, then completion: @escaping Completion) { }
```

**Generics are inference in action** — the same `[String]` sugar you're using is `Array<Element>` with `Element` inferred:

```swift
func firstOrDefault<T>(_ array: [T], default fallback: T) -> T {
    array.first ?? fallback
}
firstOrDefault([1, 2], default: 0)          // T inferred as Int
firstOrDefault(["a"], default: "")          // T inferred as String
```

**Checking a type at runtime** (useful in a playground when inference surprises you):

```swift
print(type(of: score))          // Double
print(type(of: albums))         // Array<String>
```

---

## 11. Conditionals

### Your notes

```swift
let age = Int.random(in: 1...30)

if age < 12 {
    print("You can't vote")
} else if age < 18 {
    print("You can vote soon")
} else {
    print("You can vote")
}

let temp = 26

if temp > 20 || temp < 39 {
    print("wow")
}
```

### What this shows

- `if` / `else if` / `else` evaluate top to bottom and stop at the first true branch. The parentheses around the condition are optional in Swift — omit them.
- `<` `>` `<=` `>=` `==` `!=` compare; `&&` (and), `||` (or), `!` (not) combine.
- The first chain is correct but note the ordering does the work: by the time you reach `else if age < 18`, you already know `age >= 12`.

### ⚠️ Bug 3: `||` should be `&&`

```swift
if temp > 20 || temp < 39 { }   // ❌ always true — every Int is either >20 or <39
if temp > 20 && temp < 39 { }   // ✅ "between 20 and 39"
if (21...38).contains(temp) { } // ✅ clearer still
```

An `||` that can never be false is a silent bug — nothing crashes, the branch just always runs. When you write a range check, say it out loud: *"greater than 20 **and** less than 39."*

### Going deeper

**Range membership beats chained comparisons:**

```swift
if (18...65).contains(age) { }
if (18...).contains(age) { }        // one-sided: 18 and up
if (..<18).contains(age) { }        // up to but not including 18
```

**`if let` — unwrap an Optional and bind it in one move:**

```swift
let input: String? = "42"

if let input {                          // Swift 5.7 shorthand — same name
    print(input.count)                  // `input` is a non-optional String here
}

if let number = Int(input ?? "") {      // rename while unwrapping
    print(number * 2)
}

if let a = first, let b = second, a < b {   // multiple bindings + a condition
    print("ordered")
}
```

**`guard let` — the early-exit form, and usually the better one:**

```swift
func greet(_ name: String?) {
    guard let name, !name.isEmpty else {
        print("No name")
        return                   // guard *must* exit the scope
    }
    // `name` is unwrapped for the whole rest of the function — no nesting
    print("Hi \(name)")
}
```

`if let` nests and indents; `guard let` flattens. In a function with three preconditions, `guard` keeps your happy path at one indent level. Use `guard` for "this shouldn't happen, bail", `if let` for "this is one of two normal paths".

**`??` nil-coalescing — supply a fallback inline:**

```swift
let name = maybeName ?? "Anonymous"
let count = dict["k"] ?? 0
let chained = a ?? b ?? "last resort"      // right-associative
```

**`if` is an expression (Swift 5.9+)** — great for assigning:

```swift
let label = if age < 18 { "minor" } else { "adult" }

let tier = switch score {
    case 0..<50:  "bronze"
    case 50..<80: "silver"
    default:      "gold"
}
```

**Comparison operators work on more than numbers:**

```swift
"apple" < "banana"              // true — lexicographic
[1, 2] == [1, 2]                // true — element-wise
(1, "a") < (1, "b")             // true — tuples compare left to right
Date() > someOtherDate          // true/false
```

**Common condition smells:**

```swift
if flag == true { }             // ❌ just `if flag`
if flag == false { }            // ❌ just `if !flag`
if arr.count > 0 { }            // ❌ `if !arr.isEmpty`
if x != nil { use(x!) }         // ❌ `if let x { use(x) }`
```

---

## 12. Switch

### Your notes

```swift
enum Weather {
    case sun, rain, wind
}

let forecast: Weather = Weather.sun

switch forecast {
case .sun:
    print("A nice day")
case .rain:
    print("Pack an umbrella")
default:
    print("Should be okay.")
}
```

### What this shows

- `switch` matches a value against patterns. Swift's version has **no implicit fallthrough** — each case ends on its own, no `break` needed.
- `switch` must be **exhaustive**. That's what forces the `default` here (you've covered `.sun` and `.rain` but not `.wind`).
- Cases can't be empty — if you want a case to do nothing, write `break`.

### ⚠️ Bug 5: `default` on an enum throws away your best safety feature

Right now, if you add a fourth case:

```swift
enum Weather { case sun, rain, wind, snow }   // added snow
```

…this switch still compiles, and snow silently prints *"Should be okay."* Compare with listing every case:

```swift
switch forecast {
case .sun:  print("A nice day")
case .rain: print("Pack an umbrella")
case .wind: print("Hold onto your hat")
}
// Add `snow` and the compiler *errors*: "Switch must be exhaustive"
```

That compile error is the point. It walks you to every place in your app that needs updating. **Rule: never use `default` when switching over your own enum.** Use it only for open types like `Int`, `String`, or another module's non-frozen enum (where `@unknown default:` is the right tool — it warns you without breaking the build).

### Going deeper

**Matching multiple values in one case:**

```swift
switch forecast {
case .rain, .wind: print("Stay in")
case .sun:         print("Go out")
}
```

**Ranges and `where` clauses:**

```swift
switch score {
case ..<0:        print("invalid")
case 0..<50:      print("fail")
case 50..<80:     print("pass")
case let s where s.isMultiple(of: 100): print("perfect \(s)")
default:          print("distinction")
}
```

**Binding values out of the match:**

```swift
switch result {
case .success(let value):       print(value)
case .failure(let error):       print(error.localizedDescription)
}

// Shorter when everything binds:
case let .success(value): print(value)
```

**Tuple matching** — switch on several things at once. This is where `switch` really outclasses `if`:

```swift
let point = (x: 0, y: 5)

switch point {
case (0, 0):              print("origin")
case (_, 0):              print("on the x-axis")
case (0, _):              print("on the y-axis")
case (let x, let y) where x == y: print("on the diagonal")
case (-5...5, -5...5):    print("near the middle")
default:                  print("somewhere out there")
}
```

**Optional matching:**

```swift
switch maybeName {
case .some(let name): print(name)
case .none:           print("nothing")
}
// or the sugar:
case let name?: print(name)
case nil:       print("nothing")
```

**`fallthrough`** exists if you really want C behaviour — it jumps to the next case's body *without* re-testing its pattern:

```swift
switch n {
case 1: print("one"); fallthrough
case 2: print("two")     // runs for n == 1 as well
default: break
}
```

Rare in practice. Prefer comma-separated cases.

**Switching on strings and types:**

```swift
switch command {
case "add", "insert": …
case let s where s.hasPrefix("--"): …
default: …
}
```

**The real reason to love `switch`:** with enums it turns "did I handle every case?" from a code-review question into a compiler error. Treat every new enum case as a task list that the compiler hands you.

---

## 13. Ternary operator

### Your notes

```swift
let age = 18
let canVote = age > 18 ? true : false
```

### What this shows

- `condition ? valueIfTrue : valueIfFalse` — an expression, so it produces a value you can assign or pass directly.
- Mnemonic: **WTF** — **W**hat to check, **T**rue branch, **F**alse branch.

### ⚠️ Bug 4: two problems in one line

```swift
let canVote = age > 18 ? true : false   // ❌ 18-year-olds can't vote, and the ternary is dead weight
let canVote = age >= 18                 // ✅ correct boundary, no ternary needed
```

`x ? true : false` is always just `x`. Any time you see a ternary whose branches are `true` and `false`, delete it. Similarly `x ? false : true` is `!x`.

### Going deeper

**Where the ternary genuinely earns its place** — inline, in a context where a statement won't fit:

```swift
// String interpolation
print("\(count) item\(count == 1 ? "" : "s")")

// Function arguments
view.backgroundColor = isActive ? .systemBlue : .systemGray

// Inside an expression / SwiftUI view builder
Text(isOn ? "On" : "Off")
    .foregroundStyle(isOn ? .green : .secondary)

// Sorting direction
items.sorted(by: ascending ? (<) : (>))
```

**Where it doesn't** — nested ternaries are write-only code:

```swift
// ❌ unreadable
let label = score > 80 ? "A" : score > 60 ? "B" : score > 40 ? "C" : "F"

// ✅ switch as an expression (Swift 5.9+)
let label = switch score {
    case 81...: "A"
    case 61...: "B"
    case 41...: "C"
    default:    "F"
}
```

**Related shorthand — don't confuse the two:**

```swift
let a = cond ? x : y        // ternary — picks between two values
let b = optional ?? y       // nil-coalescing — unwraps, or falls back
```

`??` is not a ternary on a Bool; it's specifically for Optionals.

---

## 14. Loops

### Your notes

```swift
let platforms = ["iOS", "tvOS", "watchOS"]

for os in platforms {
    print("Swift works on \(os)")
}

// Exclusive range
for i in 1..<12 { print("5 x \(i) is \(5 * i)") }

// Inclusive range
for i in 1...12 { print("5 x \(i) is \(5 * i)") }

let files = ["1.jpeg", "2.txt", "3.png"]
var i = 2
while i >= 0 {
    if files[i].hasSuffix(".jpeg") {
        continue        // ⚠️ infinite loop
    }
    print(files[i])
    i -= 1
}
```

### What this shows

- `for … in` walks any `Sequence` — arrays, ranges, dictionaries, sets, strings.
- `1..<12` is a **half-open range**: 1 to 11, twelve excluded. `1...12` is a **closed range**: 1 to 12 inclusive. The `..<` form is the one that matches `array.count`.
- `while` tests its condition *before* each pass; `continue` skips to the next iteration; `break` leaves the loop entirely.

### ⚠️ Bug 1: this `while` loop never terminates

Trace it:

| pass | `i` | `files[i]` | `.jpeg`? | what happens |
|---|---|---|---|---|
| 1 | 2 | `3.png` | no | prints, `i` → 1 |
| 2 | 1 | `2.txt` | no | prints, `i` → 0 |
| 3 | 0 | `1.jpeg` | **yes** | `continue` — **`i` is never decremented** |
| 4 | 0 | `1.jpeg` | yes | `continue`… forever |

`continue` jumps straight back to the condition, skipping the `i -= 1` at the bottom. Any `while` loop whose counter update sits *after* a `continue` is an infinite loop waiting to happen.

Three fixes, best last:

```swift
// 1. Decrement before you continue
var i = 2
while i >= 0 {
    let file = files[i]
    i -= 1                                    // ✅ moved above the continue
    if file.hasSuffix(".jpeg") { continue }
    print(file)
}

// 2. Let a for-in own the counter (can't forget to advance it)
for file in files.reversed() {
    if file.hasSuffix(".jpeg") { continue }
    print(file)
}

// 3. Say what you mean — no loop-control keywords at all
for file in files.reversed() where !file.hasSuffix(".jpeg") {
    print(file)
}
```

Also worth noticing: iterating `2 → 0` prints the list **backwards** (`3.png`, `2.txt`). If forward order was intended, just `for file in files`.

### Going deeper

**`for … in` variants you'll use daily:**

```swift
for _ in 1...3 { print("hi") }                   // don't need the value? use _
for (i, name) in names.enumerated() { }          // index (offset) + value
for (key, value) in dict { }                     // dictionaries destructure
for ch in "hello" { }                            // characters
for n in numbers where n.isMultiple(of: 2) { }   // built-in filter, no `if` needed
for case .failure(let e) in results { }          // only matching enum cases
for x in array.reversed() { }
for x in array.sorted() { }
for (a, b) in zip(arrayA, arrayB) { }            // two arrays in lockstep
for i in stride(from: 0, to: 100, by: 10) { }    // custom step
for i in (0..<5).reversed() { }                  // 4 3 2 1 0
```

**Ranges, laid out plainly:**

```swift
0..<array.count          // every valid index — the safe idiom
array.indices            // ✅ better: same thing, works for slices too
1...10                   // closed
1..<10                   // half-open
"a"..."z"                // works on anything Comparable
// (5...1)               💥 crashes — a range's lower bound must be ≤ its upper bound
```

That last one catches people: `for i in 0..<array.count` on an **empty** array is fine (`0..<0` is a valid empty range), but `0...array.count - 1` **crashes** on empty (`0...(-1)`). Use `..<` or `array.indices`.

**`while` vs `repeat … while`:**

```swift
while condition { }          // may run zero times — tests first
repeat { } while condition   // always runs at least once — tests last
```

**Infinite loop with an explicit exit** (a run loop, a retry, a game tick):

```swift
while true {
    guard let next = queue.pop() else { break }
    process(next)
}
```

**Labelled breaks** — escape a nested loop from the inside:

```swift
outer: for row in grid {
    for cell in row {
        if cell == target {
            print("found")
            break outer          // leaves both loops; plain `break` leaves only the inner
        }
    }
}
```

**⚠️ You can't mutate a collection while iterating it:**

```swift
// for item in items { items.remove(...) }     ❌ / undefined-feeling behaviour
items.removeAll { $0.isExpired }               // ✅ do it in one pass
let kept = items.filter { !$0.isExpired }      // ✅ or build a new array
```

**`forEach` is not a `for` loop.** It takes a closure, so `break` and `continue` are unavailable, and `return` only exits the closure (one iteration), not the enclosing function:

```swift
items.forEach { if $0.isBad { return } }       // ⚠️ `return` = `continue`, not `break`
```

Use `for … in` whenever you might need to stop early.

**Prefer the functional form when you're building a value, not causing an effect:**

```swift
// imperative
var total = 0
for n in numbers { total += n }

// declarative — shorter and obviously correct
let total = numbers.reduce(0, +)
```

Loops are for side effects (printing, mutating, I/O). `map`/`filter`/`reduce` are for deriving values.

---

## 15. Functions

### Your notes

```swift
func printTimesTable(number: Int) {
    for i in 1...12 {
        print("\(i) x \(number) is \(i * number)")
    }
}

printTimesTable(number: 8)

func rollDice() -> Int {
    return Int.random(in: 1...6)
}

let result = rollDice()
print(result)
```

### What this shows

- `func name(param: Type) -> ReturnType { }`. No return arrow means the function returns `Void` (i.e. `()`).
- **Swift arguments are labelled at the call site.** `printTimesTable(number: 8)` — the label `number` is required unless you suppress or rename it (see [§17](#17-parameter-labels)).
- Parameters are **constants** inside the function. `number += 1` inside the body wouldn't compile.
- `rollDice` could drop the `return` entirely — a single-expression function has an implicit return.

### Going deeper

**Implicit return** for one-expression bodies:

```swift
func rollDice() -> Int { Int.random(in: 1...6) }      // `return` is implied
func double(_ x: Int) -> Int { x * 2 }
```

Works for computed properties and closures too. With more than one statement, `return` is mandatory.

**`inout` — let a function mutate the caller's variable:**

```swift
func doubleInPlace(_ number: inout Int) {
    number *= 2
}

var score = 10
doubleInPlace(&score)     // note the & at the call site
print(score)              // 20
```

Rules: the argument must be a `var`, you pass it with `&`, and you can't pass a literal or a `let`. Use it sparingly — returning a new value is usually clearer.

**Variadic parameters — zero or more of a type:**

```swift
func sum(_ numbers: Int...) -> Int {
    numbers.reduce(0, +)     // `numbers` is an [Int] inside
}
sum(1, 2, 3)      // 6
sum()             // 0
```

`print` itself is variadic: `print("a", "b", separator: " | ", terminator: "\n")`.

**`@discardableResult` — silence the "result unused" warning** (the one your `numbers.contains(11)` line produces):

```swift
@discardableResult
func save() -> Bool { true }

save()          // no warning now
_ = save()      // the alternative, without the attribute
```

**Functions are values.** You can store them, pass them, and return them:

```swift
func add(_ a: Int, _ b: Int) -> Int { a + b }

let operation: (Int, Int) -> Int = add
operation(2, 3)                       // 5

[1, 2, 3].reduce(0, add)              // 6 — pass a function where a closure is expected
["c", "a"].sorted(by: <)              // `<` is just a function
["1", "2"].compactMap(Int.init)       // initialisers are functions too
```

**Overloading** — same name, different signature. Swift picks by argument types *and* labels:

```swift
func show(_ x: Int)    { print("int \(x)") }
func show(_ x: String) { print("string \(x)") }
func show(value x: Int) { print("labelled \(x)") }   // labels alone can differentiate
```

**Nested functions** — keep a helper private to one function:

```swift
func process(_ items: [Int]) -> [Int] {
    func isValid(_ x: Int) -> Bool { x > 0 }
    return items.filter(isValid)
}
```

**Multiple return values:** a tuple for quick internal use, a struct once it outgrows that. See [Tuples](#16-tuples).

**Generic functions** — write it once for every type:

```swift
func swapValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a; a = b; b = temp
}

func firstOf<T: Comparable>(_ items: [T]) -> T? { items.min() }
```

**`some` and `any` (Swift 5.7+)** — you'll see these in modern APIs:

```swift
func render(_ shape: some Shape) { }   // one specific concrete type, chosen by the caller
func store(_ shape: any Shape) { }     // could be any conforming type, boxed at runtime
```

`some` is faster (static dispatch, no box). Reach for `any` only when you need heterogeneous storage like `[any Shape]`.

**`async` functions** — the modern concurrency shape, worth recognising now:

```swift
func fetchUser(id: Int) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// called as:
let user = try await fetchUser(id: 1)
```

`async` functions can only be called from another `async` context (or a `Task { }`).

**Naming convention:** read the call site, not the declaration. Swift style favours `printTimesTable(for: 8)` over `printTimesTableForNumber(8)` — the labels carry the prose. Methods that do something are verbs (`save()`, `remove(at:)`); methods that return something are noun phrases (`sorted()`, `distance(to:)`). Mutating/non-mutating pairs follow `sort()` / `sorted()`, `reverse()` / `reversed()`.

---

## 16. Tuples

### Your notes

```swift
func getUser() -> (firstName: String, lastName: String) {
    (firstName: "Taylor", lastName: "Swift")
}

let user = getUser()
print("Name: \(user.firstName) \(user.lastName)")
```

### What this shows

- A tuple bundles several values of **possibly different types** into one, without declaring a type.
- **Named** tuple members (`firstName:`) give you dot access and self-documenting code. Unnamed ones force `user.0` / `user.1`.
- The tuple's size and the type of each slot are **fixed at compile time** — unlike a dictionary, you can't ask for a key that isn't there, and you never get an Optional back.
- That body is a single expression, so the implicit return applies.

### Going deeper

**Destructuring on assignment:**

```swift
let (first, last) = getUser()
print(first)                            // "Taylor"

let (_, lastOnly) = getUser()           // `_` discards the parts you don't want
```

**Returning a value plus metadata — the classic use:**

```swift
func minMax(of numbers: [Int]) -> (min: Int, max: Int)? {
    guard let lo = numbers.min(), let hi = numbers.max() else { return nil }
    return (lo, hi)
}

if let bounds = minMax(of: [3, 1, 4]) {
    print(bounds.min, bounds.max)       // 1 4
}
```

Note you can return a tuple without repeating the labels — they come from the signature.

**Tuples in the standard library** — you're already using them:

```swift
for (index, value) in array.enumerated() { }             // (offset:, element:)
for (key, value) in dictionary { }                       // (key:, value:)
set.insert(x)                                            // (inserted:, memberAfterInsert:)
17.quotientAndRemainder(dividedBy: 5)                    // (quotient:, remainder:)
Int.max.addingReportingOverflow(1)                       // (partialValue:, overflow:)
try await URLSession.shared.data(from: url)              // (Data, URLResponse)
```

**Comparison is synthesised for up to 6 elements**, left to right:

```swift
(1, "a") == (1, "a")        // true
(1, "a") < (1, "b")         // true  — first elements tie, so the second decides
(2, "a") < (1, "z")         // false — decided by the first element alone
```

That makes tuples a neat multi-key sort:

```swift
people.sorted { ($0.lastName, $0.firstName) < ($1.lastName, $1.firstName) }
```

**Tuples in a `switch`** — see [§12](#12-switch); pattern matching on tuples is one of their best uses.

**⚠️ The limits — and when to use a struct instead:**

```swift
// Tuples cannot conform to protocols:
// extension (Int, Int): Equatable { }      ❌ not allowed
```

So a tuple can't be `Codable`, `Hashable`, `Identifiable`, or a dictionary key; it can't have methods or computed properties; and it can't be used as a SwiftUI `Identifiable` model. Labels are also not part of the type in a way you can rely on across boundaries.

**The rule:** tuple for a *transient, local, two-or-three-value* return. Struct the moment it (a) crosses a module or public API boundary, (b) grows past three members, (c) needs any behaviour, or (d) you catch yourself writing the same tuple type twice.

```swift
// Outgrown a tuple:
struct User {
    let firstName: String
    let lastName: String
    var fullName: String { "\(firstName) \(lastName)" }   // ← a tuple couldn't do this
}
```

**Void is a tuple.** `Void` is literally a type alias for the empty tuple `()`, which is why `-> Void` and `-> ()` are interchangeable.

---

## 17. Parameter labels

### Your notes

```swift
// No argument label at all
func isUppercase(_ string: String) -> Bool {
    string == string.uppercased()
}

let string = "Hello world"
let result = isUppercase(string)         // no label needed

// A custom external label
func printTimesTable(for number: Int) {
    for i in 1...12 {
        print("\(i) x \(number) is \(i * number)")
    }
}

printTimesTable(for: 5)
```

### What this shows

- Every parameter has an **external name** (what callers type) and an **internal name** (what the body uses). By default they're the same word.
- `_ string: String` — `_` means *no external label*. Callers write `isUppercase(x)`.
- `for number: Int` — external `for`, internal `number`. Callers write `printTimesTable(for: 5)` while the body reads `number`, which is what makes both sides read naturally.
- This is the whole reason Swift call sites look like sentences.

### Going deeper

**The three forms side by side:**

```swift
func a(number: Int) { }      // a(number: 5)     — label == internal name (default)
func b(_ number: Int) { }    // b(5)             — no label
func c(for number: Int) { }  // c(for: 5)        — different label and name
```

**When to use `_`:** when the argument *is* the subject of the verb, and a label would just repeat the function name.

```swift
print(x)                          // not print(value: x)
isUppercase(string)               // not isUppercase(string: string)  ← stutter
array.contains(element)
abs(-5)

func send(_ message: String, to recipient: User) { }
send("hi", to: varun)             // reads like English
```

**When to use a custom label:** when a preposition makes the call site a sentence. Swift's own API is full of these:

```swift
array.remove(at: 0)               // at
array.index(of: x)                // of
string.hasPrefix("He")            // no label — it's the direct object
Int.random(in: 1...6)             // in
view.addSubview(child)
constraint(equalTo: other, multiplier: 2)
```

**The API Design Guidelines rule of thumb:** the first argument usually reads as a continuation of the function name, and subsequent arguments almost always keep labels.

```swift
// ✅ grammatical at the call site
func move(from start: Point, to end: Point)
move(from: a, to: b)

// ❌ labels that add nothing
func move(fromStart: Point, toEnd: Point)
move(fromStart: a, toEnd: b)
```

**Labels are part of the function's identity.** These are three different functions, and you refer to them by their full names:

```swift
func show(_ x: Int) { }
func show(value x: Int) { }
func show(number x: Int) { }

let f = show(value:)              // pick one by its full name
```

That's also why you'll see documentation write `remove(at:)`, `sorted(by:)`, `data(from:)` — the labels are the name.

**Argument order matters, labels don't rescue you:**

```swift
func rect(width: Int, height: Int) { }
// rect(height: 2, width: 1)      ❌ error — arguments must be in declared order
```

(Unlike a few other languages, Swift won't reorder for you.)

**Closure parameters never have labels.** This is why the `_` in your `sayCoolerHello` closure was unnecessary — see [§20](#20-closures).

---

## 18. Default parameter values

### Your notes

```swift
func greet(_ person: String, formal: Bool = false) {
    if formal {
        print("Welcome, \(person)")
    } else {
        print("Hi, \(person)")
    }
}

greet("Varun", formal: true)      // "Welcome, Varun"
greet("Varun")                    // "Hi, Varun"
```

### What this shows

- `= false` makes the parameter optional *at the call site* — omit it and the default is used. This is not the same as an `Optional`; `formal` is always a real `Bool` inside.
- One function now serves two call shapes, so you don't write two overloads.
- Defaults must be on parameters callers can skip, which in practice means **put defaulted parameters last**.

### Going deeper

**Defaults you'll see in the standard library:**

```swift
print("a", "b")                                           // separator: " ", terminator: "\n"
print("a", "b", separator: "-", terminator: "")

array.removeAll(keepingCapacity: false)
string.split(separator: ",", maxSplits: .max,
             omittingEmptySubsequences: true)
dict["k", default: 0]
```

**Defaults compose with labels for very readable APIs:**

```swift
func fetch(_ url: URL,
           method: String = "GET",
           timeout: TimeInterval = 30,
           retries: Int = 3,
           cachePolicy: URLRequest.CachePolicy = .useProtocolCachePolicy) { }

fetch(url)                                 // the common case stays short
fetch(url, method: "POST", retries: 0)     // override only what differs — in order
```

You still have to supply overrides in declaration order, but you can skip any of them.

**Defaults are evaluated at each call, not once:**

```swift
func log(_ message: String, at time: Date = Date()) { }
log("a")     // Date() runs now
log("b")     // Date() runs again — a fresh timestamp, not a cached one
```

**The magic default arguments** — great for logging helpers:

```swift
func trace(_ message: String,
           file: String = #fileID,
           line: Int = #line,
           function: String = #function) {
    print("[\(file):\(line)] \(function) — \(message)")
}

trace("here")     // fills in the *caller's* file and line automatically
```

**A defaulted parameter vs an Optional parameter — different meanings:**

```swift
func a(name: String = "Anon") { }        // "you may omit it; I'll use Anon"
func b(name: String?) { }                // "you must pass something, possibly nil"
func c(name: String? = nil) { }          // "you may omit it; absence is meaningful"
```

Use `c` when "not provided" needs to be distinguishable inside the function (e.g. a PATCH request where `nil` means *don't change this field*).

**⚠️ Defaults and protocols don't mix well.** A protocol requirement can't declare a default value; you put it on the concrete implementation or on a protocol-extension method. And overriding a method in a subclass doesn't inherit the parent's defaults — restate them.

**Trailing closures still work with defaults:**

```swift
func animate(duration: TimeInterval = 0.3, _ body: () -> Void) { }
animate { view.alpha = 0 }               // duration defaults, closure trails
```

---

## 19. Error handling

### Your notes

```swift
enum PasswordError: Error {
    case short, obvious
}

func checkPassword(_ password: String) throws -> String {
    if password.count < 5 { throw PasswordError.short }
    if password == "12345" { throw PasswordError.obvious }

    if password.count < 10 { return "OK" }
    else { return "Good" }
}

do {
    let result = try checkPassword("12345")
} catch PasswordError.obvious {
    print("I have the same combination on my luggage")
} catch {
    print("there was an error")
}
```

### What this shows

- **Errors are just values.** Any type conforming to the empty `Error` protocol works; an enum is the natural fit because your failure modes are a closed set.
- `throws` in the signature, `throw` to raise, `try` at the call site, `do`/`catch` to handle. The compiler enforces every step — you *cannot* call a throwing function without `try`.
- `catch` clauses are **pattern matched top to bottom**, exactly like `switch`. `catch PasswordError.obvious` handles that one case; the bare `catch` at the end catches everything else.
- A `do` block needs a bare `catch` (or the enclosing function must itself be `throws`) — unlike `switch`, Swift can't prove your catches are exhaustive.
- `"12345"` is 5 characters, so it passes the `< 5` check and trips `.obvious` — this prints *"I have the same combination on my luggage"*. Nice test case.
- Small thing: `let result` is never read, so you'll get an *"unused value"* warning. Use `_ = try …` or actually print it.

### Going deeper

**`try?` and `try!` — the two shortcuts:**

```swift
let a = try? checkPassword("12345")     // String?  — nil on any error, error discarded
let b = try! checkPassword("longenough") // String  — 💥 crashes if it throws
```

`try?` is right when you genuinely don't care *why* it failed. `try!` is only for cases that are impossible by construction (a hard-coded regex, a bundled resource) — treat it like an assertion.

Combine `try?` with `??` for a one-liner fallback:

```swift
let strength = (try? checkPassword(pw)) ?? "unknown"
```

**Catching by type, and reading the error value:**

```swift
do {
    try risky()
} catch PasswordError.short {
    print("too short")
} catch let error as PasswordError {
    print("a password problem: \(error)")
} catch let error as URLError where error.code == .timedOut {
    print("network timed out")
} catch {
    print("unexpected: \(error)")        // `error` is implicitly available here
}
```

Multiple patterns in one clause work too: `catch PasswordError.short, PasswordError.obvious {`.

**Carry context in the error, not just the case:**

```swift
enum ValidationError: Error {
    case tooShort(minimum: Int, got: Int)
    case missingCharacter(Character)
}

throw ValidationError.tooShort(minimum: 5, got: password.count)

// and at the catch site:
catch ValidationError.tooShort(let minimum, let got) {
    print("Needs \(minimum) characters, you gave \(got)")
}
```

This is the single biggest upgrade to your current enum — associated values turn an error into a useful diagnostic.

**`LocalizedError` for messages you can show a user:**

```swift
enum PasswordError: LocalizedError {
    case short, obvious

    var errorDescription: String? {
        switch self {
        case .short:   "Your password is too short."
        case .obvious: "Your password is too easy to guess."
        }
    }
}

catch { print(error.localizedDescription) }
```

Without `LocalizedError`, `localizedDescription` on your enum gives a useless *"The operation couldn't be completed"* string.

**`defer` — cleanup that runs no matter how you leave the scope:**

```swift
func process(_ path: String) throws {
    let file = try open(path)
    defer { file.close() }        // runs on return AND on throw
    try file.write("data")        // if this throws, the file still closes
}
```

Multiple `defer` blocks run in reverse order (LIFO).

**Propagating instead of handling** — most functions should just add `throws` and let the caller decide:

```swift
func signUp(password: String) throws {
    let strength = try checkPassword(password)   // no do/catch — the error flows up
    print(strength)
}
```

**`rethrows`** — for functions that only throw because their closure argument does:

```swift
func withLogging<T>(_ work: () throws -> T) rethrows -> T {
    print("starting")
    defer { print("finished") }
    return try work()
}

withLogging { 42 }                     // no `try` needed — the closure doesn't throw
try withLogging { try fetch() }        // `try` needed — it does
```

`map`, `filter`, `reduce` and `forEach` are all `rethrows`, which is why they work with both throwing and non-throwing closures.

**`Result` — an error as a return value instead of a thrown one.** Useful for callbacks and for storing a failure:

```swift
func check(_ pw: String) -> Result<String, PasswordError> {
    if pw.count < 5 { return .failure(.short) }
    return .success("OK")
}

switch check("abc") {
case .success(let s): print(s)
case .failure(let e): print(e)
}

// Bridging both ways:
let r = Result { try checkPassword("12345") }     // throwing → Result
let v = try r.get()                                // Result → throwing
```

**Typed throws (Swift 6)** — narrow `throws` to exactly one error type, so callers get exhaustive catching:

```swift
func checkPassword(_ pw: String) throws(PasswordError) -> String { … }

do {
    try checkPassword(pw)
} catch .short {                 // no `default` needed, no `as` casts
    print("short")
} catch .obvious {
    print("obvious")
}
```

**Errors vs crashes — pick deliberately:**

| Situation | Tool |
|---|---|
| Expected, recoverable failure (bad input, network down) | `throws` / `Result` |
| Programmer error that should never ship | `precondition`, `assert`, `fatalError` |
| Value might legitimately be absent | `Optional`, not an error |

Don't throw for "no results found" — that's an empty array or a `nil`.

---

## 20. Closures

### Your notes

```swift
let sayHello = {
    print("hello")
}
sayHello()

let sayCoolerHello = { (_ string: String) -> Void in
    print("Hi, \(string)")
}
sayCoolerHello("Varun")

// Passing a closure to filter
let team = ["Gloria", "Suzzanne", "Tiffany", "Tasha", "trisha"]

let onlyT = team.filter({ (name: String) -> Bool in
    return name.lowercased().hasPrefix("t")
})
print(onlyT)      // ["Tiffany", "Tasha", "trisha"]
```

**Your own notes on shortening it — all correct:**
- You can remove `return` from a one-line closure.
- If something is obvious you can remove it — parameter types, the return type.
- You can move the closure outside the `()` → **trailing closure syntax**.
- You can use shorthand argument names like `$0` instead of naming the parameter.

### What this shows

- A closure is a **function without a name**, stored in a variable. `{ … }` is the body; `in` separates the signature from the body.
- `sayHello` has type `() -> Void`. `sayCoolerHello` has type `(String) -> Void`.
- Calling it looks like calling a function, because it *is* one.
- **Closures have no argument labels.** That's why `sayCoolerHello("Varun")` takes no label — and why the `_` you wrote in `(_ string: String)` is redundant. Closure parameters are always positional.
- `filter` takes a `(Element) -> Bool` and keeps every element the closure returns `true` for. It returns a *new* array; `team` is untouched.

### The shortening ladder, step by step

Each line below is the same `filter` call. Watch what the compiler can infer away:

```swift
// 1. Everything spelled out
let onlyT = team.filter({ (name: String) -> Bool in
    return name.lowercased().hasPrefix("t")
})

// 2. Drop the parameter type — filter already knows it's a String
let onlyT = team.filter({ name -> Bool in
    return name.lowercased().hasPrefix("t")
})

// 3. Drop the return type — inferred from the body
let onlyT = team.filter({ name in
    return name.lowercased().hasPrefix("t")
})

// 4. Drop `return` — single expression, implicit return
let onlyT = team.filter({ name in name.lowercased().hasPrefix("t") })

// 5. Trailing closure — the last argument moves outside the parens
let onlyT = team.filter { name in name.lowercased().hasPrefix("t") }

// 6. Shorthand argument name — $0 is the first parameter
let onlyT = team.filter { $0.lowercased().hasPrefix("t") }
```

Step 6 is the idiomatic one. `$0`, `$1`, `$2` are the first, second, third parameters:

```swift
[3, 1, 2].sorted { $0 < $1 }        // or just .sorted(by: <)
zip(a, b).map { $0 + $1 }
dict.sorted { $0.key < $1.key }     // $0 and $1 are the two (key, value) tuples
```

**Know when to stop shortening.** `$0` is great for one short expression. Once the body has two or more statements, or `$0.something.something.else`, name the parameter — future-you has to read it:

```swift
// ❌ too clever
items.filter { $0.tags.contains { $0.isActive } }      // which $0 is which?

// ✅
items.filter { item in item.tags.contains { tag in tag.isActive } }
```

### Going deeper

**Closures capture their surrounding scope.** This is the whole point of the word "closure" — it closes *over* the variables around it:

```swift
func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1        // `count` is captured by reference and lives on
        return count
    }
}

let next = makeCounter()
next()     // 1
next()     // 2
next()     // 3  — `count` outlived the function that declared it
```

**⚠️ Closures are reference types.** Two variables pointing at the same closure share captured state:

```swift
let a = makeCounter()
let b = a          // same closure, same captured count
a()                // 1
b()                // 2  ← not 1
```

This is the one place value semantics don't apply in the code you've written so far.

**Capture lists** — control *how* things are captured. Essential in classes:

```swift
class ViewModel {
    var name = "Varun"

    func load() {
        api.fetch { [weak self] data in           // ✅ avoids a retain cycle
            guard let self else { return }
            self.name = data.name
        }
    }
}
```

- `[weak self]` → `self` becomes an Optional; it can become `nil` if the object is deallocated. The default safe choice for async callbacks.
- `[unowned self]` → non-optional, but crashes if `self` is gone. Only when you can prove the lifetime.
- No capture list → strong capture. If the object also holds the closure, you've built a **retain cycle** and it leaks.

Capture-by-value is also useful:

```swift
var x = 10
let printX = { [x] in print(x) }    // captures the value 10 right now
x = 99
printX()                            // 10 — not 99
```

**`@escaping`** — required when a closure outlives the function call (stored, or used after an `await`/callback):

```swift
var handlers: [() -> Void] = []

func register(_ handler: @escaping () -> Void) {   // stored → must escape
    handlers.append(handler)
}

func runNow(_ work: () -> Void) {                  // used immediately → non-escaping
    work()
}
```

Non-escaping is the default and the faster path — the compiler can stack-allocate. Inside an escaping closure that captures `self`, you must write `self.` explicitly; that's the compiler forcing you to notice the capture.

**Multiple trailing closures (Swift 5.3+)** — the second and later ones keep their labels:

```swift
UIView.animate(withDuration: 0.3) {
    view.alpha = 0
} completion: { _ in
    view.removeFromSuperview()
}
```

**Closures as stored properties and type aliases:**

```swift
typealias Completion = (Result<Data, Error>) -> Void

struct Button {
    var title: String
    var action: () -> Void = { }        // a default no-op
}

let b = Button(title: "Save") { print("saved") }    // trailing closure into the init
b.action()
```

**`@autoclosure`** — wrap an expression in a closure automatically so it's evaluated lazily. This is how `??` and `assert` avoid doing work they don't need:

```swift
func logIfEnabled(_ message: @autoclosure () -> String) {
    if isLoggingEnabled { print(message()) }
}

logIfEnabled("expensive \(buildHugeString())")   // the string is only built if enabled
```

**The functional trio, with closures, all together:**

```swift
let people = [("Ana", 31), ("Bo", 17), ("Cy", 45)]

people
    .filter { $0.1 >= 18 }              // adults only
    .map { $0.0.uppercased() }          // just the names, shouting
    .sorted()                           // ["ANA", "CY"]

people.reduce(0) { $0 + $1.1 }          // 93 — total age
people.max { $0.1 < $1.1 }              // Optional(("Cy", 45))
```

**Performance note: `lazy`.** Chained `map`/`filter` each allocate an intermediate array. On a big collection where you only need the first few results, `lazy` fuses the chain and stops early:

```swift
let firstBig = numbers.lazy.map { expensive($0) }.first { $0 > 100 }
// `expensive` runs only until the first match, and no intermediate array is built
```

---

## 21. Structs

### Your notes — properties, methods and `mutating`

```swift
struct Album {
    let title: String
    let artist: String
    var isReleased = true

    func printSummary() {
        print("\(title) by \(artist)")
    }

    mutating func removeFromSales() {
        isReleased = false
    }
}

let red = Album(title: "Red", artist: "Taylor Swift")
print(red.title)
red.printSummary()        // "Red by Taylor Swift"
```

**What this shows**

- **Stored properties** (`title`, `artist`, `isReleased`) hold values; `isReleased = true` gives a default so the initialiser can omit it.
- You get a **memberwise initialiser for free**: `Album(title:artist:isReleased:)`, and because `isReleased` has a default, `Album(title:artist:)` also works.
- Inside a method, properties are reachable without `self.` — `title` just works.
- **`mutating`** is required on any method that changes a stored property. It's the compiler's way of tracking which methods can be called on a `let`.

**⚠️ The catch you haven't hit yet:** `red` is a `let`, so this won't compile:

```swift
// red.removeFromSales()
// ❌ Cannot use mutating member on immutable value: 'red' is a 'let' constant
var mutableRed = Album(title: "Red", artist: "Taylor Swift")
mutableRed.removeFromSales()      // ✅
```

`printSummary()` is fine on a `let` precisely *because* it isn't `mutating`. Mark the minimum set of methods `mutating` and the compiler does this bookkeeping for you.

### Your notes — computed properties with `get` / `set`

```swift
struct Employee {
    let name: String
    var vacationAllowed = 14
    var vacationTaken = 0

    var vacationRemaining: Int {
        get {
            vacationAllowed - vacationTaken
        }
        set {
            vacationAllowed = vacationTaken - newValue   // ⚠️ bug
        }
    }
}

var employee = Employee(name: "varun")
employee.vacationRemaining = 5
print(employee.vacationAllowed)
```

**What this shows**

- A **computed property** has no storage — it runs code every time it's read. `vacationRemaining` is always derived from the two stored values, so it can never go stale.
- `get` returns the value; `set` receives the assigned value in the implicit constant **`newValue`** (you can rename it: `set(newRemaining) { … }`).
- A getter-only computed property can drop the `get { }` wrapper entirely — that's why the read-only ones elsewhere in these notes are written as `var x: Int { … }`.

**⚠️ Bug 2: the setter has its arithmetic backwards**

You want: *"if the employee should have 5 days remaining, and they've taken `vacationTaken`, then their allowance must be `vacationTaken + 5`."*

```swift
set { vacationAllowed = vacationTaken - newValue }   // ❌ 0 - 5 = -5
set { vacationAllowed = vacationTaken + newValue }   // ✅ 0 + 5 = 5
```

With `vacationTaken == 0`, your version prints **-5**. Sanity-check a setter by asserting the round trip — *set it, read it back, get the same number:*

```swift
var e = Employee(name: "varun")
e.vacationTaken = 3
e.vacationRemaining = 5
print(e.vacationRemaining)    // should print 5 — with the fix it does, before it didn't
```

Any `get`/`set` pair should satisfy `x.p = v; x.p == v`. That one line would have caught it.

### Your notes — property observers

```swift
struct Game {
    var score = 0 {
        didSet {
            print("Score has changed")
        }
    }
}

var game = Game()
game.score += 1        // prints "Score has changed"
```

**What this shows**

- `didSet` fires **after** a stored property changes; `willSet` fires **before**. They attach to *stored* properties (a computed property just uses its `set`).
- Inside `didSet` you get **`oldValue`**; inside `willSet` you get **`newValue`**.

```swift
struct Game {
    var score = 0 {
        willSet { print("about to go from \(score) to \(newValue)") }
        didSet  { print("went from \(oldValue) to \(score)") }
    }
}
```

**⚠️ Two observer gotchas:**

1. **Observers never fire during initialisation.** Setting a property in `init` runs no `didSet`. If you need side effects on the initial value, call them explicitly from `init`.
2. **Assigning the same value still fires them.** `game.score = 0` on a fresh `Game` prints anyway — Swift doesn't diff. Guard it yourself if that matters:

```swift
didSet {
    guard score != oldValue else { return }
    saveHighScore()
}
```

Keep observer bodies cheap. A `didSet` that does network I/O is a debugging nightmare, because it fires from every assignment site in your app.

### Your notes — custom initialisers

```swift
struct Player {
    var name: String
    var score: Int

    init(_ name: String, _ score: Int) {
        self.name = name
        self.score = score
    }
}

let player = Player("Varun", 20)
```

**What this shows**

- An `init` has no `func` keyword and no return type; its job is to leave **every** stored property initialised. The compiler won't let you finish otherwise.
- `self.name = name` — `self.` disambiguates the property from the same-named parameter. Without the shadowing you wouldn't need it.
- `_ name:` `_ score:` strip the labels, giving you a positional `Player("Varun", 20)`.

**⚠️ Writing a custom `init` inside the struct removes the free memberwise one:**

```swift
// Player(name: "Varun", score: 20)
// ❌ Extraneous argument labels 'name:score:' — the memberwise init is gone
```

**The workaround worth knowing: declare your custom `init` in an extension and you keep both.**

```swift
struct Player {
    var name: String
    var score: Int
}

extension Player {
    init(_ name: String) {
        self.init(name: name, score: 0)     // delegate to the memberwise init
    }
}

Player(name: "Varun", score: 20)    // ✅ memberwise, still there
Player("Varun")                     // ✅ yours
```

This trick applies to structs only, and it's why library authors often put convenience initialisers in extensions.

### Your notes — access control with `private(set)`

```swift
struct BankAccount {
    private(set) var funds = 0

    mutating func deposit(amount: Int) {
        funds += amount
    }

    mutating func withdraw(amount: Int) -> Bool {
        if funds > amount {
            funds -= amount
            return true
        } else {
            return false
        }
    }
}

var account = BankAccount(funds: 100)
print(account.funds)        // 100
account.funds += 1          // ← the demo: this does not compile
```

**What this shows**

- **`private(set)`** splits a property in two: the **getter stays visible**, the **setter becomes private**. Outside code can read `funds` all it likes and can never write to it. Verified error on that last line:

```
error: left side of mutating operator isn't mutable: 'funds' setter is inaccessible
```

- That's the whole design: `deposit` and `withdraw` become the *only* doors into `funds`, so every change goes through your validation. Compare plain `private` (invisible outside entirely) and plain `var` (anyone can write anything).
- Both mutators are `mutating` because they write a stored property on a struct.
- `withdraw` returning `Bool` is the right shape for an operation that can legitimately be refused — the caller must deal with the answer.

**One thing that surprised me, so I checked it:** `BankAccount(funds: 100)` **does** compile. The free memberwise initialiser still takes a `funds:` parameter even though the setter is private — verified, it prints `100`. So `private(set)` guards *later* mutation, not the initial value:

```swift
var sneaky = BankAccount(funds: 1_000_000)   // ✅ compiles — bypasses deposit() entirely
```

If you want the starting balance controlled too, write an initialiser and the memberwise one goes away ([§21 custom initialisers](#21-structs)):

```swift
struct BankAccount {
    private(set) var funds: Int

    init(openingBalance: Int = 0) {
        funds = max(0, openingBalance)       // now every path is validated
    }
}
```

**On the `withdraw` boundary** — verified with `funds == 100`:

```swift
account.withdraw(amount: 100)    // false, funds stay 100   (funds > amount is false)
account.withdraw(amount: 99)     // true,  funds become 1
```

So you can never withdraw your whole balance. If that's intentional (a minimum balance rule) it's fine; if you meant "withdraw anything you can afford", it's `funds >= amount`.

### Your notes — `static` properties

```swift
struct AppData {
    static let version = "1.3 beta 2"
    static let settingsFile = "settings.json"
}

print(AppData.version)      // 1.3 beta 2
```

**What this shows**

- **`static` members belong to the type, not to an instance.** There's one `version` for the whole program, and you reach it through the type name — `AppData.version`, never `AppData().version`.
- This struct has no instance properties at all, which is a deliberate and common pattern: `AppData` is a **namespace** for constants rather than something you create. You never write `AppData()`.
- `static let` constants are also **lazily initialised and thread-safe** — Swift guarantees the value is computed at most once, on first access, even from multiple threads. That makes this pattern safe for expensive values too.

A caseless `enum` is often preferred for exactly this job, because it makes instantiation *impossible* rather than merely pointless:

```swift
enum AppData {
    static let version = "1.3 beta 2"
    static let settingsFile = "settings.json"
}

// AppData()   ❌ won't compile at all — an enum with no cases cannot be instantiated
```

With the struct, `AppData()` compiles (via the empty memberwise init) and gives you a useless empty value. Both work; the enum states the intent.

### Going deeper — the rest of the struct toolbox

**`static` beyond constants** — building on your `AppData` above, a static member can also be mutable state or a factory:

```swift
struct Player {
    var name: String
    static var count = 0                     // shared mutable state — one per type
    static let maxScore = 100

    init(name: String) {
        self.name = name
        Player.count += 1                    // or Self.count
    }

    static func makeGuest() -> Player { Player(name: "Guest") }
}

Player.maxScore          // accessed on the type
Player.makeGuest()
```

`Self` (capital S) means "the type I'm in", so `Self.count` survives a rename. Note that `static var` is genuinely shared mutable state — in concurrent code Swift 6 will flag it unless it's `let` or protected.

You'll see static properties constantly in SwiftUI/UIKit as `Color.blue`, `.systemFont`, `.zero` — and the leading-dot shorthand works for them too.

**`lazy var` — compute once, on first access:**

```swift
struct DataStore {
    lazy var expensiveIndex: [String: Int] = buildIndex()      // not built until read
}

var store = DataStore()        // nothing happens
store.expensiveIndex           // built now, cached from here on
```

Requirements: must be `var` (it mutates on first read), can't be a computed property, and reading it on a struct requires the struct itself be `var`. Not thread-safe — two concurrent first-reads can both run the initialiser.

**The full access-control ladder**, from your `private(set)` outward:

```swift
struct Vault {
    private var pin = "0000"            // this type (and its extensions in the file) only
    fileprivate var debugID = ""        // anywhere in this file
    private(set) var balance = 0        // read anywhere, write only inside  ← yours
    internal var owner = ""             // the whole module (the default)
    public var currency = "INR"         // other modules too
                                        // `open` also exists, for subclassable classes
}
```

`private(set)` is the one you'll reach for most — a read-only public surface over mutable internal state, exactly as your `BankAccount` does.

**Free protocol conformances.** Add the protocol and the compiler writes the implementation, as long as every stored property already conforms:

```swift
struct Album: Equatable, Hashable, Codable, Identifiable {
    var id = UUID()
    var title: String
    var artist: String
}

albumA == albumB                                   // Equatable, synthesised
Set([albumA, albumB])                              // Hashable, synthesised
try JSONEncoder().encode(albumA)                   // Codable, synthesised
try JSONDecoder().decode(Album.self, from: data)
ForEach(albums) { … }                              // Identifiable — SwiftUI needs this
```

Add `Comparable` and you must supply `<` yourself (there's no sensible default ordering to guess):

```swift
extension Album: Comparable {
    static func < (lhs: Album, rhs: Album) -> Bool { lhs.title < rhs.title }
}
albums.sorted()      // now works
```

**Extensions — add behaviour without touching the original type,** including to types you don't own:

```swift
extension Album {
    var isTaylor: Bool { artist == "Taylor Swift" }
    func renamed(to newTitle: String) -> Album {
        var copy = self; copy.title = newTitle; return copy     // value semantics!
    }
}

extension String {
    var trimmed: String { trimmingCharacters(in: .whitespacesAndNewlines) }
}
extension Int {
    var isEven: Bool { isMultiple(of: 2) }
}
```

Extensions can add computed properties, methods, initialisers, nested types and conformances — but **not stored properties** (there's nowhere to put them).

**Protocols — describe capability, then get free implementations from an extension:**

```swift
protocol Describable {
    var name: String { get }
    func summary() -> String
}

extension Describable {
    func summary() -> String { "This is \(name)" }     // default implementation
}

struct Album: Describable {
    var title: String
    var name: String { title }
    // summary() comes free
}
```

This "protocol + extension" pairing is the backbone of Swift's answer to inheritance, and it works on structs, enums and classes alike.

**A worked example pulling it together:**

```swift
struct Album: Identifiable, Equatable, Codable, CustomStringConvertible {
    let id: UUID
    let title: String
    let artist: String
    private(set) var isReleased: Bool
    var playCount = 0 {
        didSet {
            guard playCount != oldValue else { return }
            if playCount == 1 { print("first play of \(title)") }
        }
    }

    static let maxTitleLength = 100

    var description: String { "\(title) by \(artist)" }
    var isPopular: Bool { playCount > 1_000 }

    init(title: String, artist: String, isReleased: Bool = true) {
        self.id = UUID()
        self.title = String(title.prefix(Self.maxTitleLength))
        self.artist = artist
        self.isReleased = isReleased
    }

    mutating func withdraw() { isReleased = false }
    func renamed(to newTitle: String) -> Album {
        Album(title: newTitle, artist: artist, isReleased: isReleased)
    }
}
```

Note: a custom `init` *plus* a mutating method *plus* `private(set)` gives you a type where the only legal state transitions are the ones you wrote. That's the real payoff of structs — you design away the invalid states.

---

## 22. Classes & inheritance

### Your notes — subclassing and `override`

```swift
class Employee {
    let hours: Int

    init(hours: Int) {
        self.hours = hours
    }

    func printSummary() {
        print("I work \(hours) hours a day.")
    }
}

class Developer: Employee {
    func work() {
        print("I'm coding for \(hours) hours a day.")
    }

    override func printSummary() {
        print("I spend \(hours) hours a day fighting over tabs over spaces")
    }
}
```

**What this shows**

- `class Developer: Employee` means Developer **is an** Employee — it gets `hours`, `init(hours:)` and `printSummary()` for free, and can add `work()` on top.
- **`override` is mandatory.** Drop the keyword and you get *"overriding declaration requires an 'override' keyword"*; add it where the parent has no such method and you get *"method does not override any method from its superclass"*. Swift refuses to let you shadow a parent method by accident.
- Inheritance is **classes only**. Structs and enums can't subclass — they compose via protocols instead ([§23](#23-protocols)).

**Verified output, including the bit worth noticing:**

```swift
let dev = Developer(hours: 8)
dev.work()              // I'm coding for 8 hours a day.
dev.printSummary()      // I spend 8 hours a day fighting over tabs over spaces

let asEmployee: Employee = dev
asEmployee.printSummary()
// I spend 8 hours a day fighting over tabs over spaces   ← NOT the Employee version
```

That last line is **dynamic dispatch**: the method that runs is chosen by the object's *actual* type at runtime, not by the type of the variable holding it. It's the entire point of `override`, and it's the one thing structs genuinely cannot do.

### Your notes — three rules about class initialisers

> - For classes, there won't be a memberwise initializer made for them unlike struct
> - Classes' initializer will have to call the parent's initializer
> - If a class has no initializer, it will automatically call the parent's initializer

The first two are exactly right. The third is *almost* right and the precise version matters, so here it is checked against the compiler:

**1. No memberwise init for classes — correct.** ✅ You must write `init` yourself:

```swift
class Employee {
    let hours: Int
    init(hours: Int) { self.hours = hours }   // no free Employee(hours:) — you write it
}
```

Why the asymmetry? A struct's memberwise init is always safe because there's no superclass whose invariants you might skip. A class could be subclassed, so Swift makes you be explicit.

**2. A subclass initialiser must call `super.init` — correct**, whenever the superclass has stored properties to set up. The compiler enforces it: omit the `super.init` call and you get *"super.init isn't called on all paths before returning from initializer"*.

**3. The refinement.** A subclass doesn't "automatically call" the parent's initialiser — it **inherits** the parent's initialisers, and only under two conditions:

- it declares **no initialisers of its own**, and
- every stored property it adds has a **default value**.

Both hold, and inheritance works:

```swift
class Bike: Vehicle { }                  // no init, no new properties
class Van: Vehicle { var seats = 2 }     // new property, but it has a default
Bike(isElectric: true)                   // ✅ inherited initialiser
Van(isElectric: false)                   // ✅ inherited initialiser
```

Add an uninitialised property and the inheritance stops dead — verified error text:

```swift
class Truck: Vehicle { var axles: Int }
// ❌ error: class 'Truck' has no initializers
//    note: stored property 'axles' without initial value prevents synthesized initializers
```

That's the rule in one line: **give every new property a default and you keep the parent's initialisers; leave one bare and you must write your own.** Note this is also why `Developer` above needs no `init` — it adds no stored properties at all.

### Your notes — `super.init` and two-phase initialisation

```swift
class Vehicle {
    let isElectric: Bool
    init(isElectric: Bool) {
        self.isElectric = isElectric
    }
}

class Car: Vehicle {
    let isConvertible: Bool
    init(isElectric: Bool, isConvertible: Bool) {
        self.isConvertible = isConvertible       // 1. own properties first
        super.init(isElectric: isElectric)       // 2. then hand off upward
    }
}
```

**Your ordering here is correct, and it's not a style choice — it's required.** Swift initialises in two phases:

- **Phase 1:** every stored property on the whole chain gets a value, working from the subclass upward. You may not touch `self`, call methods, or read inherited properties yet.
- **Phase 2:** once `super.init` has returned, `self` is fully formed — now you can call methods and further customise.

Reverse the two lines and the compiler stops you. Verified:

```swift
init(isElectric: Bool, isConvertible: Bool) {
    super.init(isElectric: isElectric)
    self.isConvertible = isConvertible
}
// ❌ error: immutable value 'self.isConvertible' may only be initialized once
//    note: change 'let' to 'var' to make it mutable
```

The reason: after `super.init` returns, `isConvertible` has *already* been given its value as part of phase 1, so assigning it again is a second initialisation of a `let`. Own properties first, then `super.init`, then any extra work.

### Your notes — reference semantics

```swift
class Actor {
    var name = "Nicolas Cage"
}

var actor1 = Actor()
var actor2 = actor1

actor2.name = "Tom Cruise"

print(actor1.name)      // Tom Cruise
print(actor2.name)      // Tom Cruise
```

**What this shows**

- **Both names point at one object.** `var actor2 = actor1` copies the *reference*, not the instance, so writing through `actor2` is visible through `actor1`. This is the exact counterpart to the `Person` struct in [§1](#1-value-types--reference-semantics), where the same code printed two different names.
- `actor1 === actor2` is `true` — `===` tests *identity* (same object) as opposed to `==` (equal contents). Only classes have it.
- Two variables sharing mutable state is the whole reason classes exist, and equally the reason they're harder to reason about across threads.

(Side note: `Actor` is also the name of a protocol in Swift's concurrency library. Your class shadows it locally and compiles fine — just expect the name to look crowded in autocomplete.)

### Your notes — `deinit`

```swift
class Site {
    let id: Int

    init(id: Int) {
        self.id = id
        print("Site \(id): I've been created")
    }

    deinit {
        print("Site \(id): I've been destroyed!")
    }
}

for i in 1...3 {
    let site = Site(id: i)
    print("Site \(site.id): I'm in control!")
}
```

**What this shows**

- `deinit` runs the moment the last reference to an object goes away. No `func`, no parentheses, no arguments — and **classes only**, because structs are copied rather than shared and so have no single moment of death.
- Here `site` is scoped to one pass of the loop, so each object is created and destroyed before the next begins. Verified output:

```
Site 1: I've been created
Site 1: I'm in control!
Site 1: I've been destroyed!
Site 2: I've been created
...
```

The interleaving *is* the lesson: the `deinit` lands inside the loop, not in a batch at the end.

- Change what holds the reference and the timing changes completely:

```swift
var kept: [Site] = []
for i in 4...5 { kept.append(Site(id: i)) }
print("array holds \(kept.count)")
// Site 4: I've been created
// Site 5: I've been created
// array holds 2
// ...both deinits only fire when `kept` itself goes away
```

This is **ARC** (Automatic Reference Counting) in action: Swift counts how many strong references exist and deallocates at zero. It's not a garbage collector — it's deterministic, which is why you can predict exactly where those print lines land.

### Your notes — `let` on a class reference

```swift
class Singer {
    var name = "Adele"
}

let singer = Singer()
singer.name = "Justin"      // ✅ compiles, even though `singer` is a let
print(singer.name)          // Justin
```

> Classes don't need the `mutating` method

**Both observations are correct, and they're the same fact from two angles.**

- `let` on a class freezes the **reference**, not the object. You can't point `singer` at a *different* Singer, but you can change the one it points at all day.
- Because mutation doesn't change the reference, a class method that writes to a property changes nothing the compiler needs to track — so there's no `mutating` keyword for classes. In a struct, mutating a property genuinely mutates the value itself, which is why `mutating` exists there ([§21](#21-structs)).

The contrast, side by side:

| | `let s = SomeStruct()` | `let c = SomeClass()` |
|---|---|---|
| `s.prop = x` | ❌ compile error | ✅ allowed |
| `s = other` | ❌ compile error | ❌ compile error |
| `mutating` needed on methods | ✅ yes | ✗ no such keyword |

This is the single most common source of accidental shared-state bugs: a `let` gives you no protection whatsoever on a class.

### Going deeper

**`final` — close a class to subclassing.** It's both a design statement and a performance win, because the compiler can devirtualise the calls:

```swift
final class Analytics { }            // nobody may subclass
class Repo {
    final func save() { }            // subclasses may not override just this
}
```

Default to `final` and remove it when you actually need a subclass. It's the reverse of the Java habit.

**`static` vs `class` for type members.** In a class you get both, and the difference is overridability:

```swift
class Base {
    static func a() { print("static — cannot be overridden") }
    class  func b() { print("class — CAN be overridden") }
}
class Child: Base {
    // override static func a() { }        ❌ error: cannot override static method
    override class func b() { print("overridden") }
}
```

Structs only have `static`, since there's nothing to override.

**Designated vs convenience initialisers:**

```swift
class Employee {
    let hours: Int
    let name: String

    init(hours: Int, name: String) {       // designated — sets every property
        self.hours = hours
        self.name = name
    }

    convenience init(name: String) {       // convenience — must delegate sideways
        self.init(hours: 8, name: name)    // to another init on the SAME class
    }
}
```

Rules worth memorising: a designated init calls **up** (`super.init`), a convenience init calls **across** (`self.init`), and a convenience init can never call `super.init` directly.

**`required init`** forces every subclass to reimplement an initialiser — you'll meet it mostly as `required init?(coder:)` in UIKit.

**Failable initialisers** return an Optional instance:

```swift
class User {
    let name: String
    init?(name: String) {
        guard !name.isEmpty else { return nil }
        self.name = name
    }
}
User(name: "")      // nil
```

**⚠️ Retain cycles — the one way ARC leaks.** Two objects holding each other strongly can never reach zero references:

```swift
class Parent { var child: Child?  }
class Child  { var parent: Parent? }      // ❌ strong both ways = leak

class Child2 { weak var parent: Parent? } // ✅ weak breaks the cycle
```

- `weak` → always Optional, auto-nils when the target dies. Use it for back-references (parent, delegate) and in escaping closures.
- `unowned` → non-Optional, crashes if accessed after the target dies. Only when the lifetimes are provably tied.

`deinit` never firing is the symptom. A `print` in `deinit` — exactly what your `Site` class does — is the standard way to catch a leak.

**Casting up and down the hierarchy:**

```swift
let staff: [Employee] = [Developer(hours: 8), Employee(hours: 9)]

for person in staff {
    if let dev = person as? Developer { dev.work() }   // ✅ conditional downcast
    print(person is Developer)                         // type test
}

let up: Employee = dev          // upcast — always safe, implicit
let down = staff[0] as! Developer   // 💥 force downcast, crashes if wrong
```

**`AnyObject`** is the class-only escape hatch, and `: AnyObject` on a protocol restricts conformance to classes — which is what makes `weak var delegate: MyDelegate?` legal.

**When to actually reach for a class:**

| Need | Why a struct won't do |
|---|---|
| Shared mutable state (one source of truth) | structs copy |
| Identity — *this specific* object | structs have no `===` |
| `deinit` / cleanup at a known moment | structs aren't deallocated |
| Inheritance, `override`, dynamic dispatch | structs can't subclass |
| Interop with Objective-C / UIKit / `NSObject` | requires a class |

Everything else — models, view state, value objects, SwiftUI views — is a struct. And for shared mutable state in concurrent code, the modern answer is an **`actor`** rather than a class with locks:

```swift
actor Counter {
    private var value = 0
    func increment() { value += 1 }       // serialised automatically
}
await counter.increment()
```

---

## 23. Protocols

### Your notes

```swift
protocol Vehicle {
    var name: String { get }
    var currentPassengers: Int { get set }
    func estimateTime(for distance: Int) -> Int
    func travel(distance: Int)
}

struct Car: Vehicle {
    let name: String = "Car"
    var currentPassengers: Int = 1

    func estimateTime(for distance: Int) -> Int {
        distance / 50
    }

    func travel(distance: Int) {
        print("I'm driving \(distance) km")
    }

    func openSunroof() {
        print("It's a nice day!")
    }
}

func commute(distance: Int, using vehicle: Vehicle) {
    if vehicle.estimateTime(for: distance) > 100 {
        print("Too slow!")
    } else {
        vehicle.travel(distance: distance)
    }
}
```

> protocol seems to be the swift way to creating interfaces

### What this shows

- A protocol is a **contract with no implementation**. It lists what a conforming type must provide; it never says how. Fail to provide something and the compiler tells you exactly which requirement is missing.
- **`{ get }` vs `{ get set }`** is about what *callers through the protocol* may do, not about `let` vs `var`:
  - `var name: String { get }` — readable. A `let` constant satisfies this, which is why your `let name: String = "Car"` compiles. So does a computed `var name: String { "Car" }`.
  - `var currentPassengers: Int { get set }` — must be readable **and** writable, so it needs a real `var`. A `let` won't satisfy it.
  - Note both are declared `var` in the protocol even when a `let` will satisfy them — that's just protocol syntax.
- **Method requirements are signatures only** — no body, and the parameter labels are part of the requirement (`estimateTime(for:)` must keep the `for`).
- `func commute(distance: Int, using vehicle: Vehicle)` takes **any** conforming type. This is the payoff: `commute` works with a `Car`, a `Bicycle`, or a type you write next year, and never needs editing.
- **⚠️ `openSunroof()` is invisible through the protocol.** Inside `commute`, `vehicle` is a `Vehicle`, so only the four declared members exist. `vehicle.openSunroof()` fails to compile even when you pass a `Car`. The protocol is a narrower lens onto the type — you'd need `if let car = vehicle as? Car { car.openSunroof() }`.

### On "the Swift way to create interfaces"

Right, and then some. Protocols do everything a Java/C# interface does, plus four things interfaces can't:

1. **Structs and enums conform too**, not just classes. This is the big one — it's how Swift gets polymorphism without inheritance.
2. **Default implementations** via protocol extensions ([§24](#24-extensions)), so a protocol can ship behaviour, not just requirements.
3. **Retroactive conformance** — you can make a type you don't own conform to a protocol you do own (`extension Int: MyProtocol { }`).
4. **Associated types** — generic placeholders resolved by the conformer, which is how `Sequence`, `Collection` and `Identifiable` work.

That combination is why Swift is described as protocol-oriented rather than object-oriented: you compose small capabilities instead of inheriting from a base class.

### Going deeper

**Default implementations — a protocol extension gives conformers free behaviour:**

```swift
extension Vehicle {
    func travel(distance: Int) {                 // a default
        print("I'm travelling \(distance) km")
    }
    var description: String {                    // a bonus, not a requirement
        "\(name) carrying \(currentPassengers)"
    }
}

struct Bicycle: Vehicle {
    let name = "Bicycle"
    var currentPassengers = 1
    func estimateTime(for distance: Int) -> Int { distance / 10 }
    // travel(distance:) is inherited from the extension — no need to write it
}
```

This is the mechanism behind most of the standard library: `Collection` declares a handful of requirements, and the extension hands you `map`, `filter`, `first`, `isEmpty` and dozens more.

**⚠️ The dispatch trap — the most-missed protocol gotcha.** A method **in the protocol** dispatches dynamically; a method **only in the extension** dispatches statically. Verified:

```swift
protocol Greeter {
    func hello()                                  // IS a requirement
}
extension Greeter {
    func hello() { print("protocol hello") }
    func bonus() { print("protocol bonus") }      // NOT a requirement
}
struct S: Greeter {
    func hello() { print("S hello") }
    func bonus() { print("S bonus") }
}

let concrete = S()
let viaProtocol: Greeter = S()

concrete.hello()      // S hello
concrete.bonus()      // S bonus
viaProtocol.hello()   // S hello        ← requirement, so the override wins
viaProtocol.bonus()   // protocol bonus ← NOT a requirement, so the extension wins ⚠️
```

Same object, same method name, two different results depending on the static type of the variable. **Fix: if you intend conformers to be able to override it, declare it in the protocol body**, then use the extension only to supply the default.

**`mutating` requirements** — needed so value types can conform:

```swift
protocol Resettable {
    mutating func reset()
}
struct Counter: Resettable {
    var n = 5
    mutating func reset() { n = 0 }      // a class would just write `func reset()`
}
```

Leave `mutating` off the requirement and no struct can ever satisfy it.

**Protocol inheritance and composition:**

```swift
protocol Named { var name: String { get } }
protocol Aged  { var age: Int { get } }

protocol Person: Named, Aged { }              // inherits both sets of requirements

func greet(_ p: Named & Aged) { }              // composition — must satisfy both
func greet(_ p: some Named & Aged) { }         // same, generically
```

**`some` vs `any`** — the modern way to write your `commute` signature:

```swift
func commute(distance: Int, using vehicle: some Vehicle)   // generic: one concrete type
func commute(distance: Int, using vehicle: any Vehicle)    // existential: a box
func commute(distance: Int, using vehicle: Vehicle)        // your version — still legal
```

- `some Vehicle` — the caller picks a type, the compiler specialises, static dispatch, no boxing. **Prefer this** for parameters.
- `any Vehicle` — a runtime box that can hold any conformer. Needed for heterogeneous storage: `let fleet: [any Vehicle] = [Car(), Bicycle()]`.
- Bare `Vehicle` means the same as `any Vehicle`.

I checked your bare-`Vehicle` version against Swift 6.4 and it compiles with **no warning**, in both Swift 5 and Swift 6 language modes. The explicit spelling only becomes mandatory under an opt-in flag:

```
$ swiftc -swift-version 6 -enable-upcoming-feature ExistentialAny …
warning: use of protocol 'Vehicle' as a type must be written 'any Vehicle';
         this will be an error in a future Swift language mode [#ExistentialAny]
```

So nothing to change today — but writing `some` or `any` explicitly is the direction the language is heading, and it makes the performance difference visible at the call site.

**Class-only protocols** — required for `weak` delegate references:

```swift
protocol DataDelegate: AnyObject {
    func didLoad(_ data: Data)
}
class Controller {
    weak var delegate: DataDelegate?     // `weak` needs AnyObject
}
```

**Standard-library protocols worth conforming to** (most are synthesised — see [§21](#21-structs)):

| Protocol | Gives you | Cost |
|---|---|---|
| `Equatable` | `==`, `!=`, `contains` | free |
| `Hashable` | `Set`/dictionary keys | free |
| `Comparable` | `<`, `sorted()`, `min()` | you write `<` |
| `Codable` | JSON encode/decode | free |
| `CustomStringConvertible` | pretty `print` | you write `description` |
| `Identifiable` | SwiftUI `ForEach`/`List` | add an `id` |
| `CaseIterable` | `allCases` on an enum | free |
| `Sequence` / `IteratorProtocol` | `for … in` over your type | you write `next()` |
| `Error` | `throw` it | free (marker protocol) |

**Constrained extensions** — behaviour that only applies to *some* conformers:

```swift
extension Vehicle where Self: Codable {
    func save() throws -> Data { try JSONEncoder().encode(self) }
}

extension Collection where Element: Numeric {
    var total: Element { reduce(0, +) }
}
[1, 2, 3].total        // 6 — but ["a"].total doesn't exist
```

**Associated types** — a placeholder the conformer fills in:

```swift
protocol Container {
    associatedtype Item
    var count: Int { get }
    mutating func append(_ item: Item)
    subscript(i: Int) -> Item { get }
}

struct IntBox: Container {
    typealias Item = Int             // often inferred; you can usually omit this
    private var items: [Int] = []
    var count: Int { items.count }
    mutating func append(_ item: Int) { items.append(item) }
    subscript(i: Int) -> Int { items[i] }
}
```

A protocol with an associated type (or a `Self` requirement, like `Equatable`) can't always be used as a plain existential — that's the *"protocol can only be used as a generic constraint"* error you'll eventually meet. The answer is a generic function (`<T: Container>` or `some Container`) rather than `any Container`.

**Design guidance:** keep protocols small and capability-shaped. `Vehicle` with four members is a good size; a protocol with twenty members forces conformers to implement things they don't need. Swift's own naming hints at this — the `-able` suffix (`Equatable`, `Hashable`, `Codable`, `Identifiable`) describes one capability, not a whole category of object.

---

## 24. Extensions

### Your notes — extending a type you don't own

```swift
extension String {
    func trimmed() -> String {
        self.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    mutating func trim() {
        self = self.trimmed()
    }

    var lines: [String] {
        self.components(separatedBy: .newlines)
    }
}

var quote = "The truth is rarely pure and never simple    "
quote.trim()                     // quote is now trimmed in place

let lyrics = """
    But I keep cruising
    Can't stop, won't stop moving
    """

print(lyrics.lines.count)        // 2
```

### What this shows

- An extension adds members to an **existing type — including one you didn't write**. `String` lives in the standard library and you just gave it three new members, with no subclassing and no wrapper type.
- **`trimmed()` / `trim()` is textbook Swift naming, and worth naming explicitly:** when a non-mutating method returns a new value, name it with a **past participle** (`trimmed`, `sorted`, `reversed`); when the mutating twin acts in place, use the **imperative verb** (`trim`, `sort`, `reverse`). The standard library follows this everywhere, so your pair reads exactly like built-in API. If a past participle doesn't fit, the convention switches to an adjective: `union` / `formUnion`.
- **`mutating` works in an extension because `String` is a struct.** `self = self.trimmed()` — assigning wholesale to `self` is legal inside a `mutating` method on a value type, and it's the tidiest way to implement the in-place twin in terms of the pure one.
- `var lines: [String]` is a **computed** property. Extensions can add computed properties freely; they cannot add stored ones (see below).
- `quote` must be a `var` for `quote.trim()` to compile — same `mutating` rule as [§21](#21-structs).
- `lines.count` is **2** (verified): the multi-line string's closing `"""` is indented to match the content, so the leading four spaces are stripped from both lines and there's no trailing empty line.

**Small style note:** the `self.` prefixes are all optional here — `trimmingCharacters(in:)` and `components(separatedBy:)` resolve to `self` on their own. Idiomatic Swift omits `self.` unless it's needed to disambiguate from a parameter or to capture in a closure.

### Your notes — extending a protocol

```swift
extension Collection {
    var isNotEmpty: Bool {
        isEmpty == false
    }
}

let guests = ["Mario", "Luigi", "Peach"]

if guests.isNotEmpty {
    print("Guest count: \(guests.count)")
}
```

> We can extend collections to and all the sub classes of the collections will get the function as well.

**Right idea, one term to swap: *conformers*, not subclasses.** `Collection` is a protocol, not a base class, so nothing subclasses it — types *conform* to it. That distinction is what makes this so much more powerful than class inheritance would be: conformance is opt-in, retroactive, and available to structs and enums. Verified, all of these pick up `isNotEmpty` from that one extension:

```swift
"abc".isNotEmpty            // true — String is a Collection
[1, 2].isNotEmpty           // true — Array
["a": 1].isNotEmpty         // true — Dictionary
Set([1]).isNotEmpty         // true — Set
(1..<5).isNotEmpty          // true — Range
[1,2,3].dropFirst().isNotEmpty   // true — ArraySlice
```

This is **protocol extension as default implementation** ([§23](#23-protocols)) — one definition, every conforming type in the language and in your own code.

Two notes on the body:

- `isEmpty == false` works, but `!isEmpty` is the idiomatic spelling (see the style appendix). Both compile to the same thing.
- Because `isNotEmpty` is declared *only* in the extension and not as a protocol requirement, it's statically dispatched — no conformer can override it. That's fine and even desirable here, but it's the same mechanism as the dispatch trap in [§23](#23-protocols), so it's worth recognising.

### Going deeper

**What an extension can and cannot add:**

| ✅ Can add | ❌ Cannot add |
|---|---|
| Computed properties (instance & static) | **Stored** properties |
| Methods, including `mutating` | Property observers (`willSet`/`didSet`) |
| Initialisers (convenience only, for classes) | `deinit` |
| Subscripts | An `override` of an existing method |
| Nested types | A designated initialiser on a class |
| Protocol conformances | New cases on an enum |

The stored-property restriction is the one that bites. An extension can't change a type's memory layout, so there's nowhere to put the storage:

```swift
extension String {
    // var cachedLines: [String] = []       ❌ extensions must not contain stored properties
    var lines: [String] { components(separatedBy: .newlines) }   // ✅ recompute instead
}
```

**Adding an initialiser — and the struct trick from [§21](#21-structs):**

```swift
extension Player {
    init(_ name: String) { self.init(name: name, score: 0) }
}
// the free memberwise init survives, because the custom one lives in an extension
```

**Constrained extensions** — add members only where they make sense:

```swift
extension Array where Element: Numeric {
    var total: Element { reduce(0, +) }
}
[1, 2, 3].total          // 6
// ["a", "b"].total      ❌ doesn't exist for non-numeric elements

extension Collection where Element: Equatable {
    func countOccurrences(of value: Element) -> Int {
        filter { $0 == value }.count
    }
}

extension Optional where Wrapped == String {
    var orEmpty: String { self ?? "" }       // very handy in UI code
}
```

`where Self: …` is the protocol-extension equivalent — see [§23](#23-protocols).

**Extensions for organising conformances.** A widely used convention: keep the type's own members in the main declaration, and give each protocol its own extension:

```swift
struct Album {
    let title: String
    let artist: String
}

extension Album: Equatable {
    static func == (l: Album, r: Album) -> Bool { l.title == r.title }
}

extension Album: Comparable {
    static func < (l: Album, r: Album) -> Bool { l.title < r.title }
}

extension Album: CustomStringConvertible {
    var description: String { "\(title) by \(artist)" }
}
```

This keeps each conformance's requirements visibly grouped, and the compiler reports a missing requirement against the right extension.

**⚠️ `components(separatedBy:)` vs `split(separator:)` — they disagree on empty lines.** Your `lines` uses `components`, and that's usually the right choice for text, but know the difference (verified):

```swift
let text = "a\n\nb"
text.components(separatedBy: .newlines)   // ["a", "", "b"]   keeps the blank
text.split(separator: "\n")               // ["a", "b"]       drops it
text.split(separator: "\n", omittingEmptySubsequences: false)   // ["a", "", "b"]
```

Also: `components(separatedBy:)` is Foundation and returns `[String]`; `split` is the standard library and returns `[Substring]` — cheaper, but see the `Substring` warning in [§2](#2-strings). For counting lines in a document, `components` (or `text.lines` on iOS 16+) is what you want, because a blank line is still a line.

**Useful extensions worth having in every project:**

```swift
extension String {
    var isBlank: Bool { trimmingCharacters(in: .whitespacesAndNewlines).isEmpty }
    func truncated(to n: Int) -> String {
        count <= n ? self : prefix(n) + "…"
    }
}

extension Collection {
    subscript(safe i: Index) -> Element? {          // from §6 — no more index crashes
        indices.contains(i) ? self[i] : nil
    }
}

extension Array where Element: Hashable {
    func uniqued() -> [Element] {                   // dedupe, order preserved
        var seen = Set<Element>()
        return filter { seen.insert($0).inserted }
    }
}

extension Int {
    var isEven: Bool { isMultiple(of: 2) }
}
```

**Retroactive conformance — powerful, and mildly discouraged.** You can make a type you don't own conform to a protocol you don't own:

```swift
extension Int: MyProtocol { }        // ✅ your protocol, fine
extension Date: Identifiable { … }   // ⚠️ neither the type nor the protocol is yours
```

That second form draws a warning in Swift 6 — verified text:

```
warning: extension declares a conformance of imported type 'Date' to imported
         protocol 'Identifiable'; this will not behave correctly if the owners of
         'Foundation' introduce this conformance in the future
note: add '@retroactive' to silence this warning
```

If the framework later adds the same conformance, the two collide. Either spell it `extension Date: @retroactive Identifiable` to accept that risk knowingly, or wrap the type in one of your own.

**Extensions cannot override.** For a class, an extension adds; it never replaces:

```swift
class Base { func f() { print("base") } }
extension Base { override func f() { } }
// ❌ error: invalid redeclaration of 'f()'
// ❌ error: method does not override any method from its superclass
```

Note the second error is a little misleading — the real rule is that an extension cannot replace an existing member, so Swift sees a duplicate declaration. Subclass if you need to override.

**Access control follows the extension**, which is a tidy way to keep helpers private:

```swift
private extension String {
    var slug: String { lowercased().replacingOccurrences(of: " ", with: "-") }
}
// `slug` is visible only in this file
```

**When *not* to extend.** Extensions are global — an `extension String` is visible to your whole module, so a vaguely named helper pollutes autocomplete for everyone. Keep the name specific, keep it `private` or `fileprivate` when it's local to one file, and prefer a free function or a dedicated type when the behaviour isn't really *about* the type you're extending.

---

## 25. Optionals

An Optional is a box that either holds a value or is empty. `String?` is really `Optional<String>` — an enum with two cases, `.some(Wrapped)` and `.none`. Only an Optional may be `nil`:

```swift
var name: String? = "Varun"
name = nil                    // ✅ legal
var other: String = nil       // ❌ 'nil' cannot initialize a non-optional type
```

Everything below is one of the ways to get the value back out.

### Your notes — `if let`

```swift
let opposites = [
    "Mario": "Wario",
    "Luigi": "Waluigi"
]

let peachOpposite = opposites["Peach"]        // nil — no such key

if let marioOpposite = opposites["Mario"] {
    print("Mario's opposite is \(marioOpposite)")
}
```

**What this shows**

- A dictionary subscript **always** returns an Optional, because the key may be absent. `peachOpposite` is `String?` holding `nil`; no crash, unlike an out-of-range array index ([§6](#6-arrays)).
- `if let` does two things at once: tests for a value, and binds the **unwrapped** value to a new constant for the body. Inside the braces `marioOpposite` is a plain `String` — no `!`, no further checks.
- The binding is scoped to the `if` body. Outside it, only the Optional exists.
- `peachOpposite` is never read, so you'll see *"initialization of immutable value 'peachOpposite' was never used"*. That's the compiler noting the demo value, not a problem with the code.

**Modern shorthand (Swift 5.7+)** — when you'd reuse the same name, drop the `= name` entirely:

```swift
if let marioOpposite = opposites["Mario"] { }   // classic
let mario = opposites["Mario"]
if let mario { }                                // shorthand: same name, unwrapped
```

Shadowing like this is idiomatic — inside the body the Optional version is simply no longer in scope, so you can't accidentally use it.

**Multiple bindings and extra conditions chain with commas:**

```swift
if let mario = opposites["Mario"],
   let luigi = opposites["Luigi"],
   mario != luigi {
    print("\(mario) and \(luigi)")
}
```

Each binding can use the ones before it, and any plain `Bool` condition can join the chain.

### Your notes — `guard let`

```swift
func printSquare(of number: Int?) {
    guard let number = number else {
        print("Missing input")
        return
    }

    print("\(number) x \(number) is \(number * number)")
}
```

**What this shows**

- `guard let` is the **early-exit** form: handle the absent case first, then carry on with the unwrapped value for the **rest of the function**. Note where `number` is usable — not inside a nested block, but at the function's top level from the `guard` onward.
- The `else` block **must leave the current scope** — `return`, `throw`, `break`, `continue`, or `fatalError()`. Fall off the end and you get *"'guard' body must not fall through, consider using a 'return' or 'throw' to exit the scope"*.
- `guard let number = number` can be written `guard let number` with the same 5.7 shorthand.

**`if let` vs `guard let` — the choice is about shape, not capability:**

```swift
// if let nests: each precondition costs an indent level
func a(_ x: Int?, _ y: Int?) {
    if let x {
        if let y {
            print(x + y)        // the real work, buried two levels deep
        }
    }
}

// guard let flattens: preconditions at the top, work at one indent
func b(_ x: Int?, _ y: Int?) {
    guard let x, let y else { return }
    print(x + y)
}
```

Use `guard` for "this shouldn't happen — bail out", and `if let` when both branches are normal outcomes and you want to do something in each.

### Your notes — nil coalescing `??`

```swift
let tvShows = ["Archer", "Babylon 5", "Ted Lasso"]
let favourite = tvShows.randomElement() ?? "None"

let input = ""
let number = Int(input) ?? 0
print(number)                    // 0
```

**What this shows**

- `??` unwraps the left side, or evaluates the right side if it's `nil`. The **result is non-optional** — that's the whole point.
- `randomElement()` returns an Optional because the array might be empty. Here it never is, so `"None"` is unreachable — but the compiler can't know that, and `??` is how you satisfy it without a `!`.
- `Int("")` is `nil`, so `number` is `0`. Verified. This is the correct instinct for any string→number conversion: **`Int(userInput)` is always an Optional**, because users type anything.
- `??` is lazy on the right — `Int(input) ?? expensiveDefault()` only calls the function when needed.

**It chains, right-associatively, and works with `try?`:**

```swift
let value = primary ?? secondary ?? "last resort"
let strength = (try? checkPassword(pw)) ?? "unknown"
let count = dict["k"] ?? 0
```

**⚠️ `??` and precedence** — it binds looser than arithmetic, so parenthesise when mixing:

```swift
let total = (count ?? 0) + 1      // ✅ clear and correct
```

### Your notes — optional chaining

```swift
let names = ["Arya", "Bran", "Robb", "Sansa"]
let chosen = names.randomElement()?.uppercased()
print("Next in line: \(chosen ?? "No one")")
```

> optional will still be using the function call made on it

**That's optional chaining, and your description is the right intuition — here's the precise rule.**

- `?.` means *"if there's a value, call this on it; if it's `nil`, stop and produce `nil`"*. The method call is **skipped entirely** when the Optional is empty — nothing crashes, nothing runs.
- **The whole expression becomes Optional**, even though `uppercased()` returns a plain `String`. Verified: `type(of: chosen)` is `Optional<String>`. That's why the `?? "No one"` at the end is needed to print it cleanly.
- With an empty array the chain short-circuits, verified:

```swift
let empty: [String] = []
empty.randomElement()?.uppercased()      // nil — uppercased() never ran
```

**Chains can be arbitrarily long, and one `nil` anywhere yields `nil`:**

```swift
let city = user?.address?.city?.uppercased()     // String?  — any link may be nil
user?.save()                                     // a no-op if user is nil
let n = user?.friends?.count ?? 0                 // Int
let first = dict["key"]?.first?.uppercased()
```

You never need more than one `?` per link, and you never need `!` in between.

**Assigning through a chain** works too, and silently does nothing if the chain is `nil`:

```swift
user?.name = "Varun"          // no effect at all when user == nil
```

That silence is occasionally a bug — if the write mattering is important, use `guard let` instead.

**Interpolating an Optional directly is the cosmetic trap** ([§5](#5-string-interpolation)):

```swift
print("Next in line: \(chosen)")             // "Optional("BRAN")" ⚠️ and it warns
print("Next in line: \(chosen ?? "No one")") // ✅ what you wrote
```

### Your notes — `try?`

```swift
enum UserError: Error {
    case badID, networkFailed
}

func getUser(id: Int) throws -> String {
    throw UserError.networkFailed
}

if let user = try? getUser(id: 23) {
    print("User: \(user)")
}
```

**What this shows**

- `try?` converts a **throwing call into an Optional**: the value on success, `nil` on any error. It's the bridge between the two failure systems in Swift ([§19](#19-error-handling)).
- That makes `try?` compose with everything in this section — here with `if let`, so the success branch gets a plain `String`.
- This function always throws, so the body never prints. Verified.
- **The trade-off: `try?` discards *why* it failed.** `badID` and `networkFailed` become the same `nil`. That's fine when the caller genuinely doesn't care, and wrong when the user needs a message — use `do`/`catch` then.

**The three `try` flavours side by side:**

```swift
let a = try  getUser(id: 1)     // String  — propagates; needs `throws` or do/catch
let b = try? getUser(id: 1)     // String? — nil on error, reason discarded
let c = try! getUser(id: 1)     // String  — 💥 crashes on error
```

**`try?` with `??` for a one-liner default, and with `guard`:**

```swift
let user = (try? getUser(id: 23)) ?? "Guest"

guard let user = try? getUser(id: 23) else { return }
```

**⚠️ `try?` on a function that already returns an Optional flattens the two layers** — and that costs you information. Verified:

```swift
func find(id: Int) throws -> String? { nil }

let x = try? find(id: 1)     // String?, NOT String?? — Swift 5 flattens it
type(of: x)                  // Optional<String>
```

Since Swift 5, `try?` collapses the nesting, so a `nil` result is ambiguous: **it could mean the call threw, or that it returned `nil` successfully.** Both produce the same `nil`. When that distinction matters, don't use `try?`:

```swift
do {
    if let user = try find(id: 1) { print(user) }   // found
    else { print("no such user") }                  // genuinely absent
} catch {
    print("lookup failed: \(error)")               // threw — a different thing
}
```

### Going deeper

**Where Optionals come from** — recognising these saves a lot of confusion:

| Source | Why |
|---|---|
| `dict[key]` | key may be absent |
| `array.first` / `.last` / `.min()` / `.max()` | array may be empty |
| `array.randomElement()` | array may be empty |
| `array.firstIndex(of:)` | may not be found |
| `Int("abc")`, `Double(str)`, `URL(string:)` | conversion may fail |
| `MyEnum(rawValue:)` | no case matches |
| `try?` | the call may have thrown |
| `weak var` | the target may have been deallocated |
| `init?` (failable initialisers) | construction may fail |

**Transforming without unwrapping — `map` and `flatMap` on Optionals:**

```swift
let age: Int? = 26
age.map { $0 * 2 }                       // Optional(52) — stays nil if age was nil
let str: String? = "42"
str.flatMap { Int($0) }                  // Optional(42) — flatMap avoids Int??
str.map { Int($0) }                       // Int?? — the nested case flatMap prevents
```

`?.` is really sugar over this: `chosen = names.randomElement().map { $0.uppercased() }` is the same thing.

**Optionals in a `switch`:**

```swift
switch opposites["Mario"] {
case .some(let name): print(name)
case .none:           print("nothing")
}

// with the sugar:
switch opposites["Mario"] {
case let name?: print(name)
case nil:       print("nothing")
}
```

**Collections of Optionals — `compactMap` is the workhorse:**

```swift
let raw: [String?] = ["a", nil, "b"]
raw.compactMap { $0 }                    // ["a", "b"]  — drops nil AND unwraps
["1", "x", "3"].compactMap { Int($0) }   // [1, 3]
dict.compactMapValues { $0 }             // same idea for dictionary values
```

**On force-unwrapping (`!`).** It isn't forbidden — it's a *claim*: "I have proved this is never `nil`, and I accept a crash if I'm wrong."

```swift
URL(string: "https://apple.com")!        // ✅ a hard-coded, known-good literal
UIImage(named: "logo")!                  // ✅ an asset you ship
Int(userTypedText)!                      // ❌ never — users type anything
json["name"] as! String                  // ❌ never — servers change
```

A useful middle ground when a `nil` really is a programming error, because it documents the assumption:

```swift
guard let url = URL(string: urlString) else {
    preconditionFailure("Malformed URL literal: \(urlString)")
}
```

**Implicitly unwrapped optionals (`String!`)** exist mainly for Objective-C interop and `@IBOutlet`. They behave like `String?` but force-unwrap on every access, so they crash silently at a distance. Don't introduce new ones.

**⚠️ Don't stack two representations of "nothing."** These are bug factories:

```swift
var tags: [String]? = nil       // ❌ is nil different from []? almost never
var tags: [String] = []         // ✅ one representation

var note: String? = ""          // ❌ nil vs "" — which means "no note"?
```

Pick one and make the type say it. The exception is a genuine three-state case — for example a PATCH request where `nil` means *"don't change this field"* and `""` means *"clear it"*.

**Comparison quirks:**

```swift
let a: Int? = nil
a == nil                 // true — Optional is Equatable when Wrapped is
a == 5                   // false, no unwrapping needed
// a < 5                 ❌ Optionals aren't Comparable
[3, nil, 1].compactMap { $0 }.sorted()   // unwrap first, then sort
```

**`Optional` is just an enum**, which is worth internalising — it's why pattern matching, `map`, and the `.some`/`.none` cases all work the way they do. Nothing about Optionals is special-cased in the language except the `?` sugar and the `!`/`?.` operators.

---

## Appendix — Style notes on your code

Nothing here is a bug — these are the conventions that will make your code look like everyone else's Swift, which matters more than it sounds when you're reading other people's projects.

**1. Drop the semicolons.** Swift doesn't use statement terminators. They compile fine, but no Swift codebase writes them, and Xcode won't insert them:

```swift
let score = 10;      // works, but
let score = 10       // ✅ idiomatic
```

The one legitimate use is two statements on one line: `var a = 1; a += 1` — and you shouldn't do that either.

**2. `if` conditions don't need parentheses:**

```swift
if (files[i].hasSuffix(".jpeg")) { }    // C habit
if files[i].hasSuffix(".jpeg") { }      // ✅
```

**3. `let` over `var`, always, until the compiler complains.** Xcode actively warns *"variable was never mutated; consider changing to let"*. Every `let` is a fact the compiler can rely on.

**4. Name booleans with a verb.** `isReleased`, `hasPrefix`, `canVote`, `shouldSave`. Your `isSaved`/`isEnabled`/`goodDog` are good; `gameOver` reads better as `isGameOver`.

**5. Property names shouldn't repeat their type.** In `struct Person { var person: String }`, the property is really a *name*:

```swift
struct Person { var name: String }      // ✅
```

**6. Types are `UpperCamelCase`, everything else is `lowerCamelCase`.** Enum *cases* are lowerCamelCase too (`case monday`, not `case Monday`) — your enums follow this correctly.

**7. Use `_` for values you deliberately ignore.** This kills the "unused" warnings in today's notes:

```swift
_ = numbers.contains(11)
_ = try checkPassword("12345")
for _ in 1...3 { }
```

**8. Prefer the sugar.** `[String]` over `Array<String>`, `[String: Int]` over `Dictionary<String, Int>`, `.friday` over `Weekday.friday` once the type is known.

**9. One blank line between members, no blank line after `{`.** And a space after the colon in an annotation (`var x: Int`, not `var x : Int` — your `var isEnabled : Bool` has the extra space).

---

## Where to go next

Classes, protocols, extensions and optionals are now covered above. What builds directly on them, roughly in order of usefulness:

- **Generics** — `<T>`, constraints (`where T: Comparable`), associated types. You've met the consumer side (`[String]`, `Optional<Wrapped>`, `some Vehicle`); writing your own is the next step.
- **`Codable` in earnest** — `CodingKeys`, nested containers, custom `init(from:)`, dates and snake_case. Free on most structs ([§21](#21-structs)), fiddly the moment the JSON doesn't match your model.
- **ARC in depth** — `weak` vs `unowned`, retain cycles in closures, `deinit` as a leak detector. Sketched in [§22](#22-classes--inheritance); worth a focused pass once you have a real app holding references.
- **Collections beyond `Array`** — `Sequence`/`Collection` conformance for your own types, `lazy`, `AnyIterator`.
- **`async`/`await`, `Task`, `actor`** — the modern concurrency model, and the reason `static var` and shared classes get flagged in Swift 6.
- **Result builders & SwiftUI** — where nearly everything in this file (structs, enums, closures, trailing closures, protocols, `some`, property wrappers) shows up at once.
- **Property wrappers** — `@State`, `@Published`, `@AppStorage`. Built on the computed-property and `get`/`set` machinery from [§21](#21-structs).
