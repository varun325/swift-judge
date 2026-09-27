import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
B = 'LanguageGuide/TheBasics'; BO='LanguageGuide/BasicOperators'; SC='LanguageGuide/StringsAndCharacters'; CS='LanguageGuide/ClassesAndStructures'
P = []
# ---------- Value types & basics (notes §1, §10)
P.append(dict(id='predict-array-copy', title='Predict: Copying an Array', topic='Value types', mode='predict', notes='1',
 concepts=['value-vs-reference','collection-types'], docs=[('Structures and Classes — value types', CS)],
 statement="""Type the **exact output** of this program (naukri Q63 in disguise). The judge compiles and runs it with `swiftc` and compares line by line.""",
 snippet="""
 var arr1 = ["a", "b", "c"]
 var arr2 = arr1
 arr2.append("d")
 print(arr1.count, arr2.count)
 print(arr1)
 """,
 explain="""`Array` is a **value type**: `var arr2 = arr1` gives an independent copy (copy-on-write makes it cheap until one side mutates), so appending to `arr2` leaves `arr1` alone. `print` of an array uses `debugDescription` for elements — hence the quotes."""))
P.append(dict(id='predict-struct-vs-class', title='Predict: Struct Copy vs Class Share', topic='Value types', mode='predict', notes='1',
 concepts=['value-vs-reference','struct-vs-class'], docs=[('Structures and Classes', CS)],
 statement="Predict the output. One of these types is a value type, the other a reference type.",
 snippet="""
 struct PointS { var x = 0 }
 final class PointC { var x = 0 }

 var a = PointS()
 var b = a
 b.x = 10

 let c = PointC()
 let d = c
 d.x = 10

 print(a.x, b.x)
 print(c.x, d.x)
 print(c === d)
 """,
 explain="""Assigning a **struct** copies it — `a` and `b` are independent. Assigning a **class** reference copies the *pointer* — `c` and `d` name the same object, which `===` confirms. Note `let d` still allows `d.x = 10`: `let` freezes the reference, not the object."""))
P.append(dict(id='swap-values', title='Swap Two Values with inout', topic='Value types', notes='1', diff='easy',
 concepts=['inout','value-vs-reference'], docs=[('Functions — In-Out Parameters', 'LanguageGuide/Functions')],
 sig='func swapPair(_ pair: inout [Int])',
 statement="""`pair` always has exactly two elements. Swap them **in place** — the judge passes the array as `inout` and reports what it looks like afterwards.

 Try it without the standard library's `swap` or `swapAt` first, using a temporary `let`. Then notice what `(a, b) = (b, a)` tuple assignment gives you.""",
 solution="""
 func swapPair(_ pair: inout [Int]) {
     let temp = pair[0]
     pair[0] = pair[1]
     pair[1] = temp
 }
 """,
 explain="""An `inout` parameter is copied in, mutated, and written back when the function returns (copy-in copy-out). Idiomatic alternatives: `pair.swapAt(0, 1)` or `(pair[0], pair[1]) = (pair[1], pair[0])`.""",
 tests=[({'pair':[1,2]},[2,1]), {'pair':[5,5]}, {'pair':[-1,99]}, {'pair':[0,-7]}]))
P.append(dict(id='runtime-constant', title='Constants Decided at Runtime', topic='Constants & variables', notes='10',
 concepts=['let-vs-var','runtime-constants'], docs=[('The Basics — Constants and Variables', B)],
 sig='func shippingCost(weightKg: Double, express: Bool) -> Double',
 statement="""Compute a shipping cost using a **`let` constant that is assigned in each branch** of an `if` — not a `var`.

 - base rate: `5.0` for express, `2.5` otherwise
 - cost = base rate × weight, but never less than `10.0`

 ```swift
 shippingCost(weightKg: 2, express: false)  // 10.0 (2.5*2 = 5 → minimum 10)
 shippingCost(weightKg: 4, express: true)   // 20.0
 ```""",
 solution="""
 func shippingCost(weightKg: Double, express: Bool) -> Double {
     let rate: Double
     if express {
         rate = 5.0
     } else {
         rate = 2.5
     }
     return max(10.0, rate * weightKg)
 }
 """,
 explain="""A `let` only needs to be assigned **exactly once before use** — the compiler's definite-initialisation analysis checks every path. In Swift 5.9+ you can also write `let rate = express ? 5.0 : 2.5` or `let rate = if express { 5.0 } else { 2.5 }`.""",
 tests=[({'weightKg':2,'express':False},10.0), ({'weightKg':4,'express':True},20.0), {'weightKg':0,'express':True}, {'weightKg':10,'express':False}, {'weightKg':1.5,'express':True}, {'weightKg':100,'express':True}]))
P.append(dict(id='diag-let-reassign', title='Diagnostic: Reassigning a let', topic='Constants & variables', mode='diagnostic', notes='10',
 concepts=['let-vs-var'], docs=[('The Basics — Constants and Variables', B)],
 statement="""Write a program that declares `let maxLoginAttempts = 3` and then tries to change it to `5`. You pass when the compiler **refuses**.

 Read the exact error text in the results panel — you'll see it a lot.""",
 starter="let maxLoginAttempts = 3\n",
 solution="let maxLoginAttempts = 3\nmaxLoginAttempts = 5\n",
 explain="""`cannot assign to value: 'maxLoginAttempts' is a 'let' constant`. The fix-it suggests changing `let` to `var` — but ask first whether the value *should* change.""",
 tests=[{'name':'Reassignment rejected','pattern':"cannot assign to value: 'maxLoginAttempts' is a 'let' constant"}]))
P.append(dict(id='type-inference-describe', title='Name That Inferred Type', topic='Type inference', notes='10', diff='easy',
 concepts=['type-inference','fundamental-types'], docs=[('The Basics — Type Safety and Type Inference', B)],
 sig='func inferredTypes() -> [String]',
 statement="""Return the names of the types Swift infers for these literals, **in order**, by writing `String(describing: type(of: …))` for each:

 ```swift
 42          3.0          "hi"          true
 [1, 2]      ["a": 1]     (1, "x")      1...3
 ```

 The expected answer is what the real compiler infers — write it with `type(of:)` rather than guessing strings.""",
 solution="""
 func inferredTypes() -> [String] {
     [
         String(describing: type(of: 42)),
         String(describing: type(of: 3.0)),
         String(describing: type(of: "hi")),
         String(describing: type(of: true)),
         String(describing: type(of: [1, 2])),
         String(describing: type(of: ["a": 1])),
         String(describing: type(of: (1, "x"))),
         String(describing: type(of: 1...3)),
     ]
 }
 """,
 explain="""Integer literals default to `Int`, float literals to `Double`, and collection literals are inferred from their elements (`Array<Int>`, `Dictionary<String, Int>`). `1...3` is a `ClosedRange<Int>`. Look at your output: `type(of:)` prints the *full* generic names — `[Int]` is sugar for `Array<Int>`.""",
 tests=[{}], hidden=0))
P.append(dict(id='numeric-literals', title='Binary, Octal and Hex Literals', topic='Numbers', notes='3', diff='easy',
 concepts=['numeric-literals'], docs=[('The Basics — Numeric Literals', B)],
 sig='func literalValues() -> [Int]',
 statement="""Return an array containing the decimal value **17** written four ways — decimal, binary, octal and hexadecimal literals — followed by `1_000_000` written with underscores.

 ```swift
 literalValues()  // [17, 17, 17, 17, 1000000]
 ```""",
 starter="func literalValues() -> [Int] {\n    // write each value with a different literal prefix: 0b, 0o, 0x\n    return []\n}\n",
 solution="func literalValues() -> [Int] {\n    [17, 0b10001, 0o21, 0x11, 1_000_000]\n}\n",
 explain="""Prefixes: `0b` binary, `0o` octal, `0x` hex. Underscores are ignored and exist purely for readability. They're all the same `Int` value — the literal form only changes how *you* write it.""",
 tests=[({},[17,17,17,17,1000000])], hidden=0))
P.append(dict(id='to-binary-string', title='Format an Int in Any Base', topic='Numbers', notes='3', diff='easy',
 concepts=['numeric-literals','fundamental-types'], docs=[('The Basics — Integers', B)],
 sig='func format(_ value: Int, radix: Int) -> String',
 statement="""Return `value` written in the given `radix` (2…36), using lowercase letters for digits above 9, with a leading `-` for negatives. Hint: `String` has an initialiser for exactly this.

 ```swift
 format(255, radix: 16)  // "ff"
 format(5, radix: 2)     // "101"
 format(-8, radix: 8)    // "-10"
 ```""",
 solution="func format(_ value: Int, radix: Int) -> String {\n    String(value, radix: radix)\n}\n",
 explain="""`String(_:radix:uppercase:)` formats any `BinaryInteger`; the reverse is the failable `Int(_:radix:)`, which returns `nil` for invalid digits.""",
 tests=[({'value':255,'radix':16},'ff'), {'value':5,'radix':2}, {'value':-8,'radix':8}, {'value':0,'radix':2}, {'value':35,'radix':36}, {'value':1024,'radix':2}]))
P.append(dict(id='overflow-safe-add', title='Detect Integer Overflow', topic='Numbers', notes='3', diff='medium',
 concepts=['integer-overflow'], docs=[('Advanced Operators — Overflow Operators','LanguageGuide/AdvancedOperators')],
 sig='func safeAdd(_ a: Int, _ b: Int) -> Int?',
 statement="""Plain `a + b` **crashes** on overflow. Return the sum, or `nil` if it would overflow `Int`.

 ```swift
 safeAdd(2, 3)            // 5
 safeAdd(Int.max, 1)      // nil
 safeAdd(Int.min, -1)     // nil
 ```""",
 solution="""
 func safeAdd(_ a: Int, _ b: Int) -> Int? {
     let (sum, overflow) = a.addingReportingOverflow(b)
     return overflow ? nil : sum
 }
 """,
 explain="""`addingReportingOverflow(_:)` returns a tuple `(partialValue, overflow)`. `&+` would silently wrap instead — useful for hashing, dangerous for money.""",
 tests=[({'a':2,'b':3},5), ({'a':9223372036854775807,'b':1},None), {'a':-9223372036854775808,'b':-1}, {'a':-5,'b':5}, {'a':9223372036854775806,'b':1}, {'a':-9223372036854775807,'b':-1}]))
P.append(dict(id='wrapping-hash', title='Wrapping Arithmetic Hash', topic='Numbers', notes='3', diff='medium',
 concepts=['integer-overflow','operator-overloading'], docs=[('Advanced Operators — Overflow Operators','LanguageGuide/AdvancedOperators')],
 sig='func djb2(_ text: String) -> Int',
 statement="""Implement the classic djb2 string hash over the string's **UTF-8 bytes**: start with `5381`, then for each byte `hash = hash * 33 + byte`. The multiplication will overflow for longer strings — use the **wrapping** operators so it wraps around instead of crashing.

 ```swift
 djb2("")    // 5381
 djb2("a")   // 177670
 ```""",
 solution="""
 func djb2(_ text: String) -> Int {
     var hash = 5381
     for byte in text.utf8 {
         hash = hash &* 33 &+ Int(byte)
     }
     return hash
 }
 """,
 explain="""`&*` and `&+` wrap on overflow (two's complement), which is exactly what hash functions want. Without the `&`, the long test cases trap with *Arithmetic overflow*. `text.utf8` is a zero-copy view of the bytes.""",
 tests=[('',5381), 'a', 'hello', 'The quick brown fox jumps over the lazy dog', 'swift'*40, '🦅✨'], ))
P[-1]['tests'] = [({'text':t[0]},t[1]) if isinstance(t,tuple) else {'text':t} for t in P[-1]['tests']]
P.append(dict(id='float-compare', title='Comparing Doubles Safely', topic='Numbers', notes='3', diff='easy',
 concepts=['float-vs-double'], docs=[('The Basics — Floating-Point Numbers', B)],
 sig='func nearlyEqual(_ a: Double, _ b: Double) -> Bool',
 statement="""`0.1 + 0.2 == 0.3` is **false** in binary floating point. Return `true` when `|a - b| <= 1e-9 * max(1, |a|, |b|)`.""",
 solution="""
 func nearlyEqual(_ a: Double, _ b: Double) -> Bool {
     abs(a - b) <= 1e-9 * max(1, abs(a), abs(b))
 }
 """,
 explain="""A relative tolerance scales with the magnitude of the numbers; a fixed `1e-9` alone fails for huge values. `Double` has ~15–16 significant digits, `Float` only ~7.""",
 tests=[({'a':0.30000000000000004,'b':0.3},True), ({'a':1.0,'b':1.1},False), {'a':1e12,'b':1e12+0.0001}, {'a':0,'b':1e-10}, {'a':-2.5,'b':-2.5}, {'a':100,'b':100.001}]))
P.append(dict(id='digit-sum', title='Sum of Digits', topic='Numbers', notes='3', diff='easy',
 concepts=['fundamental-types','map-filter-reduce'], docs=[('Basic Operators — Remainder Operator', BO)],
 sig='func digitSum(_ n: Int) -> Int',
 statement="""Return the sum of the decimal digits of `n` (ignore the sign).

 ```swift
 digitSum(1234)  // 10
 digitSum(-907)  // 16
 ```""",
 solution="""
 func digitSum(_ n: Int) -> Int {
     var x = n.magnitude
     var total: UInt = 0
     while x > 0 {
         total += x % 10
         x /= 10
     }
     return Int(total)
 }
 """,
 explain="""`%` and `/` peel digits off the end. `magnitude` (a `UInt`) handles `Int.min`, whose absolute value doesn't fit in `Int` — `abs(Int.min)` would trap. A string approach works too: `String(n).compactMap(\\.wholeNumberValue).reduce(0, +)`.""",
 tests=[({'n':1234},10), ({'n':-907},16), {'n':0}, {'n':9}, {'n':-9223372036854775808}, {'n':1000000001}]))
P.append(dict(id='fahrenheit', title='Temperature Conversion', topic='Numbers', notes='3', diff='easy',
 concepts=['float-vs-double','type-inference'], docs=[('The Basics — Numeric Type Conversion', B)],
 sig='func celsiusToFahrenheit(_ celsius: Int) -> Double',
 statement="""Convert an **integer** Celsius value to Fahrenheit: `F = C × 9 / 5 + 32`.

 Careful: `celsius * 9 / 5` in integer arithmetic truncates — convert first.

 ```swift
 celsiusToFahrenheit(100)  // 212.0
 celsiusToFahrenheit(37)   // 98.6
 ```""",
 compare='float:1e-9',
 solution="func celsiusToFahrenheit(_ celsius: Int) -> Double {\n    Double(celsius) * 9 / 5 + 32\n}\n",
 explain="""Swift never converts numeric types implicitly — `Int * Double` doesn't compile. `Double(celsius)` converts once, and the literals `9`, `5`, `32` are then inferred as `Double`.""",
 tests=[({'celsius':100},212.0), ({'celsius':37},98.6), {'celsius':-40}, {'celsius':0}, {'celsius':1}, {'celsius':-273}]))
P.append(dict(id='bool-toggle-xor', title='Boolean Logic: Exactly One', topic='Booleans', notes='4', diff='easy',
 concepts=['fundamental-types'], docs=[('Basic Operators — Logical Operators', BO)],
 sig='func exactlyOne(_ a: Bool, _ b: Bool, _ c: Bool) -> Bool',
 statement="""Return `true` when **exactly one** of the three flags is `true`. Swift has no truthiness — `Bool` isn't an integer — so think about how to count them.""",
 solution="func exactlyOne(_ a: Bool, _ b: Bool, _ c: Bool) -> Bool {\n    [a, b, c].filter { $0 }.count == 1\n}\n",
 explain="""Since `Bool` doesn't convert to `Int`, count with `filter { $0 }.count` (or `[a, b, c].count(where: \\.self)` in Swift 6). For two flags, exactly-one is `a != b` — `!=` on `Bool` is XOR.""",
 tests=[({'a':True,'b':False,'c':False},True), ({'a':True,'b':True,'c':False},False), {'a':False,'b':False,'c':False}, {'a':True,'b':True,'c':True}, {'a':False,'b':False,'c':True}, {'a':False,'b':True,'c':True}]))
P.append(dict(id='leap-year', title='Leap Year', topic='Booleans', notes='4', diff='easy',
 concepts=['fundamental-types','control-flow'], docs=[('Basic Operators — Logical Operators', BO)],
 sig='func isLeapYear(_ year: Int) -> Bool',
 statement="""A year is a leap year if it is divisible by 4, **except** years divisible by 100, **unless** also divisible by 400. Use `isMultiple(of:)`.""",
 solution="func isLeapYear(_ year: Int) -> Bool {\n    year.isMultiple(of: 4) && (!year.isMultiple(of: 100) || year.isMultiple(of: 400))\n}\n",
 explain="""`isMultiple(of:)` reads better than `% x == 0` and handles negative numbers and zero correctly. `&&` and `||` short-circuit.""",
 tests=[({'year':2024},True), ({'year':1900},False), ({'year':2000},True), {'year':2023}, {'year':2100}, {'year':2400}, {'year':0}]))
# ---------- Strings (notes §2, §5)
P.append(dict(id='character-count', title='Characters vs Bytes', topic='Strings', notes='2', diff='easy',
 concepts=['strings-are-collections'], docs=[('Strings and Characters — Counting Characters', SC)],
 sig='func lengths(_ text: String) -> [Int]',
 statement="""Return `[characters, unicodeScalars, utf16 units, utf8 bytes]` for the string.

 ```swift
 lengths("abc")  // [3, 3, 3, 3]
 lengths("é")    // depends on how the é is encoded!
 ```""",
 solution="func lengths(_ text: String) -> [Int] {\n    [text.count, text.unicodeScalars.count, text.utf16.count, text.utf8.count]\n}\n",
 explain="""A `Character` is an **extended grapheme cluster** — what a human sees as one character. `"👨‍👩‍👧"` is 1 `Character` but 5 scalars, 8 UTF-16 units and 18 UTF-8 bytes. That's why `String` can't be indexed by `Int`, and why `count` is O(n).""",
 tests=[({'text':'abc'},[3,3,3,3]), {'text':''}, {'text':'e\u0301'}, {'text':'👨‍👩‍👧'}, {'text':'🇮🇳'}, {'text':'naïve café'}]))
P.append(dict(id='reverse-words', title='Reverse the Words', topic='Strings', notes='2', diff='easy',
 concepts=['strings-are-collections','map-filter-reduce'], docs=[('Strings and Characters', SC)],
 sig='func reverseWords(_ sentence: String) -> String',
 statement="""Reverse the order of words. Words are separated by one or more spaces; the result joins them with single spaces and has no leading/trailing spaces.

 ```swift
 reverseWords("the sky is blue")    // "blue is sky the"
 reverseWords("  hello   world ")   // "world hello"
 ```""",
 solution="func reverseWords(_ sentence: String) -> String {\n    sentence.split(separator: \" \").reversed().joined(separator: \" \")\n}\n",
 explain="""`split(separator:)` omits empty subsequences by default, which swallows the repeated spaces. It returns `[Substring]` — views into the original string — and `joined(separator:)` accepts those directly.""",
 tests=[({'sentence':'the sky is blue'},'blue is sky the'), ({'sentence':'  hello   world '},'world hello'), {'sentence':''}, {'sentence':'one'}, {'sentence':'a b  c   d'}, {'sentence':'Swift 🚀 is fun'}]))
P.append(dict(id='palindrome', title='Unicode-Aware Palindrome', topic='Strings', notes='2', diff='easy',
 concepts=['strings-are-collections','string-equality'], docs=[('Strings and Characters — Comparing Strings', SC)],
 sig='func isPalindrome(_ text: String) -> Bool',
 statement="""Return whether `text` reads the same forwards and backwards, **ignoring case and every character that isn't a letter or number**.

 ```swift
 isPalindrome("A man, a plan, a canal: Panama")  // true
 isPalindrome("race a car")                      // false
 ```""",
 solution="""
 func isPalindrome(_ text: String) -> Bool {
     let cleaned = text.lowercased().filter { $0.isLetter || $0.isNumber }
     return cleaned == String(cleaned.reversed())
 }
 """,
 explain="""`Character` has handy properties — `isLetter`, `isNumber`, `isWhitespace`, `isUppercase`. Filtering a `String` gives a `String`. `reversed()` is a lazy `ReversedCollection`, so wrap it in `String(...)` (or compare with `elementsEqual`).""",
 tests=[({'text':'A man, a plan, a canal: Panama'},True), ({'text':'race a car'},False), {'text':''}, {'text':'Was it a car or a cat I saw?'}, {'text':'été'}, {'text':'0P'}, {'text':'No lemon, no melon'}]))
P.append(dict(id='string-index-nth', title='The nth Character', topic='Strings', notes='2', diff='medium',
 concepts=['strings-are-collections'], docs=[('Strings and Characters — String Indices', SC)],
 sig='func character(in text: String, at offset: Int) -> String?',
 statement="""Return the character at integer `offset` (0-based) as a `String`, or `nil` if the offset is out of range (including negative). You can't write `text[offset]` — work with `String.Index`.

 ```swift
 character(in: "Swift", at: 1)   // "w"
 character(in: "🇮🇳ok", at: 0)   // "🇮🇳"
 character(in: "abc", at: 3)     // nil
 ```""",
 solution="""
 func character(in text: String, at offset: Int) -> String? {
     guard offset >= 0,
           let index = text.index(text.startIndex, offsetBy: offset, limitedBy: text.endIndex),
           index < text.endIndex
     else { return nil }
     return String(text[index])
 }
 """,
 explain="""`index(_:offsetBy:limitedBy:)` returns `nil` instead of trapping when you'd walk past the limit. Note `endIndex` is *one past* the last character, so it must be excluded too. Each step is O(1) but walking `n` characters is O(n).""",
 tests=[({'text':'Swift','offset':1},'w'), ({'text':'abc','offset':3},None), {'text':'🇮🇳ok','offset':0}, {'text':'abc','offset':-1}, {'text':'','offset':0}, {'text':'héllo','offset':1}, {'text':'abc','offset':2}]))
P.append(dict(id='vowel-count', title='Count Vowels with a Set', topic='Strings', notes='2', diff='easy',
 concepts=['strings-are-collections','set-vs-array'], docs=[('Strings and Characters', SC)],
 sig='func vowelCount(_ text: String) -> Int',
 statement="""Count the vowels `a e i o u` (either case).""",
 solution="""
 func vowelCount(_ text: String) -> Int {
     let vowels: Set<Character> = ["a", "e", "i", "o", "u"]
     return text.lowercased().filter { vowels.contains($0) }.count
 }
 """,
 explain="""A `Set<Character>` gives O(1) membership. Without the annotation `["a", ...]` would be inferred as `[String]` — the type annotation makes the literal a `Set` of `Character`s.""",
 tests=[({'text':'Hello World'},3), {'text':''}, {'text':'AEIOU aeiou'}, {'text':'rhythm'}, {'text':'Programming in Swift'}]))
P.append(dict(id='caesar-cipher', title='Caesar Cipher', topic='Strings', notes='2', diff='medium',
 concepts=['strings-are-collections','fundamental-types'], docs=[('Strings and Characters — Unicode Scalars', SC)],
 sig='func caesar(_ text: String, shift: Int) -> String',
 statement="""Shift every ASCII letter by `shift` places, wrapping around the alphabet and **preserving case**. Everything else is unchanged. `shift` may be negative or larger than 26.

 ```swift
 caesar("Hello, World!", shift: 3)  // "Khoor, Zruog!"
 caesar("abc", shift: -1)           // "zab"
 ```""",
 solution="""
 func caesar(_ text: String, shift: Int) -> String {
     let k = ((shift % 26) + 26) % 26
     return String(text.map { ch -> Character in
         guard let ascii = ch.asciiValue, ch.isLetter else { return ch }
         let base: UInt8 = ch.isUppercase ? 65 : 97
         return Character(UnicodeScalar((Int(ascii - base) + k) % 26 + Int(base))!)
     })
 }
 """,
 explain="""`Character.asciiValue` is `UInt8?` — `nil` for non-ASCII. `((shift % 26) + 26) % 26` normalises negative shifts because Swift's `%` keeps the sign of the dividend (`-1 % 26 == -1`).""",
 tests=[({'text':'Hello, World!','shift':3},'Khoor, Zruog!'), ({'text':'abc','shift':-1},'zab'), {'text':'xyz','shift':29}, {'text':'Ünïcode 123','shift':5}, {'text':'','shift':10}, {'text':'Swift','shift':-52}]))
P.append(dict(id='interpolation-receipt', title='Receipt Line with Interpolation', topic='String interpolation', notes='5', diff='easy',
 concepts=['string-interpolation'], docs=[('Strings and Characters — String Interpolation', SC)],
 sig='func receiptLine(item: String, quantity: Int, unitCents: Int) -> String',
 statement="""Build a receipt line: `"<quantity> x <item> @ $<unit> = $<total>"` where money is formatted as dollars with exactly two decimals, computed from **integer cents** (no floating point).

 ```swift
 receiptLine(item: "Coffee", quantity: 3, unitCents: 250)
 // "3 x Coffee @ $2.50 = $7.50"
 ```""",
 solution="""
 func dollars(_ cents: Int) -> String {
     let remainder = cents % 100
     return "$\\(cents / 100).\\(remainder < 10 ? "0" : "")\\(remainder)"
 }

 func receiptLine(item: String, quantity: Int, unitCents: Int) -> String {
     "\\(quantity) x \\(item) @ \\(dollars(unitCents)) = \\(dollars(quantity * unitCents))"
 }
 """,
 explain="""Interpolation accepts any expression, including function calls and ternaries. Keeping money in integer cents avoids `0.1 + 0.2` surprises. Foundation offers `String(format: "%.2f", x)` and `x.formatted(.currency(code: "USD"))` for real apps.""",
 tests=[({'item':'Coffee','quantity':3,'unitCents':250},'3 x Coffee @ $2.50 = $7.50'), {'item':'Bagel','quantity':1,'unitCents':105}, {'item':'Gum','quantity':10,'unitCents':5}, {'item':'Laptop','quantity':1,'unitCents':129999}, {'item':'Free sample','quantity':2,'unitCents':0}]))
P.append(dict(id='multiline-raw-strings', title='Raw & Multiline Strings', topic='String interpolation', notes='5', diff='easy',
 concepts=['raw-strings','string-interpolation'], docs=[('Strings and Characters — String Literals', SC)],
 sig='func windowsPath(user: String) -> String',
 statement="""Return the path `C:\\Users\\<user>\\Documents` using a **raw string** (`#"..."#`) so you don't have to escape every backslash, and interpolate `user` with raw-string interpolation syntax.

 ```swift
 windowsPath(user: "varun")   // C:\\Users\\varun\\Documents
 ```""",
 solution="func windowsPath(user: String) -> String {\n    #\"C:\\Users\\\\#(user)\\Documents\"#\n}\n",
 explain="""In a raw string `\\` is literal, so `\\(user)` would be printed verbatim — interpolation needs the same number of `#` as the delimiter: `\\#(user)`. Multiline literals use `\"\"\"` and strip indentation up to the closing delimiter.""",
 tests=[({'user':'varun'},'C:\\Users\\varun\\Documents'), {'user':'a b'}, {'user':''}]))
P.append(dict(id='predict-interpolation', title='Predict: print, debugPrint & terminator', topic='String interpolation', mode='predict', notes='5',
 concepts=['print-vs-debugprint','string-interpolation'], docs=[('Strings and Characters', SC)],
 statement="Predict the exact output, including quotes and where lines break.",
 snippet="""
 let name = "Swift"
 let version = 6.0
 print("Hello, \\(name) \\(version)!")
 print(1, 2, 3, separator: "-", terminator: " | ")
 print("same line")
 debugPrint(name)
 print([name, "\\(Int(version))"])
 print(name.uppercased().lowercased().count)
 """,
 explain="""`print` joins items with `separator` (default space) and ends with `terminator` (default newline). `debugPrint` shows strings *with quotes*, and arrays always print their elements in debug form. `6.0` prints as `6.0` — Swift keeps the decimal for `Double`."""))
P.append(dict(id='acronym', title='Make an Acronym', topic='Strings', notes='2', diff='easy',
 concepts=['compactmap-flatmap','strings-are-collections'], docs=[('Strings and Characters', SC)],
 sig='func acronym(_ phrase: String) -> String',
 statement="""Build an acronym from the first letter of each word, uppercased. Words are separated by spaces **or hyphens**; ignore empty pieces.

 ```swift
 acronym("Portable Network Graphics")    // "PNG"
 acronym("Complementary metal-oxide semiconductor")  // "CMOS"
 ```""",
 solution="""
 func acronym(_ phrase: String) -> String {
     String(phrase.split(whereSeparator: { $0 == " " || $0 == "-" }).compactMap(\\.first)).uppercased()
 }
 """,
 explain="""`split(whereSeparator:)` takes a predicate. `compactMap(\\.first)` uses a **key path as a function** and drops `nil`s. A `[Character]` converts straight into a `String`.""",
 tests=[({'phrase':'Portable Network Graphics'},'PNG'), ({'phrase':'Complementary metal-oxide semiconductor'},'CMOS'), {'phrase':''}, {'phrase':'  as soon   as possible '}, {'phrase':'ruby on-rails'}]))
P.append(dict(id='echo-stdin-upper', title='Shout Back (stdin)', topic='Strings', mode='stdio', notes='2', diff='easy',
 concepts=['strings-are-collections'], docs=[('Strings and Characters', SC)],
 statement="""Your first **stdin → stdout** problem. Read lines with `readLine()` until it returns `nil`. For each line print it uppercased followed by ` (<n> chars)` where `n` is its character count.

 Input:
 ```
 hello
 Swift 🚀
 ```
 Output:
 ```
 HELLO (5 chars)
 SWIFT 🚀 (7 chars)
 ```""",
 starter="while let line = readLine() {\n    // print something for each line\n}\n",
 solution="while let line = readLine() {\n    print(\"\\(line.uppercased()) (\\(line.count) chars)\")\n}\n",
 explain="""`readLine()` returns `String?` — `nil` at end of input — which makes `while let` the natural loop. It strips the trailing newline by default.""",
 tests=['hello\nSwift 🚀\n', '', 'a\n\nb\n', 'ümlaut\n']))

write_all(P, 'beginner', 100)
