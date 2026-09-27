import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CF='LanguageGuide/ControlFlow'; FN='LanguageGuide/Functions'; EN='LanguageGuide/Enumerations'; BO='LanguageGuide/BasicOperators'
P=[]
# ---------- Conditionals (§11) & ternary (§13)
P.append(dict(id='fix-temperature-range', title='Fix the Bug: Always-True Range Check', topic='Conditionals', notes='11', concepts=['control-flow','half-open-range'], docs=[('Basic Operators — Logical Operators', BO)],
 sig='func isPleasant(_ temp: Int) -> Bool',
 statement="""From your notes: this check is meant to be *"strictly between 20 and 39"* — but it returns `true` for **every** integer. Fix it (bonus: rewrite with a range's `contains`).""",
 starter="func isPleasant(_ temp: Int) -> Bool {\n    if temp > 20 || temp < 39 {\n        return true\n    }\n    return false\n}\n",
 solution="func isPleasant(_ temp: Int) -> Bool {\n    (21...38).contains(temp)\n}\n",
 explain="""Every `Int` is either `> 20` **or** `< 39`, so `||` can never be false — a silent bug. "Between" means `&&`. `(21...38).contains(temp)` says it directly, and `if cond { return true } return false` is just `return cond`.""",
 tests=[({'temp':26},True), ({'temp':50},False), ({'temp':-10},False), {'temp':20}, {'temp':21}, {'temp':38}, {'temp':39}]))
P.append(dict(id='fix-can-vote', title='Fix the Bug: Voting Age Boundary', topic='Ternary operator', notes='13', concepts=['ternary','control-flow'], docs=[('Basic Operators — Ternary Conditional Operator', BO)],
 sig='func canVote(age: Int) -> Bool',
 statement="""From your notes: `age > 18 ? true : false`. Two problems in one line — an 18-year-old *can* vote, and the ternary is dead weight. Fix both.""",
 starter="func canVote(age: Int) -> Bool {\n    age > 18 ? true : false\n}\n",
 solution="func canVote(age: Int) -> Bool {\n    age >= 18\n}\n",
 explain="""`x ? true : false` is always just `x` (and `x ? false : true` is `!x`). Off-by-one boundaries are the classic comparison bug — test the exact boundary value.""",
 tests=[({'age':18},True), ({'age':17},False), {'age':30}, {'age':0}, {'age':19}]))
P.append(dict(id='grade-letter', title='Letter Grade', topic='Conditionals', notes='11', concepts=['control-flow','switch-statement'], docs=[('Control Flow — Conditional Statements', CF)],
 sig='func letterGrade(_ score: Int) -> String',
 statement="""Scores 90–100 → `"A"`, 80–89 → `"B"`, 70–79 → `"C"`, 60–69 → `"D"`, 0–59 → `"F"`, anything else → `"invalid"`. Use a `switch` with range patterns.""",
 solution="""
 func letterGrade(_ score: Int) -> String {
     switch score {
     case 90...100: "A"
     case 80..<90: "B"
     case 70..<80: "C"
     case 60..<70: "D"
     case 0..<60: "F"
     default: "invalid"
     }
 }
 """,
 explain="""Range patterns match through `~=`. Since Swift 5.9 a `switch` is an **expression**: each case yields a value, so the function body is one expression with an implicit return. `default` is required — `Int` has more values than your cases cover.""",
 tests=[({'score':95},'A'), ({'score':80},'B'), {'score':79}, {'score':60}, {'score':59}, {'score':0}, {'score':100}, {'score':101}, {'score':-1}]))
P.append(dict(id='if-expression', title='if as an Expression', topic='Conditionals', notes='11', concepts=['ternary','control-flow'], docs=[('Control Flow — Conditional Statements', CF)],
 sig='func bmiCategory(weightKg: Double, heightM: Double) -> String',
 statement="""BMI = weight / height². Categories: `< 18.5` "underweight", `< 25` "normal", `< 30` "overweight", else "obese". Assign the result with a single **`let category = if … else if …`** expression.""",
 solution="""
 func bmiCategory(weightKg: Double, heightM: Double) -> String {
     let bmi = weightKg / (heightM * heightM)
     let category = if bmi < 18.5 {
         "underweight"
     } else if bmi < 25 {
         "normal"
     } else if bmi < 30 {
         "overweight"
     } else {
         "obese"
     }
     return category
 }
 """,
 explain="""`if`/`switch` expressions (Swift 5.9) let a `let` be assigned from branches without a mutable `var` or nested ternaries. Every branch must produce a value of the same type and must end with `else`.""",
 tests=[({'weightKg':70,'heightM':1.75},'normal'), {'weightKg':50,'heightM':1.8}, {'weightKg':85,'heightM':1.75}, {'weightKg':120,'heightM':1.7}, {'weightKg':56.7,'heightM':1.75}]))
# ---------- Switch (§12)
P.append(dict(id='diag-exhaustive-switch', title='Diagnostic: Make switch Exhaustive', topic='Switch', mode='diagnostic', notes='12', concepts=['switch-statement','enums'], docs=[('Control Flow — Switch', CF)],
 statement="""Your notes' Bug 5: `default` on your own enum hides new cases. Prove the safety net exists: declare `enum Weather { case sun, rain, wind, snow }`, then write a `switch` over a `Weather` value that handles **sun, rain and wind only**, with **no `default`**.

 You pass when the compiler refuses because the switch isn't exhaustive.""",
 starter="""
 enum Weather { case sun, rain, wind, snow }
 let forecast = Weather.snow

 switch forecast {
 case .sun: print("A nice day")
 default: print("Should be okay")
 }
 """,
 solution="""
 enum Weather { case sun, rain, wind, snow }
 let forecast = Weather.snow

 switch forecast {
 case .sun: print("A nice day")
 case .rain: print("Pack an umbrella")
 case .wind: print("Hold onto your hat")
 }
 """,
 explain="""`switch must be exhaustive` walks you to every place that needs updating when you add a case. Reserve `default` for open types (`Int`, `String`) and use `@unknown default` for other modules' non-frozen enums.""",
 tests=[{'name':'Non-exhaustive switch rejected','pattern':'switch must be exhaustive'}]))
P.append(dict(id='fizzbuzz-stdio', title='FizzBuzz from Standard Input', topic='Switch', mode='stdio', notes='12', concepts=['switch-statement','tuples','for-in'], docs=[('Control Flow — Switch', CF)],
 statement="""Read one integer `n` with `readLine()`. For every `i` in `1...n` print `Fizz` (divisible by 3), `Buzz` (by 5), `FizzBuzz` (both) or `i`. Print nothing if `n < 1`. Try switching on the tuple `(i % 3, i % 5)`.""",
 starter="let n = Int(readLine() ?? \"\") ?? 0\n",
 solution="""
 let n = Int(readLine() ?? "") ?? 0
 if n >= 1 {
     for i in 1...n {
         switch (i % 3, i % 5) {
         case (0, 0): print("FizzBuzz")
         case (0, _): print("Fizz")
         case (_, 0): print("Buzz")
         default: print(i)
         }
     }
 }
 """,
 explain="""Switching on a **tuple** makes each case read like its rule. `1...n` with `n < 1` traps (a closed range needs lower ≤ upper), hence the guard.""",
 tests=['5\n','15\n','0\n','1\n','-3\n'], hidden=2))
P.append(dict(id='switch-multiple-patterns', title='Classify Characters', topic='Switch', notes='12', concepts=['switch-statement','where-clause','pattern-matching'], docs=[('Control Flow — Compound Cases', CF)],
 sig='func classify(_ text: String) -> [String]',
 statement="""For each character return `"vowel"` (a e i o u, either case), `"digit"`, `"space"`, `"consonant"` (other letters) or `"other"`. Use **compound cases** (`case "a", "e", …:`) and a `where` clause.""",
 solution="""
 func classify(_ text: String) -> [String] {
     text.map { ch -> String in
         switch ch.lowercased() {
         case "a", "e", "i", "o", "u": return "vowel"
         case _ where ch.isNumber: return "digit"
         case " ": return "space"
         case _ where ch.isLetter: return "consonant"
         default: return "other"
         }
     }
 }
 """,
 explain="""Compound cases list alternatives separated by commas. `case _ where condition` lets any boolean test live in a switch. Order matters: the vowel case must come before the generic letter case.""",
 tests=[({'text':'Hi 5!'},['consonant','vowel','space','digit','other']), {'text':''}, {'text':'AEIOUxyz'}, {'text':'ß9 é'}]))
P.append(dict(id='fallthrough-description', title='fallthrough: Describe a Number', topic='Switch', notes='12', diff='easy', concepts=['fallthrough','break-continue'], docs=[('Control Flow — Fallthrough', CF)],
 sig='func describe(_ n: Int) -> String',
 statement="""Reproduce the Swift book's example: start with `"The number \\(n) is"`. If `n` is one of the primes `2, 3, 5, 7, 11, 13, 17, 19`, append `" a prime number, and also"` and then **`fallthrough`** to `default`, which appends `" an integer."`.

 ```swift
 describe(5)   // "The number 5 is a prime number, and also an integer."
 describe(4)   // "The number 4 is an integer."
 ```""",
 solution="""
 func describe(_ n: Int) -> String {
     var description = "The number \\(n) is"
     switch n {
     case 2, 3, 5, 7, 11, 13, 17, 19:
         description += " a prime number, and also"
         fallthrough
     default:
         description += " an integer."
     }
     return description
 }
 """,
 explain="""Swift cases **don't** fall through by default (no forgotten `break` bugs). `fallthrough` opts in, jumping into the next case's body **without checking its pattern**.""",
 tests=[({'n':5},'The number 5 is a prime number, and also an integer.'), ({'n':4},'The number 4 is an integer.'), {'n':19}, {'n':0}]))
# ---------- Loops (§14)
P.append(dict(id='fix-infinite-while', title='Fix the Bug: The Loop That Never Ends', topic='Loops', notes='14', diff='easy', concepts=['break-continue','for-in'], docs=[('Control Flow — Continue', CF)],
 sig='func nonJpegsReversed(_ files: [String]) -> [String]',
 timeLimitMs=1000,
 statement="""From your notes: this should return the non-`.jpeg` file names, last to first. Run it — you'll get **Time Limit Exceeded**. Find out why (`continue` skips something) and fix it. Best fix: let a `for`-`in` own the counter.""",
 starter="""
 func nonJpegsReversed(_ files: [String]) -> [String] {
     var result: [String] = []
     var i = files.count - 1
     while i >= 0 {
         if files[i].hasSuffix(".jpeg") {
             continue
         }
         result.append(files[i])
         i -= 1
     }
     return result
 }
 """,
 solution="""
 func nonJpegsReversed(_ files: [String]) -> [String] {
     var result: [String] = []
     for file in files.reversed() where !file.hasSuffix(".jpeg") {
         result.append(file)
     }
     return result
 }
 """,
 explain="""`continue` jumps straight back to the condition, skipping `i -= 1` — so once `i` points at a `.jpeg`, it stays there forever. A `for`-`in` can't forget to advance. Even shorter: `files.reversed().filter { !$0.hasSuffix(".jpeg") }`.""",
 tests=[({'files':['1.jpeg','2.txt','3.png']},['3.png','2.txt']), {'files':[]}, {'files':['a.jpeg']}, {'files':['a.txt','b.jpeg','c.jpeg','d.md']}]))
P.append(dict(id='labeled-break', title='Labelled break: Find a Pair', topic='Loops', notes='14', concepts=['break-continue'], docs=[('Control Flow — Labeled Statements', CF)],
 sig='func firstPair(_ grid: [[Int]], target: Int) -> [Int]',
 statement="""Search the 2-D `grid` row by row for the first cell equal to `target` and return `[row, col]`, or `[]`. Use a **labelled** outer loop and `break` out of both loops at once.""",
 solution="""
 func firstPair(_ grid: [[Int]], target: Int) -> [Int] {
     var found: [Int] = []
     search: for (r, row) in grid.enumerated() {
         for (c, value) in row.enumerated() where value == target {
             found = [r, c]
             break search
         }
     }
     return found
 }
 """,
 explain="""A label (`search:`) names a loop so `break search` / `continue search` can target it from an inner loop. (Here `return [r, c]` would also work — labels matter when there's more code after the loops.)""",
 tests=[({'grid':[[1,2],[3,4]],'target':3},[1,0]), ({'grid':[],'target':1},[]), {'grid':[[5,5],[5]],'target':5}, {'grid':[[1],[2,3,9]],'target':9}, {'grid':[[1]],'target':2}]))
P.append(dict(id='repeat-while-collatz', title='Collatz Steps (repeat-while)', topic='Loops', notes='14', concepts=['control-flow'], docs=[('Control Flow — Repeat-While', CF)],
 sig='func collatzSteps(_ n: Int) -> Int',
 statement="""Starting at `n ≥ 1`, repeatedly apply: even → `n / 2`, odd → `3n + 1`. Return how many steps it takes to reach 1 (0 if `n == 1`).""",
 solution="""
 func collatzSteps(_ n: Int) -> Int {
     var value = n
     var steps = 0
     while value != 1 {
         value = value.isMultiple(of: 2) ? value / 2 : 3 * value + 1
         steps += 1
     }
     return steps
 }
 """,
 explain="""`while` tests before each pass; `repeat { } while cond` tests after (runs at least once) — here the check-first form is right because `n == 1` needs zero steps.""",
 tests=[({'n':1},0), ({'n':6},8), {'n':27}, {'n':2}, {'n':97}, {'n':871}]))
P.append(dict(id='multiplication-table-stdio', title='Multiplication Table (stdin)', topic='Loops', mode='stdio', notes='14', concepts=['for-in','half-open-range','string-interpolation'], docs=[('Control Flow — For-In Loops', CF)],
 statement="""Input: two integers `n` and `upTo` on one line, separated by a space. Print `"<n> x <i> = <product>"` for `i` in `1...upTo` (nothing if `upTo < 1`).

 ```
 input:  5 3
 output: 5 x 1 = 5
         5 x 2 = 10
         5 x 3 = 15
 ```""",
 starter="let parts = (readLine() ?? \"\").split(separator: \" \").compactMap { Int($0) }\n",
 solution="""
 let parts = (readLine() ?? "").split(separator: " ").compactMap { Int($0) }
 let n = parts[0], upTo = parts[1]
 for i in stride(from: 1, through: upTo, by: 1) {
     print("\\(n) x \\(i) = \\(n * i)")
 }
 """,
 explain="""`stride(from: 1, through: upTo, by: 1)` is simply empty when `upTo < 1`, whereas `1...upTo` would trap. `compactMap { Int($0) }` parses and drops anything that isn't a number.""",
 tests=['5 3\n','7 0\n','12 12\n','-2 4\n'], hidden=1))
P.append(dict(id='pyramid-stdio', title='Print a Pyramid (stdin)', topic='Loops', mode='stdio', notes='14', diff='easy', concepts=['for-in','strings-are-collections'], docs=[('Strings and Characters — Initializing an Empty String','LanguageGuide/StringsAndCharacters')],
 statement="""Read `h` and print a centred pyramid of `*` of height `h` — row `i` (1-based) has `h - i` leading spaces and `2i - 1` stars, and **no trailing spaces**.

 ```
 input: 3
   *
  ***
 *****
 ```""",
 starter="let h = Int(readLine() ?? \"\") ?? 0\n",
 solution="""
 let h = Int(readLine() ?? "") ?? 0
 for i in stride(from: 1, through: h, by: 1) {
     print(String(repeating: " ", count: h - i) + String(repeating: "*", count: 2 * i - 1))
 }
 """,
 explain="""`String(repeating:count:)` builds padding without a loop. The judge's default comparison ignores *trailing* whitespace but not leading — so the indentation matters.""",
 tests=['3\n','1\n','0\n','5\n'], compare='exact', hidden=1))
P[-1]['compare']='trimmed'
# ---------- Functions (§15, §17, §18)
P.append(dict(id='argument-labels', title='Argument Labels That Read Like English', topic='Functions', notes='17', concepts=['argument-labels','functions-basics'], docs=[('Functions — Function Argument Labels and Parameter Names', FN)],
 sig='func move(from start: Int, to end: Int, by step: Int) -> [Int]',
 statement="""The call site is `move(from: 2, to: 10, by: 3)`, but inside the function you want the names `start`, `end`, `step`. Return the positions visited, from `start` up to (but not past) `end`.

 ```swift
 move(from: 2, to: 10, by: 3)  // [2, 5, 8]
 ```""",
 starter="func move(from start: Int, to end: Int, by step: Int) -> [Int] {\n    return []\n}\n",
 solution="func move(from start: Int, to end: Int, by step: Int) -> [Int] {\n    Array(stride(from: start, through: end, by: step))\n}\n",
 explain="""Each parameter has an **argument label** (outside) and a **parameter name** (inside). Good labels make calls read as sentences — `move(from:to:by:)` is the function's full name.""",
 tests=[({'start':2,'end':10,'step':3},[2,5,8]), {'start':0,'end':0,'step':1}, {'start':5,'end':1,'step':1}, {'start':1,'end':10,'step':1}]))
P.append(dict(id='default-parameters', title='Default Parameter Values', topic='Functions', notes='18', concepts=['default-params','functions-basics'], docs=[('Functions — Default Parameter Values', FN)],
 sig='func greetAll(_ names: [String]) -> [String]',
 statement="""Write `func greet(_ name: String, greeting: String = "Hello", punctuation: String = "!") -> String` returning e.g. `"Hello, Ana!"`. Then `greetAll` greets the names like this:

 - the 1st name uses both defaults,
 - the 2nd uses `greeting: "Hi"`,
 - every other name uses `punctuation: "."` and the default greeting.""",
 solution="""
 func greet(_ name: String, greeting: String = "Hello", punctuation: String = "!") -> String {
     "\\(greeting), \\(name)\\(punctuation)"
 }

 func greetAll(_ names: [String]) -> [String] {
     names.enumerated().map { i, name in
         switch i {
         case 0: greet(name)
         case 1: greet(name, greeting: "Hi")
         default: greet(name, punctuation: ".")
         }
     }
 }
 """,
 explain="""Parameters with defaults can be **omitted individually** — `greet(name, punctuation: ".")` skips `greeting`. Defaults usually replace a pile of overloads.""",
 tests=[({'names':['Ana','Bo','Cy']},['Hello, Ana!','Hi, Bo!','Hello, Cy.']), {'names':[]}, {'names':['Solo']}]))
P.append(dict(id='variadic-average', title='Variadic Average', topic='Functions', notes='15', concepts=['variadic'], docs=[('Functions — Variadic Parameters', FN)],
 sig='func averages(_ groups: [[Double]]) -> [Double?]',
 statement="""Write `func average(_ numbers: Double...) -> Double?` (nil for no numbers). Variadic parameters can't receive an existing array, so also write `func average(of numbers: [Double]) -> Double?` and have the variadic one call it. `averages` returns `average(of:)` for each group.

 Bonus: `averages` must call the variadic version at least once — e.g. `average(1, 2, 3)` — to check it compiles.""",
 compare='float:1e-9',
 solution="""
 func average(of numbers: [Double]) -> Double? {
     numbers.isEmpty ? nil : numbers.reduce(0, +) / Double(numbers.count)
 }

 func average(_ numbers: Double...) -> Double? {
     average(of: numbers)
 }

 func averages(_ groups: [[Double]]) -> [Double?] {
     precondition(average(1, 2, 3) == 2)
     return groups.map { average(of: $0) }
 }
 """,
 explain="""Inside the function a variadic `Double...` **is** a `[Double]`. Swift has no "splat" to pass an array into a variadic parameter, so the standard pattern is an array-taking overload that the variadic one forwards to.""",
 tests=[({'groups':[[1,2,3],[]]},[2.0,None]), {'groups':[[5]]}, {'groups':[[1.5,2.5],[-1,1],[0.1,0.2,0.3]]}]))
P.append(dict(id='overloading-describe', title='Overloading by Type', topic='Functions', notes='15', concepts=['overloading-overriding','functions-basics'], docs=[('Functions', FN)],
 sig='func describeAll(ints: [Int], words: [String], flags: [Bool]) -> [String]',
 statement="""Write three overloads of `func describe(_ value: …) -> String`:
 - `Int` → `"int <value>"`
 - `String` → `"string '<value>' (<count>)"`
 - `Bool` → `"bool yes"` / `"bool no"`

 `describeAll` describes all ints, then all words, then all flags. The compiler picks the overload from each argument's static type.""",
 solution="""
 func describe(_ value: Int) -> String { "int \\(value)" }
 func describe(_ value: String) -> String { "string '\\(value)' (\\(value.count))" }
 func describe(_ value: Bool) -> String { "bool \\(value ? "yes" : "no")" }

 func describeAll(ints: [Int], words: [String], flags: [Bool]) -> [String] {
     ints.map(describe) + words.map(describe) + flags.map(describe)
 }
 """,
 explain="""Overloads share a base name but differ in parameter types, labels or return type; resolution happens **at compile time**. Note `ints.map(describe)` — passing an overloaded function by name works because the expected type `(Int) -> String` disambiguates it.""",
 tests=[({'ints':[1],'words':['hi'],'flags':[True,False]},['int 1',"string 'hi' (2)",'bool yes','bool no']), {'ints':[],'words':[],'flags':[]}, {'ints':[-3,0],'words':['','🦅'],'flags':[]}]))
P.append(dict(id='nested-functions', title='Nested Functions & Function Types', topic='Functions', notes='15', diff='medium', concepts=['functions-basics','closures'], docs=[('Functions — Nested Functions', FN)],
 sig='func stepper(backward: Bool, start: Int, steps: Int) -> [Int]',
 statement="""Inside `stepper`, define two **nested** functions `stepForward(_:)` (+1) and `stepBackward(_:)` (-1). Pick one into a `let step: (Int) -> Int` based on `backward`, then apply it `steps` times starting from `start`, collecting every value **after** each step.""",
 solution="""
 func stepper(backward: Bool, start: Int, steps: Int) -> [Int] {
     func stepForward(_ x: Int) -> Int { x + 1 }
     func stepBackward(_ x: Int) -> Int { x - 1 }
     let step: (Int) -> Int = backward ? stepBackward : stepForward
     var current = start
     var visited: [Int] = []
     for _ in 0..<max(0, steps) {
         current = step(current)
         visited.append(current)
     }
     return visited
 }
 """,
 explain="""Functions are values with types like `(Int) -> Int`, so you can store them, pass them and choose between them. Nested functions are hidden from the outside world but can capture the enclosing function's variables.""",
 tests=[({'backward':False,'start':0,'steps':3},[1,2,3]), {'backward':True,'start':3,'steps':4}, {'backward':True,'start':0,'steps':0}]))
P.append(dict(id='implicit-return-sign', title='Implicit Returns', topic='Functions', notes='15', diff='easy', concepts=['implicit-return','switch-statement'], docs=[('Functions — Functions With an Implicit Return', FN)],
 sig='func signs(_ nums: [Int]) -> [String]',
 statement="""Write a helper `func sign(_ n: Int) -> String` returning `"negative"`, `"zero"` or `"positive"` whose body is a **single `switch` expression** with no `return` keyword. `signs` maps it over the input.""",
 solution="""
 func sign(_ n: Int) -> String {
     switch n {
     case ..<0: "negative"
     case 0: "zero"
     default: "positive"
     }
 }

 func signs(_ nums: [Int]) -> [String] {
     nums.map(sign)
 }
 """,
 explain="""A function whose body is a single expression returns it implicitly — and `if`/`switch` count as expressions since Swift 5.9. `..<0` is a one-sided range pattern.""",
 tests=[({'nums':[-2,0,5]},['negative','zero','positive']), {'nums':[]}, {'nums':[-9223372036854775808, 9223372036854775807]}]))
# ---------- Enums (§9)
P.append(dict(id='enum-raw-values', title='Raw Values: Planet Order', topic='Enums', notes='9', concepts=['enums','associated-values','failable-init'], docs=[('Enumerations — Raw Values', EN)],
 sig='func planetNames(_ positions: [Int]) -> [String]',
 statement="""Declare `enum Planet: Int { case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune }`. For each position return the planet's name (use `"\\(planet)"`) or `"unknown"` if `Planet(rawValue:)` fails.""",
 solution="""
 enum Planet: Int {
     case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
 }

 func planetNames(_ positions: [Int]) -> [String] {
     positions.map { Planet(rawValue: $0).map { "\\($0)" } ?? "unknown" }
 }
 """,
 explain="""Integer raw values **auto-increment** from the first explicit one. `init?(rawValue:)` is a synthesised **failable** initialiser returning an optional. Interpolating an enum case prints its name.""",
 tests=[({'positions':[3,1,9]},['earth','mercury','unknown']), {'positions':[]}, {'positions':[0,8,4]}]))
P.append(dict(id='enum-case-iterable', title='CaseIterable Menu', topic='Enums', notes='9', concepts=['case-iterable','enums'], docs=[('Enumerations — Iterating over Enumeration Cases', EN)],
 sig='func menu(maxPrice: Int) -> [String]',
 statement="""Declare `enum Coffee: String, CaseIterable { case espresso, latte, cappuccino, mocha }` with a computed `price: Int` property — 2, 4, 4, 5 respectively. Return the raw values of every coffee costing at most `maxPrice`, in declaration order.""",
 solution="""
 enum Coffee: String, CaseIterable {
     case espresso, latte, cappuccino, mocha

     var price: Int {
         switch self {
         case .espresso: 2
         case .latte, .cappuccino: 4
         case .mocha: 5
         }
     }
 }

 func menu(maxPrice: Int) -> [String] {
     Coffee.allCases.filter { $0.price <= maxPrice }.map(\\.rawValue)
 }
 """,
 explain="""`CaseIterable` synthesises `allCases` in declaration order. `String` raw values default to the case name. Enums can't have stored properties, but computed properties switching on `self` are idiomatic.""",
 tests=[({'maxPrice':4},['espresso','latte','cappuccino']), {'maxPrice':1}, {'maxPrice':5}]))
P.append(dict(id='enum-associated-shapes', title='Associated Values: Shapes', topic='Enums', notes='9', diff='medium', concepts=['associated-values','enums','pattern-matching'], docs=[('Enumerations — Associated Values', EN)],
 sig='func totalArea(_ specs: [String]) -> Double',
 compare='float:1e-9',
 statement="""Model `enum Shape { case circle(radius: Double); case rectangle(width: Double, height: Double); case triangle(base: Double, height: Double) }` with an `area` computed property.

 Parse each spec — `"circle 2"`, `"rectangle 3 4"`, `"triangle 6 2"` — into a `Shape` (skip malformed specs) and return the total area. Use `Double.pi`.""",
 solution="""
 enum Shape {
     case circle(radius: Double)
     case rectangle(width: Double, height: Double)
     case triangle(base: Double, height: Double)

     var area: Double {
         switch self {
         case .circle(let r): .pi * r * r
         case let .rectangle(w, h): w * h
         case let .triangle(b, h): b * h / 2
         }
     }

     init?(spec: String) {
         let parts = spec.split(separator: " ")
         let nums = parts.dropFirst().compactMap { Double($0) }
         switch (parts.first, nums.count) {
         case ("circle", 1): self = .circle(radius: nums[0])
         case ("rectangle", 2): self = .rectangle(width: nums[0], height: nums[1])
         case ("triangle", 2): self = .triangle(base: nums[0], height: nums[1])
         default: return nil
         }
     }
 }

 func totalArea(_ specs: [String]) -> Double {
     specs.compactMap(Shape.init(spec:)).reduce(0) { $0 + $1.area }
 }
 """,
 explain="""Associated values attach **per-instance** data to a case; `case let .rectangle(w, h)` binds them. A failable `init?` on the enum is a neat parser. Note `Shape.init(spec:)` passed as a function to `compactMap`.""",
 tests=[({'specs':['rectangle 3 4','triangle 6 2']},18.0), {'specs':['circle 1']}, {'specs':[]}, {'specs':['hexagon 2','circle x','rectangle 2 2 2','rectangle 0.5 4']}]))
P.append(dict(id='enum-mutating-toggle', title='Mutating Enum: Traffic Light', topic='Enums', notes='9', concepts=['mutating','enums'], docs=[('Enumerations', EN),('Methods — Modifying Value Types','LanguageGuide/Methods')],
 sig='func lightSequence(steps: Int) -> [String]',
 statement="""Declare `enum TrafficLight: String { case red, green, yellow }` with a **`mutating func next()`** that cycles red → green → yellow → red. Starting from red, return the raw value after each of `steps` calls.""",
 solution="""
 enum TrafficLight: String {
     case red, green, yellow

     mutating func next() {
         self = switch self {
         case .red: .green
         case .green: .yellow
         case .yellow: .red
         }
     }
 }

 func lightSequence(steps: Int) -> [String] {
     var light = TrafficLight.red
     var seen: [String] = []
     for _ in 0..<steps {
         light.next()
         seen.append(light.rawValue)
     }
     return seen
 }
 """,
 explain="""Enum methods that change the value must be `mutating`, and they do it by **assigning a new case to `self`**. You can only call them on a `var`.""",
 tests=[({'steps':4},['green','yellow','red','green']), {'steps':0}, {'steps':7}]))
P.append(dict(id='predict-enum-switch-order', title='Predict: Enum Payloads & if case', topic='Enums', mode='predict', notes='9', concepts=['associated-values','pattern-matching'], docs=[('Enumerations — Associated Values', EN)],
 statement="Predict the output.",
 snippet="""
 enum Event {
     case login(user: String)
     case purchase(item: String, cents: Int)
     case logout
 }

 let events: [Event] = [.login(user: "ana"), .purchase(item: "book", cents: 1299), .purchase(item: "pen", cents: 150), .logout]

 var total = 0
 for event in events {
     if case .purchase(_, let cents) = event {
         total += cents
     }
 }
 print("spent \\(total)")

 for case .purchase(let item, let cents) in events where cents > 1000 {
     print("big: \\(item)")
 }

 if case .login(let user) = events[0] {
     print(user.uppercased())
 }
 print(events.count)
 """,
 explain="""`if case pattern = value` tests one pattern without a whole `switch`. `for case pattern in sequence` iterates only matching elements, and `where` filters further. `_` ignores an associated value."""))

write_all(P, 'beginner', 500)
