import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
TB='LanguageGuide/TheBasics'; BO='LanguageGuide/BasicOperators'; SC='LanguageGuide/StringsAndCharacters'; CT='LanguageGuide/CollectionTypes'; CF='LanguageGuide/ControlFlow'; FN='LanguageGuide/Functions'; EH='LanguageGuide/ErrorHandling'; EN='LanguageGuide/Enumerations'
P=[]
P.append(dict(id='checkpoint-2-unique-count', title='Checkpoint 2: Count Unique Items', topic='Collections', concepts=['set-vs-array','collection-types'], docs=[('Collection Types — Sets', CT)],
 sig='func uniqueReport(_ items: [String]) -> [Int]',
 statement="""Paul Hudson's *100 Days of SwiftUI* Checkpoint 2: given an array of strings, report `[total count, unique count]`. Create the unique count by converting to a `Set`.""",
 solution="func uniqueReport(_ items: [String]) -> [Int] {\n    [items.count, Set(items).count]\n}\n",
 explain="""A `Set` keeps one of each element, so `Set(array).count` is the number of distinct values — O(n) with hashing, no nested loops.""",
 hints=("Which collection type refuses to store duplicates?","Build a `Set` from the array; its `count` is the unique count.","`[items.count, Set(items).count]`"),
 tests=[({'items':['a','b','a']},[3,2]), {'items':[]}, {'items':['x','x','x']}, {'items':['Swift','swift','SWIFT']}]))
P.append(dict(id='checkpoint-4-integer-sqrt', title='Checkpoint 4: Integer Square Root with Errors', topic='Error handling', diff='medium', concepts=['error-handling','functions-basics'], docs=[('Error Handling', EH)],
 sig='func integerSqrt(_ n: Int) throws -> Int',
 statement="""Checkpoint 4: write a function that returns the integer square root of a number from 1 to 10,000 — without using `sqrt()`.
 - throw `SqrtError.outOfBounds` if `n < 1` or `n > 10_000`
 - throw `SqrtError.noRoot` if `n` isn't a perfect square

 Brute force is fine: there are only 100 candidates.""",
 starter="enum SqrtError: Error { case outOfBounds, noRoot }\n\nfunc integerSqrt(_ n: Int) throws -> Int {\n    return 0\n}\n",
 solution="""
 enum SqrtError: Error { case outOfBounds, noRoot }

 func integerSqrt(_ n: Int) throws -> Int {
     guard (1...10_000).contains(n) else { throw SqrtError.outOfBounds }
     for i in 1...100 where i * i == n {
         return i
     }
     throw SqrtError.noRoot
 }
 """,
 explain="""`guard` handles the out-of-range case first; the `for … where` loop returns as soon as it finds the root, and falling out of the loop means there isn't one. The judge shows thrown errors as `{"$error": "…"}`.""",
 hints=("Which checks can fail before you even start looping?","Guard the range with `(1...10_000).contains(n)`, then loop `1...100` looking for `i * i == n`.","`for i in 1...100 where i * i == n { return i }` then `throw SqrtError.noRoot`."),
 tests=[({'n':25},5), ({'n':26},{'$error':'noRoot'}), ({'n':0},{'$error':'outOfBounds'}), {'n':1}, {'n':10000}, {'n':10001}, {'n':9801}]))
P.append(dict(id='checkpoint-5-lucky-numbers', title='Checkpoint 5: Lucky Numbers Pipeline', topic='Closures', concepts=['map-filter-reduce','closures','higher-order-functions'], docs=[('Closures', 'LanguageGuide/Closures')],
 sig='func luckyNumbers(_ numbers: [Int]) -> [String]',
 statement="""Checkpoint 5: filter out **even** numbers, sort ascending, and map each to `"<n> is a lucky number"` — as a single chain with no temporary variables.""",
 solution="func luckyNumbers(_ numbers: [Int]) -> [String] {\n    numbers.filter { !$0.isMultiple(of: 2) }.sorted().map { \"\\($0) is a lucky number\" }\n}\n",
 explain="""Chaining `filter` → `sorted` → `map` reads top to bottom like a data pipeline; each step returns a new array.""",
 hints=("Three higher-order functions, one after another.","`filter` keeps odd numbers, `sorted()` orders them, `map` builds strings.","`numbers.filter { !$0.isMultiple(of: 2) }.sorted().map { \"\\($0) is a lucky number\" }`."),
 tests=[({'numbers':[7,4,38,21,16,15,12,33,31,49]},['7 is a lucky number','15 is a lucky number','21 is a lucky number','31 is a lucky number','33 is a lucky number','49 is a lucky number']), {'numbers':[]}, {'numbers':[2,4]}, {'numbers':[-3,1,-1]}]))
P.append(dict(id='compound-assignment', title='Compound Assignment Operators', topic='Operators', concepts=['fundamental-types','string-interpolation'], docs=[('Basic Operators — Compound Assignment Operators', BO)],
 sig='func scoreboard(_ events: [String]) -> [String]',
 statement="""Start with `score = 10` and `title = "Game"`. Apply events using **compound assignment**:
 - `"+n"` → `score += n`, `"-n"` → `score -= n`, `"*n"` → `score *= n`, `"/n"` → `score /= n` (skip if n is 0)
 - `"!word"` → `title += " " + word`

 Return `[title, "\\(score)"]`.""",
 solution="""
 func scoreboard(_ events: [String]) -> [String] {
     var score = 10
     var title = "Game"
     for event in events {
         guard let op = event.first else { continue }
         let rest = String(event.dropFirst())
         if op == "!" { title += " " + rest; continue }
         guard let n = Int(rest) else { continue }
         switch op {
         case "+": score += n
         case "-": score -= n
         case "*": score *= n
         case "/": if n != 0 { score /= n }
         default: break
         }
     }
     return [title, "\\(score)"]
 }
 """,
 explain="""`+=`, `-=`, `*=`, `/=` modify in place — and `+=` works on `String` too. Integer `/` truncates toward zero, and dividing by zero traps, hence the guard.""",
 hints=("`a += b` is shorthand for `a = a + b` — and it works for strings too.","Take the first character as the operator and parse the rest as an `Int`.","`switch op { case \"+\": score += n … case \"/\": if n != 0 { score /= n } }`."),
 tests=[({'events':['+5','*2','!Over','/3']},['Game Over','10']), {'events':[]}, {'events':['/0','-20','!A','!B']}, {'events':['x','+','*-3']}]))
P.append(dict(id='multi-line-strings', title='Predict: Multi-line String Literals', topic='Strings', mode='predict', concepts=['raw-strings','string-interpolation'], docs=[('Strings and Characters — Multiline String Literals', SC)],
 statement="Predict the exact output. Pay attention to indentation and the backslash at a line end.",
 snippet='''
 let name = "Taylor"
 let poem = """
     Roses are red,
       \\(name) is too,
     this line continues \\
     here.
     """
 print(poem)
 print(poem.split(separator: "\\n").count)
 ''',
 explain="""Indentation up to the closing `\"\"\"` is stripped from every line; extra indentation is kept. A trailing `\\` joins the next line without a newline. Interpolation works inside multiline literals.""",
 hints=("The closing `\"\"\"` sets the indentation that gets removed from every line.","The second line keeps its **extra** two spaces; the `\\` at a line end removes that line break.","The poem has 3 lines: `Roses are red,`, `  Taylor is too,`, `this line continues here.`")))
P.append(dict(id='string-methods', title='String Methods Toolkit', topic='Strings', concepts=['strings-are-collections','string-equality'], docs=[('Strings and Characters', SC)],
 sig='func analyze(_ text: String) -> [String]',
 statement="""Return facts about `text`, one string each, using `String` methods (import Foundation where needed):
 1. `hasPrefix("http")` → `"url"` or `"text"`
 2. uppercased first letter + rest (`"hello" → "Hello"`; empty stays empty)
 3. `text.contains("swift")` case-insensitively → `"true"`/`"false"`
 4. text with every `" "` replaced by `"_"`
 5. `"\\(text.count)"`""",
 solution="""
 import Foundation

 func analyze(_ text: String) -> [String] {
     let capitalized = text.prefix(1).uppercased() + text.dropFirst()
     return [
         text.hasPrefix("http") ? "url" : "text",
         capitalized,
         String(text.localizedCaseInsensitiveContains("swift")),
         text.replacingOccurrences(of: " ", with: "_"),
         "\\(text.count)",
     ]
 }
 """,
 explain="""`prefix(1)` and `dropFirst()` return `Substring`s, and `+` joins them into a `String`. `localizedCaseInsensitiveContains` and `replacingOccurrences` come from Foundation; Swift 5.7+ also has `replacing(_:with:)` in the standard library.""",
 hints=("Many handy string methods live in Foundation — import it.","Capitalise with `prefix(1).uppercased() + dropFirst()`; search with `localizedCaseInsensitiveContains`.","`text.replacingOccurrences(of: \" \", with: \"_\")` for item 4."),
 tests=[({'text':'hello Swift world'},['text','Hello Swift world','true','hello_Swift_world','17']), {'text':''}, {'text':'https://swift.org'}, {'text':'é clair'}]))
P.append(dict(id='array-methods', title='Array Methods: insert, remove, firstIndex', topic='Arrays', concepts=['array-basics'], docs=[('Collection Types — Arrays', CT)],
 sig='func playlist(_ commands: [String]) -> [String]',
 statement="""Maintain a playlist (starting empty) with commands:
 - `add X` → append · `front X` → insert at index 0 · `remove X` → remove the **first** occurrence (if any)
 - `swap` → swap first and last (if ≥ 2) · `reverse` → reverse in place · `sort` → sort ascending

 Return the final playlist.""",
 solution="""
 func playlist(_ commands: [String]) -> [String] {
     var songs: [String] = []
     for command in commands {
         let parts = command.split(separator: " ", maxSplits: 1).map(String.init)
         switch (parts[0], parts.count) {
         case ("add", 2): songs.append(parts[1])
         case ("front", 2): songs.insert(parts[1], at: 0)
         case ("remove", 2):
             if let i = songs.firstIndex(of: parts[1]) { songs.remove(at: i) }
         case ("swap", 1): if songs.count >= 2 { songs.swapAt(0, songs.count - 1) }
         case ("reverse", 1): songs.reverse()
         case ("sort", 1): songs.sort()
         default: break
         }
     }
     return songs
 }
 """,
 explain="""`firstIndex(of:)` returns an optional index; `remove(at:)` traps on a bad index, so unwrap first. `reverse()`/`sort()` mutate in place, while `reversed()`/`sorted()` return new values.""",
 hints=("Arrays have `append`, `insert(_:at:)`, `remove(at:)`, `firstIndex(of:)`, `swapAt`, `reverse()` and `sort()`.","Split each command into a verb and an optional argument, then switch on them.","`if let i = songs.firstIndex(of: name) { songs.remove(at: i) }`."),
 tests=[({'commands':['add b','add a','front c','remove b','sort']},['a','c']), {'commands':[]}, {'commands':['add x','add y','add z','swap','reverse']}, {'commands':['remove q','add two words']}]))
P.append(dict(id='predict-empty-collections', title='Predict: Creating Empty Collections', topic='Collections', mode='predict', concepts=['collection-types','type-inference'], docs=[('Collection Types', CT)],
 statement="Predict the output.",
 snippet="""
 var scores = [String: Int]()
 var names = [String]()
 var ids = Set<Int>()
 var more = Array<Int>()
 scores["ana"] = 3
 names.append("bo")
 ids.insert(7); ids.insert(7)
 more += [1, 2]
 print(scores, names, ids, more)
 print(scores.isEmpty, names.count, ids.count, more.isEmpty)
 print([Int]() == [], [String: Int]().count)
 """,
 explain="""`[T]()`, `[K: V]()` and `Set<T>()` create empty collections; `Array<T>()` is the long form. Inserting a duplicate into a `Set` is ignored.""",
 hints=("Each line creates an empty collection with a different spelling.","A `Set` ignores the second `insert(7)`.","Line 1: `[\"ana\": 3] [\"bo\"] [7] [1, 2]`.")))
P.append(dict(id='dictionary-merge', title='Merging Dictionaries', topic='Dictionaries', concepts=['dictionary-basics'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func mergeInventories(_ a: [String: Int], _ b: [String: Int]) -> [String: Int]',
 statement="""Merge two inventories, **adding** quantities for items in both. Then remove any item whose total is 0 or less. Use `merging(_:uniquingKeysWith:)` and `filter`.""",
 solution="""
 func mergeInventories(_ a: [String: Int], _ b: [String: Int]) -> [String: Int] {
     a.merging(b, uniquingKeysWith: +).filter { $0.value > 0 }
 }
 """,
 explain="""`merging` asks what to do on a key clash; passing the `+` operator as the combine function sums them. `filter` on a dictionary returns a dictionary (Swift 4+).""",
 hints=("Dictionaries have a method that merges another dictionary and resolves key clashes.","`merging(_:uniquingKeysWith:)` takes a function `(old, new) -> value` — an operator can be that function.","`a.merging(b, uniquingKeysWith: +).filter { $0.value > 0 }`."),
 tests=[({'a':{'apple':3,'pear':1},'b':{'apple':2,'fig':5}},{'apple':5,'pear':1,'fig':5}), {'a':{},'b':{}}, {'a':{'x':2},'b':{'x':-2,'y':-1}}]))
P.append(dict(id='ordered-dedupe', title='Remove Duplicates, Keep Order', topic='Sets', concepts=['set-vs-array','equatable-hashable'], docs=[('Collection Types — Sets', CT)],
 sig='func dedupe(_ values: [Int]) -> [Int]',
 statement="""Remove duplicates while keeping the **first** occurrence order. `Array(Set(values))` loses order — use a `Set` only to remember what you've seen.""",
 solution="""
 func dedupe(_ values: [Int]) -> [Int] {
     var seen = Set<Int>()
     return values.filter { seen.insert($0).inserted }
 }
 """,
 explain="""`Set.insert` returns `(inserted: Bool, memberAfterInsert:)`, so one call both checks and records membership. O(n) overall.""",
 hints=("A set is great for \"have I seen this?\" — but it has no order.","Walk the array; keep an element only the first time you insert it into the set.","`values.filter { seen.insert($0).inserted }`."),
 tests=[({'values':[3,1,3,2,1]},[3,1,2]), {'values':[]}, {'values':[5,5,5]}, {'values':[1,2,3]}]))
P.append(dict(id='enum-string-raw', title='String Raw Values & Case Names', topic='Enums', concepts=['enums','associated-values'], docs=[('Enumerations — Raw Values', EN)],
 sig='func parseSizes(_ codes: [String]) -> [String]',
 statement="""Declare `enum Size: String { case small = "S", medium = "M", large = "L", extraLarge = "XL" }`. For each code return `"<caseName>=<rawValue>"` (e.g. `"large=L"`) or `"invalid"`.""",
 solution="""
 enum Size: String {
     case small = "S", medium = "M", large = "L", extraLarge = "XL"
 }

 func parseSizes(_ codes: [String]) -> [String] {
     codes.map { code in
         guard let size = Size(rawValue: code) else { return "invalid" }
         return "\\(size)=\\(size.rawValue)"
     }
 }
 """,
 explain="""With explicit `String` raw values, `rawValue` differs from the case name; interpolating the case prints its **name**. Without explicit values, a `String` raw value defaults to the case name.""",
 hints=("An enum can have `String` raw values different from its case names.","Use `Size(rawValue:)` — it returns an optional.","`\"\\(size)=\\(size.rawValue)\"`."),
 tests=[({'codes':['L','XL','Q']},['large=L','extraLarge=XL','invalid']), {'codes':[]}, {'codes':['s','S','M']}]))
P.append(dict(id='diag-type-annotation', title='Diagnostic: Type Annotation Mismatch', topic='Type inference', mode='diagnostic', concepts=['type-inference','fundamental-types'], docs=[('The Basics — Type Annotations', TB)],
 statement="""Declare `let score: Int = "100"` — a type annotation that disagrees with the value. You pass when the compiler refuses to convert.""",
 starter="let score: Int = 100\nprint(score)\n",
 solution="let score: Int = \"100\"\nprint(score)\n",
 explain="""*cannot convert value of type 'String' to specified type 'Int'*. Swift never converts between types implicitly — use `Int("100")`, which returns an `Int?`.""",
 hints=("Swift is strict about types, even for literals.","Annotate the constant as `Int` but give it a string literal.","`let score: Int = \"100\"`."),
 tests=[{'name':'Conversion rejected','pattern':"cannot convert value of type 'String' to specified type 'Int'"}]))
P.append(dict(id='skipping-items', title='continue: Skipping Items', topic='Loops', concepts=['break-continue','for-in'], docs=[('Control Flow — Continue', CF)],
 sig='func sumValidReadings(_ readings: [String]) -> [Int]',
 statement="""Sum sensor readings, skipping (with `continue`) anything that isn't an integer or is negative, and stopping entirely (with `break`) at the first `"END"`. Return `[sum, count of values used]`.""",
 solution="""
 func sumValidReadings(_ readings: [String]) -> [Int] {
     var sum = 0, used = 0
     for reading in readings {
         if reading == "END" { break }
         guard let value = Int(reading), value >= 0 else { continue }
         sum += value
         used += 1
     }
     return [sum, used]
 }
 """,
 explain="""`continue` jumps to the next iteration; `break` leaves the loop. A `guard … else { continue }` keeps the happy path unindented.""",
 hints=("Two loop-control keywords: one skips an item, one stops the loop.","Check for `\"END\"` first (break), then `guard let value = Int(reading), value >= 0 else { continue }`.","Accumulate `sum += value; used += 1` after the guard."),
 tests=[({'readings':['4','x','-2','6','END','9']},[10,2]), {'readings':[]}, {'readings':['END','1']}, {'readings':['0','0']}]))
P.append(dict(id='predict-ranges', title='Predict: Range Operators', topic='Ranges', mode='predict', concepts=['half-open-range','stride'], docs=[('Basic Operators — Range Operators', BO)],
 statement="Predict the output.",
 snippet="""
 let names = ["Ana", "Bo", "Cy", "Di", "Ed"]
 print(names[1...3])
 print(names[..<2], names[3...])
 print(Array(1..<1), (1...3).count, (0..<10).contains(10))
 print(Array(stride(from: 0, to: 10, by: 4)), Array(stride(from: 3, through: 0, by: -1)))
 print((1...5).reversed().map { $0 * $0 })
 """,
 explain="""`a...b` includes `b`, `a..<b` excludes it, and one-sided ranges run to the end or from the start. Slicing an array gives an `ArraySlice`, which prints like an array.""",
 hints=("`...` includes the upper bound; `..<` stops before it.","`1..<1` is empty; `(0..<10).contains(10)` is false.","Line 1 prints `[\"Bo\", \"Cy\", \"Di\"]`.")))
P.append(dict(id='switch-strings', title='switch on Strings', topic='Switch', concepts=['switch-statement'], docs=[('Control Flow — Switch', CF)],
 sig='func weatherAdvice(_ forecasts: [String]) -> [String]',
 statement="""Map each forecast to advice with a `switch` on the lowercased string: `"sun"` → `"sunscreen"`, `"rain"` or `"drizzle"` → `"umbrella"`, `"snow"` → `"boots"`, anything starting with `"storm"` → `"stay in"`, else `"enjoy"`.""",
 solution="""
 func weatherAdvice(_ forecasts: [String]) -> [String] {
     forecasts.map { forecast in
         switch forecast.lowercased() {
         case "sun": "sunscreen"
         case "rain", "drizzle": "umbrella"
         case "snow": "boots"
         case let f where f.hasPrefix("storm"): "stay in"
         default: "enjoy"
         }
     }
 }
 """,
 explain="""Swift can `switch` on strings directly (unlike C). `case let f where …` binds the value and adds a condition. `default` is required because strings are open-ended.""",
 hints=("`switch` works on `String` values, and a case can list several strings.","Lowercase first; use `case let f where f.hasPrefix(\"storm\")` for prefixes.","`case \"rain\", \"drizzle\": \"umbrella\"`."),
 tests=[({'forecasts':['Sun','drizzle','Stormy','fog']},['sunscreen','umbrella','stay in','enjoy']), {'forecasts':[]}, {'forecasts':['SNOW','rain','storm']}]))
P.append(dict(id='rounding-doubles', title='Rounding Doubles', topic='Numbers', concepts=['float-vs-double','fundamental-types'], docs=[('Double', 'https://developer.apple.com/documentation/swift/double')],
 sig='func roundings(_ value: Double) -> [Double]',
 statement="""Return `[rounded(), rounded(.down), rounded(.up), rounded(.towardZero), value rounded to 2 decimal places]` for `value`. For two decimals, multiply by 100, round, divide by 100.""",
 compare='float:1e-9',
 solution="""
 func roundings(_ value: Double) -> [Double] {
     [value.rounded(), value.rounded(.down), value.rounded(.up), value.rounded(.towardZero), (value * 100).rounded() / 100]
 }
 """,
 explain="""`rounded(_:)` takes a `FloatingPointRoundingRule`; plain `rounded()` rounds halves away from zero (`-2.5 → -3`). `.down` is floor, `.up` is ceiling, `.towardZero` truncates.""",
 hints=("`Double` has a `rounded(_:)` method with different rounding rules.","The rules are `.down`, `.up` and `.towardZero`; plain `rounded()` rounds halves away from zero.","Two decimals: `(value * 100).rounded() / 100`."),
 tests=[({'value':2.5},[3,2,3,2,2.5]), ({'value':-2.567},[-3,-3,-2,-2,-2.57]), {'value':0}, {'value':1.005}, {'value':-0.5}]))
P.append(dict(id='character-properties', title='Character Properties: Password Strength', topic='Strings', concepts=['strings-are-collections'], docs=[('Character', 'https://developer.apple.com/documentation/swift/character')],
 sig='func strength(_ password: String) -> String',
 statement="""Score a password: +1 each for length ≥ 8, containing an uppercase letter, a lowercase letter, a digit, and a character that's none of those (symbol). 0–2 → `"weak"`, 3–4 → `"medium"`, 5 → `"strong"`. Use `Character` properties (`isUppercase`, `isNumber`…) and `contains(where:)`.""",
 solution="""
 func strength(_ password: String) -> String {
     let checks = [
         password.count >= 8,
         password.contains(where: \\.isUppercase),
         password.contains(where: \\.isLowercase),
         password.contains(where: \\.isNumber),
         password.contains { !$0.isLetter && !$0.isNumber },
     ]
     switch checks.filter { $0 }.count {
     case 0...2: return "weak"
     case 3...4: return "medium"
     default: return "strong"
     }
 }
 """,
 explain="""`contains(where:)` short-circuits at the first match. Key paths like `\\.isUppercase` can be passed where a `(Character) -> Bool` is expected.""",
 hints=("`Character` has properties such as `isUppercase`, `isLowercase`, `isNumber` and `isLetter`.","Build an array of five `Bool` checks with `contains(where:)` and count the `true`s.","`password.contains(where: \\.isUppercase)` — then switch on the count with ranges."),
 tests=[({'password':'abc'},'weak'), ({'password':'Passw0rd!'},'strong'), {'password':'password123'}, {'password':''}, {'password':'ÅBCdefgh'}]))
P.append(dict(id='nested-collections', title='Nested Collections: Class Roster', topic='Collections', diff='medium', concepts=['dictionary-basics','array-basics'], docs=[('Collection Types', CT)],
 sig='func roster(_ enrolments: [[String]]) -> [String]',
 statement="""Each enrolment is `[className, student]`. Build `[String: [String]]` (class → students, no duplicates, alphabetical) and return lines `"<class>: <students joined by ', '>"` sorted by class name, followed by `"largest: <class>"` (the class with most students; ties → alphabetically first; `"none"` if empty).""",
 solution="""
 func roster(_ enrolments: [[String]]) -> [String] {
     var classes: [String: Set<String>] = [:]
     for e in enrolments { classes[e[0], default: []].insert(e[1]) }
     let sorted = classes.map { (name: $0.key, students: $0.value.sorted()) }.sorted { $0.name < $1.name }
     var lines = sorted.map { "\\($0.name): \\($0.students.joined(separator: ", "))" }
     let largest = sorted.min { ($1.students.count, $0.name) < ($0.students.count, $1.name) }
     lines.append("largest: \\(largest?.name ?? "none")")
     return lines
 }
 """,
 explain="""A dictionary of sets de-duplicates for free; `default: []` creates the inner set on first use. Converting to sorted arrays at the end makes the output deterministic.""",
 hints=("Nest collections: a dictionary whose values are sets gives dedupe for free.","`classes[name, default: []].insert(student)`, then sort keys and each set when printing.","Largest with ties: compare `(count, name)` tuples with the name ascending."),
 tests=[({'enrolments':[['math','ana'],['art','bo'],['math','cy'],['math','ana']]},['art: bo','math: ana, cy','largest: math']), {'enrolments':[]}, {'enrolments':[['b','x'],['a','y']]}]))
P.append(dict(id='word-stats-stdio', title='Word Statistics (stdin)', topic='Standard I/O', mode='stdio', concepts=['strings-are-collections','dictionary-basics'], docs=[('Strings and Characters', SC)],
 statement="""Read all of stdin. Print three lines:
 1. `words: <n>` — whitespace-separated words
 2. `longest: <word>` — the longest word (first one on ties; `-` if none)
 3. `top: <letter>` — the most frequent **letter** (case-insensitive; alphabetically first on ties; `-` if none)""",
 starter="var text = \"\"\nwhile let line = readLine() { text += line + \"\\n\" }\n",
 solution="""
 var text = ""
 while let line = readLine() { text += line + "\\n" }
 let words = text.split(whereSeparator: \\.isWhitespace)
 print("words: \\(words.count)")
 let longest = words.reduce(nil as Substring?) { best, w in (best == nil || w.count > best!.count) ? w : best }
 print("longest: \\(longest.map(String.init) ?? "-")")
 var counts: [Character: Int] = [:]
 for ch in text.lowercased() where ch.isLetter { counts[ch, default: 0] += 1 }
 let top = counts.min { ($1.value, $0.key) < ($0.value, $1.key) }
 print("top: \\(top.map { String($0.key) } ?? "-")")
 """,
 explain="""`split(whereSeparator: \\.isWhitespace)` handles spaces, tabs and newlines. Tie-breaking with tuples keeps output deterministic even though dictionaries are unordered.""",
 hints=("Read everything first, then split on whitespace.","Track the longest word with a strict `>` so the first one wins ties; count letters in a dictionary.","Pick the top letter with `counts.min { ($1.value, $0.key) < ($0.value, $1.key) }`."),
 tests=['the quick brown fox\njumps over the lazy dog\n','', 'aa bb\n', 'Hello, World!\n'], hidden=1))
P.append(dict(id='functions-returning-tuples', title='Returning Multiple Values', topic='Functions', concepts=['tuples','functions-basics'], docs=[('Functions — Functions with Multiple Return Values', FN)],
 sig='func stats(_ values: [Double]) -> [Double]',
 statement="""Write `func summary(_ values: [Double]) -> (mean: Double, median: Double, range: Double)?` returning `nil` for an empty array. `stats` returns `[mean, median, range]` or `[]` — destructure the tuple with `let (mean, median, range) = …`.""",
 compare='float:1e-9',
 solution="""
 func summary(_ values: [Double]) -> (mean: Double, median: Double, range: Double)? {
     guard !values.isEmpty else { return nil }
     let s = values.sorted()
     let mid = s.count / 2
     let median = s.count.isMultiple(of: 2) ? (s[mid - 1] + s[mid]) / 2 : s[mid]
     return (s.reduce(0, +) / Double(s.count), median, s.last! - s.first!)
 }

 func stats(_ values: [Double]) -> [Double] {
     guard let (mean, median, range) = summary(values) else { return [] }
     return [mean, median, range]
 }
 """,
 explain="""Functions return several values as a (labelled) tuple; `guard let (a, b, c) = optionalTuple` unwraps and destructures at once. For an even count the median averages the two middle values.""",
 hints=("A tuple return lets one function produce several values; make it optional for the empty case.","Sort once; the median is the middle element (or the average of the two middle ones).","`guard let (mean, median, range) = summary(values) else { return [] }`."),
 tests=[({'values':[3,1,2]},[2,2,2]), ({'values':[]},[]), {'values':[4,1,3,2]}, {'values':[-5.5]}]))
P.append(dict(id='predict-shadowing', title='Predict: Shadowing in if let & Scopes', topic='Optionals', mode='predict', concepts=['optional-binding','guard'], docs=[('The Basics — Optional Binding', TB)],
 statement="Predict the output. Which `name` does each `print` see?",
 snippet="""
 let name: String? = "Ana"
 if let name {
     print(name, type(of: name))
 }
 print(name ?? "none", type(of: name))
 let count = 3
 do {
     let count = count * 2
     print(count)
 }
 print(count)
 func greet(_ name: String?) {
     guard let name else { print("no name"); return }
     print("hi \\(name)")
 }
 greet(nil)
 greet(name)
 """,
 explain="""`if let name` creates a **new**, non-optional constant that shadows the outer optional inside the braces. An inner `let count` in a nested scope shadows the outer one until the scope ends.""",
 hints=("Inside `if let name { }` there is a second, unwrapped `name`.","`type(of:)` shows `String` inside the `if let` and `Optional<String>` outside.","The `do` block prints 6; after it, `count` is 3 again.")))
P.append(dict(id='temperature-table-stdio', title='Temperature Table (stdin)', topic='Standard I/O', mode='stdio', concepts=['stride','string-interpolation'], docs=[('Control Flow', CF)],
 statement="""Input: three integers `from to step` on one line. Print a Celsius → Fahrenheit table from `from` to `to` inclusive (step may be negative), one row per line formatted `"<C>°C = <F>°F"`, with F rounded to the nearest integer.""",
 starter="let p = (readLine() ?? \"\").split(separator: \" \").compactMap { Int($0) }\n",
 solution="""
 let p = (readLine() ?? "").split(separator: " ").compactMap { Int($0) }
 for c in stride(from: p[0], through: p[1], by: p[2]) {
     let f = (Double(c) * 9 / 5 + 32).rounded()
     print("\\(c)°C = \\(Int(f))°F")
 }
 """,
 explain="""`stride(from:through:by:)` handles negative steps; if the direction doesn't match, it's simply empty.""",
 hints=("`stride` works with negative steps too.","Convert to `Double` before `* 9 / 5`, then round.","`print(\"\\(c)°C = \\(Int(f))°F\")`."),
 tests=['0 100 25\n','30 -10 -20\n','5 0 1\n'], hidden=1))
P.append(dict(id='nil-coalescing-chains', title='Defaults with ?? and Optional Arrays', topic='Optionals', concepts=['nil-coalescing','optional-chaining'], docs=[('Basic Operators — Nil-Coalescing Operator', BO)],
 sig='func profileSummary(nickname: String?, name: String?, tags: [String]?) -> String',
 statement="""Return `"<display> [<tagCount>] <firstTag>"` where `display` is the nickname, else the name, else `"Anonymous"`; `tagCount` is `tags?.count ?? 0`; `firstTag` is the first tag uppercased, or `"-"`.""",
 solution="""
 func profileSummary(nickname: String?, name: String?, tags: [String]?) -> String {
     let display = nickname ?? name ?? "Anonymous"
     let count = tags?.count ?? 0
     let first = tags?.first?.uppercased() ?? "-"
     return "\\(display) [\\(count)] \\(first)"
 }
 """,
 explain="""`??` chains fall through left to right. `tags?.first?.uppercased()` short-circuits at either optional and yields one `String?`.""",
 hints=("`??` can chain several fallbacks.","`tags?.count ?? 0` handles a missing array; `tags?.first?.uppercased()` handles a missing or empty one.","`nickname ?? name ?? \"Anonymous\"`."),
 tests=[({'nickname':None,'name':'Ana','tags':['swift','ios']},'Ana [2] SWIFT'), {'nickname':'ace','name':'Ana','tags':None}, {'nickname':None,'name':None,'tags':[]}]))
P.append(dict(id='variadic-join', title='Variadic Parameters: Build a Path', topic='Functions', concepts=['variadic','default-params'], docs=[('Functions — Variadic Parameters', FN)],
 sig='func paths(_ parts: [[String]]) -> [String]',
 statement="""Write `func joinPath(_ components: String..., separator: String = "/") -> String` that trims `/` from both ends of every component, drops empty ones, and joins them with the separator, starting with the separator. `paths` calls `joinPath` via an array-taking helper for each group, then also appends `joinPath("a", "b", separator: "::")` to prove the variadic form works.""",
 solution="""
 func joinPath(components: [String], separator: String = "/") -> String {
     let cleaned = components
         .map { $0.trimmingCharacters(in: CharacterSet(charactersIn: "/")) }
         .filter { !$0.isEmpty }
     return separator + cleaned.joined(separator: separator)
 }

 func joinPath(_ components: String..., separator: String = "/") -> String {
     joinPath(components: components, separator: separator)
 }

 import Foundation

 func paths(_ parts: [[String]]) -> [String] {
     parts.map { joinPath(components: $0) } + [joinPath("a", "b", separator: "::")]
 }
 """,
 explain="""A variadic `String...` arrives as `[String]`. Because you can't forward an array to a variadic parameter, the real work lives in an array-based overload. Default arguments can follow variadics.""",
 hints=("Inside the function, a variadic parameter is an ordinary array.","Put the logic in a `components: [String]` overload and have the variadic one forward to it.","Trim with `trimmingCharacters(in: CharacterSet(charactersIn: \"/\"))` (Foundation)."),
 tests=[({'parts':[['/usr/','local','bin/']]},['/usr/local/bin','::a::b']), {'parts':[]}, {'parts':[['','/'],['x']]}]))
P.append(dict(id='enum-methods-state', title='Enums with Methods: Order Status', topic='Enums', diff='medium', concepts=['enums','mutating','switch-statement'], docs=[('Enumerations', EN)],
 sig='func orderTimeline(_ events: [String]) -> [String]',
 statement="""Model `enum OrderStatus { case placed, paid, shipped, delivered, cancelled }` with a `mutating func handle(_ event: String) -> Bool` implementing the rules:
 - `pay`: placed → paid · `ship`: paid → shipped · `deliver`: shipped → delivered
 - `cancel`: placed or paid → cancelled
 - anything else is rejected (status unchanged, returns `false`)

 Return `"<event>: <status>"` or `"<event>: rejected"` for each event, starting from `.placed`.""",
 solution="""
 enum OrderStatus {
     case placed, paid, shipped, delivered, cancelled

     mutating func handle(_ event: String) -> Bool {
         switch (self, event) {
         case (.placed, "pay"): self = .paid
         case (.paid, "ship"): self = .shipped
         case (.shipped, "deliver"): self = .delivered
         case (.placed, "cancel"), (.paid, "cancel"): self = .cancelled
         default: return false
         }
         return true
     }
 }

 func orderTimeline(_ events: [String]) -> [String] {
     var status = OrderStatus.placed
     return events.map { event in
         status.handle(event) ? "\\(event): \\(status)" : "\\(event): rejected"
     }
 }
 """,
 explain="""Switching on a `(state, event)` tuple is a compact state machine. The enum owns its transition rules, so invalid transitions are impossible to express by accident.""",
 hints=("A state machine is an enum plus a method that decides the next state.","Switch on the tuple `(self, event)` and assign `self = .next` for valid transitions.","`case (.placed, \"cancel\"), (.paid, \"cancel\"): self = .cancelled`."),
 tests=[({'events':['pay','ship','cancel','deliver']},['pay: paid','ship: shipped','cancel: rejected','deliver: delivered']), {'events':[]}, {'events':['cancel','pay']}, {'events':['ship','pay','pay']}]))
P.append(dict(id='predict-integer-division', title='Predict: Integer vs Floating Division', topic='Numbers', mode='predict', concepts=['fundamental-types','float-vs-double','integer-overflow'], docs=[('Basic Operators — Arithmetic Operators', BO)],
 statement="Predict the output.",
 snippet="""
 print(7 / 2, 7 % 2, -7 / 2, -7 % 2)
 print(7.0 / 2, Double(7) / 2, 7 / 2.0)
 let a = 10, b = 4
 print(Double(a) / Double(b), Double(a / b))
 print(Int(3.99), Int(-3.99), Int((3.5).rounded()))
 print(Int.max, Int8.max, UInt8.max)
 print(0.1 + 0.2 == 0.3, abs(0.1 + 0.2 - 0.3) < 1e-9)
 """,
 explain="""Integer division truncates toward zero and `%` keeps the sign of the dividend. Converting `Double → Int` truncates too. A literal like `7.0 / 2` is all-`Double`, but `Double(a / b)` divides as integers first.""",
 hints=("Integer `/` truncates toward zero; `%` takes the sign of the left operand.","`Double(a / b)` does integer division **before** converting.","First line: `3 1 -3 -1`.")))
write_all(P, 'beginner', 800)
