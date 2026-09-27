import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CS='LanguageGuide/ClassesAndStructures'; PR='LanguageGuide/Properties'; IN='LanguageGuide/Initialization'; DE='LanguageGuide/Deinitialization'; NT='LanguageGuide/NestedTypes'; CT='LanguageGuide/CollectionTypes'; CF='LanguageGuide/ControlFlow'; PT='LanguageGuide/Protocols'; TB='LanguageGuide/TheBasics'; OC='LanguageGuide/OptionalChaining'; SC='LanguageGuide/StringsAndCharacters'
P=[]
P.append(dict(id='predict-for-var-copy', title='Predict: Mutating Structs in a Loop', topic='Structs', mode='predict', notes='21', concepts=['value-vs-reference','for-in','mutating'], docs=[('Structures and Classes', CS)],
 statement="Predict the output. Does changing the loop variable change the array?",
 snippet="""
 struct Player { var score: Int }
 final class Box { var score: Int; init(_ s: Int) { score = s } }

 var players = [Player(score: 1), Player(score: 2)]
 for var p in players { p.score *= 10 }
 print(players.map(\\.score))

 for i in players.indices { players[i].score *= 10 }
 print(players.map(\\.score))

 let boxes = [Box(1), Box(2)]
 for b in boxes { b.score *= 10 }
 print(boxes.map(\\.score))
 """,
 explain="""`for var p in players` gives you a **copy** of each struct, so the array is unchanged. Mutating through the index (`players[i]`) changes the array's own element. With a class, the loop constant is a reference to the shared object — even a `let` loop variable can mutate it."""))
P.append(dict(id='predict-observers-init', title='Predict: Observers During init', topic='Structs', mode='predict', notes='21', concepts=['property-observers','initializers'], docs=[('Properties — Property Observers', PR)],
 statement="Predict the output. When do `willSet`/`didSet` fire — and when don't they?",
 snippet="""
 struct Thermostat {
     var target: Int {
         willSet { print("will", target, "->", newValue) }
         didSet { print("did", oldValue, "->", target) }
     }
     init(target: Int) {
         self.target = target
         print("init done")
     }
     mutating func bump() { target += 1 }
 }

 var t = Thermostat(target: 20)
 t.target = 22
 t.bump()
 let same = t.target
 t.target = same
 """,
 explain="""Observers **don't** fire when a type sets its own property during `init` — so nothing is printed before `init done`. After that, every assignment triggers them, including through `mutating` methods and even when assigning the **same** value. (Writing `t.target = t.target` directly is a compile *error* — "assigning a property to itself" — hence the `let same`.)"""))
P.append(dict(id='predict-lazy-order', title='Predict: lazy Initialisation Order', topic='Structs', mode='predict', notes='21', concepts=['lazy-properties','lazy-vs-computed','computed-vs-closure-property'], docs=[('Properties — Lazy Stored Properties', PR)],
 statement="Predict the output — note when each closure body actually runs.",
 snippet="""
 func log(_ s: String) -> Int { print("computing", s); return s.count }

 struct Report {
     let eager: Int = log("eager")
     lazy var deferred: Int = log("lazy")
     var computed: Int { log("computed") }
 }

 print("start")
 var r = Report()
 print("created")
 print(r.deferred)
 print(r.deferred)
 print(r.computed)
 print(r.computed)
 """,
 explain="""A stored property's default runs during initialisation; a `lazy var` runs **once**, on first access, then stores the result; a computed property runs **every** time. `lazy` requires `var` (and a mutable instance), because first access mutates storage."""))
P.append(dict(id='predict-deinit-order', title='Predict: When deinit Runs', topic='Classes & inheritance', mode='predict', notes='22', concepts=['deinit','arc','strong-reference'], docs=[('Deinitialization', DE)],
 statement="Predict the output. Track every strong reference to each object.",
 snippet="""
 final class Node {
     let name: String
     init(_ name: String) { self.name = name; print("init", name) }
     deinit { print("deinit", name) }
 }

 var a: Node? = Node("A")
 var b = a
 a = nil
 print("a released")
 b = Node("B")
 print("b reassigned")
 do {
     let c = Node("C")
     _ = c
     print("leaving scope")
 }
 b = nil
 print("end")
 """,
 explain="""`a = nil` doesn't free "A" because `b` still holds it; reassigning `b` drops the last reference, and "A" is deinitialised **immediately** — before `b reassigned` prints. "C" dies at the end of its `do` scope. ARC is deterministic: no collector, no delay."""))
P.append(dict(id='predict-static-lazy', title='Predict: static let Is Lazy', topic='Structs', mode='predict', notes='21', concepts=['static-properties','singleton','lazy-properties'], docs=[('Properties — Type Properties', PR)],
 statement="Predict the output. When is each `static let` initialised?",
 snippet="""
 func make(_ label: String) -> String { print("making", label); return label }

 enum Config {
     static let apiURL = make("apiURL")
     static let timeout = make("timeout")
 }

 print("program start")
 print(Config.timeout)
 print(Config.timeout)
 print(Config.apiURL)
 """,
 explain="""Type properties (`static let`) and globals are initialised **lazily** on first access, exactly once, and thread-safely — which is why `static let shared = …` is the canonical singleton. Accessing `timeout` doesn't initialise `apiURL`."""))
P.append(dict(id='predict-optional-chaining-assign', title='Predict: Assigning Through Optional Chains', topic='Optionals', mode='predict', notes='25', concepts=['optional-chaining','dictionary-basics'], docs=[('Optional Chaining', OC)],
 statement="Predict the output. What does an assignment through `?.` return?",
 snippet="""
 final class Room { var name = "lobby" }
 final class House { var room: Room? }

 let house = House()
 let r1: Void? = (house.room?.name = "kitchen")
 print(r1 == nil ? "not assigned" : "assigned")
 house.room = Room()
 let r2: Void? = (house.room?.name = "kitchen")
 print(r2 == nil ? "not assigned" : "assigned", house.room?.name ?? "-")

 var scores = ["ana": [1, 2]]
 scores["ana"]?.append(3)
 scores["bo"]?.append(9)
 print(scores["ana"]!, scores["bo"] as Any)
 """,
 explain="""An assignment through an optional chain evaluates to `Void?` — `nil` if the chain broke, telling you whether it happened. `dict[key]?.append(x)` mutates **in place** only if the key exists; it never inserts."""))
P.append(dict(id='predict-set-dictionary-order', title='Predict: Only What Is Deterministic', topic='Collections', mode='predict', notes='8', concepts=['set-vs-array','dictionary-basics'], docs=[('Collection Types', CT)],
 statement="""Sets and dictionaries are **unordered** and their iteration order changes between runs — so this snippet only prints things that are deterministic. Predict them.""",
 snippet="""
 let a: Set = [3, 1, 4, 1, 5, 9, 2, 6]
 let b: Set = [2, 7, 1, 8, 2, 8]
 print(a.count, b.count)
 print(a.intersection(b).sorted())
 print(a.isSuperset(of: [1, 9]), b.isDisjoint(with: [3, 4]))
 var counts: [Character: Int] = [:]
 for ch in "mississippi" { counts[ch, default: 0] += 1 }
 print(counts.sorted { $0.key < $1.key }.map { "\\($0.key)\\($0.value)" }.joined())
 print(counts["z"] as Any, counts["s", default: 0])
 """,
 explain="""Duplicates vanish in a `Set` literal. Anything you print from a set or dictionary should be `sorted()` first — otherwise the output (and your tests) will flicker between runs because hashing is randomly seeded per process."""))
P.append(dict(id='predict-string-indices', title='Predict: Strings Are Not Arrays', topic='Strings', mode='predict', notes='2', concepts=['strings-are-collections','string-equality'], docs=[('Strings and Characters', SC)],
 statement="Predict the output.",
 snippet="""
 let flag = "🇮🇳"
 let word = "cafe\\u{301}"
 print(flag.count, flag.unicodeScalars.count, flag.utf8.count)
 print(word, word.count, word == "café")
 let s = "Hello, Swift"
 let i = s.firstIndex(of: ",")!
 print(s[..<i], s[s.index(after: i)...].trimmingPrefix(" "))
 print(s.prefix(4), s.suffix(3), s.dropFirst(7).uppercased())
 print(String(s.reversed()))
 let words: [Substring] = s.split(separator: " ")
 print(words.map { $0.count })
 """,
 explain="""A flag emoji is one `Character` built from two regional-indicator scalars (8 UTF-8 bytes). `"e"` + combining accent is **canonically equivalent** to `"é"`, so `==` is true and `count` is 4. Slicing uses `String.Index`, and `prefix`/`suffix`/`dropFirst` return `Substring`s."""))
P.append(dict(id='predict-switch-where-fallthrough', title='Predict: switch Subtleties', topic='Switch', mode='predict', notes='12', concepts=['switch-statement','fallthrough','where-clause'], docs=[('Control Flow — Switch', CF)],
 statement="Predict the output.",
 snippet="""
 func check(_ x: Int) -> String {
     var out = ""
     switch x {
     case let n where n < 0:
         out += "negative "
         fallthrough
     case 0:
         out += "small "
     case 1...9:
         out += "digit "
     case 10, 20, 30:
         out += "round "
         fallthrough
     default:
         out += "other"
     }
     return out
 }
 for x in [-5, 0, 7, 20, 99] { print(x, "->", check(x)) }
 """,
 explain="""`fallthrough` runs the **next** case's body without checking its pattern — so `-5` also gets `"small"` and `20` also gets `"other"`. Without `fallthrough`, exactly one case runs."""))
P.append(dict(id='nested-types-cards', title='Nested Types: A Deck of Cards', topic='Enums', notes='9', diff='medium', concepts=['enums','case-iterable','comparable','nested-types' if False else 'enums'], docs=[('Nested Types', NT)],
 sig='func deckSummary(_ draws: [Int]) -> [String]',
 statement="""Build `struct Card` with **nested** `enum Suit: Character, CaseIterable { case spades = "♠", hearts = "♥", diamonds = "♦", clubs = "♣" }` and `enum Rank: Int, CaseIterable, Comparable { case two = 2, …, jack, queen, king, ace }` (with a `symbol` computed property: 2–10 as digits, J Q K A).

 `static var fullDeck: [Card]` iterates suits then ranks. For each index in `draws`, return the card as `"<symbol><suit>"` (e.g. `"A♠"`), then append `"highest: <card>"` for the highest rank among the draws (first one on ties; `"none"` if no draws).""",
 solution="""
 struct Card {
     enum Suit: Character, CaseIterable {
         case spades = "♠", hearts = "♥", diamonds = "♦", clubs = "♣"
     }

     enum Rank: Int, CaseIterable, Comparable {
         case two = 2, three, four, five, six, seven, eight, nine, ten, jack, queen, king, ace

         var symbol: String {
             switch self {
             case .jack: "J"
             case .queen: "Q"
             case .king: "K"
             case .ace: "A"
             default: String(rawValue)
             }
         }

         static func < (a: Rank, b: Rank) -> Bool { a.rawValue < b.rawValue }
     }

     let rank: Rank
     let suit: Suit

     var name: String { "\\(rank.symbol)\\(suit.rawValue)" }

     static var fullDeck: [Card] {
         Suit.allCases.flatMap { suit in Rank.allCases.map { Card(rank: $0, suit: suit) } }
     }
 }

 func deckSummary(_ draws: [Int]) -> [String] {
     let deck = Card.fullDeck
     let hand = draws.map { deck[$0 % deck.count] }
     let best = hand.max { $0.rank < $1.rank }
     return hand.map(\\.name) + ["highest: \\(best?.name ?? "none")"]
 }
 """,
 explain="""Nesting `Suit` and `Rank` inside `Card` scopes their names (`Card.Suit`) to where they belong. Raw values can be `Character`s. `max(by:)` returns the **last** maximal element with a strict `<`… except the standard library guarantees the *first* for `max(by:)`? It returns the last — check the output to see which you got, and why a tie-break rule matters.""",
 tests=[({'draws':[12,0,25]},None), {'draws':[]}, {'draws':[51,50,13]}, {'draws':[12,25,38]}]))
P[-1]['tests'][0] = {'draws':[12,0,25]}
P[-1]['statement'] = P[-1]['statement'].replace("(first one on ties; `\"none\"` if no draws)", "(if several share the highest rank, report whichever `max(by:)` returns — run it and see; `\"none\"` if no draws)")
P[-1]['explain'] = """Nesting `Suit` and `Rank` inside `Card` scopes their names (`Card.Suit`) to where they belong. Raw values can be `Character`s. `max(by:)` with ties returns the **last** of the equal maximal elements — a detail worth checking whenever ties matter, and a reason to make comparisons total (e.g. break ties by suit)."""
P.append(dict(id='custom-string-convertible', title='CustomStringConvertible & debugDescription', topic='Protocols', notes='23', diff='easy', concepts=['protocols','print-vs-debugprint','string-interpolation'], docs=[('Protocols', PT)],
 sig='func describeMoney(_ cents: [Int]) -> [String]',
 statement="""`struct Money: CustomStringConvertible, CustomDebugStringConvertible` stores `cents`. `description` is `"$12.05"` (negative as `"-$0.50"`); `debugDescription` is `"Money(cents: 1205)"`.

 Return, for each amount, `"\\(money)"` and `String(reflecting: money)` — two entries per amount.""",
 solution="""
 struct Money: CustomStringConvertible, CustomDebugStringConvertible {
     let cents: Int

     var description: String {
         let sign = cents < 0 ? "-" : ""
         let abs = cents.magnitude
         let fraction = abs % 100
         return "\\(sign)$\\(abs / 100).\\(fraction < 10 ? "0" : "")\\(fraction)"
     }

     var debugDescription: String { "Money(cents: \\(cents))" }
 }

 func describeMoney(_ cents: [Int]) -> [String] {
     cents.flatMap { c -> [String] in
         let money = Money(cents: c)
         return ["\\(money)", String(reflecting: money)]
     }
 }
 """,
 explain="""Interpolation and `print` use `description`; `debugPrint`, `String(reflecting:)` and the debugger use `debugDescription`. Conforming makes your types log nicely everywhere.""",
 tests=[({'cents':[1205,-50]},['$12.05','Money(cents: 1205)','-$0.50','Money(cents: -50)']), {'cents':[]}, {'cents':[0,7,100]}]))
P.append(dict(id='for-case-optional', title='for case let x? — Iterate Non-nil Values', topic='Optionals', notes='25', diff='easy', concepts=['pattern-matching','optionals','compactmap-flatmap'], docs=[('Patterns — Optional Pattern','ReferenceManual/Patterns')],
 sig='func sumPresent(_ values: [Int?]) -> [Int]',
 statement="""Return `[sum of non-nil values using for case let x? in values, count of nils using if case .none, sum of values > 10 using for case let x? in values where x > 10]`.""",
 solution="""
 func sumPresent(_ values: [Int?]) -> [Int] {
     var total = 0
     for case let x? in values { total += x }
     var nils = 0
     for v in values { if case .none = v { nils += 1 } }
     var big = 0
     for case let x? in values where x > 10 { big += x }
     return [total, nils, big]
 }
 """,
 explain="""The **optional pattern** `x?` matches `.some(x)` and binds the payload — `for case let x? in` iterates only present values (like `compactMap`, but lazy and loop-shaped). `Optional` is just an enum, so `.none`/`.some` patterns work too.""",
 tests=[({'values':[1,None,20,None,3]},[24,2,20]), {'values':[]}, {'values':[None]}, {'values':[11,12]}]))
P.append(dict(id='builder-pattern-copy', title='Fluent Builders with Value Types', topic='Structs', notes='21', diff='medium', concepts=['value-semantics','self-vs-Self','mutating'], docs=[('Methods', 'LanguageGuide/Methods')],
 sig='func requestDemo(_ steps: [String]) -> [String]',
 statement="""`struct Request` has `method = "GET"`, `path = "/"`, `headers: [String: String] = [:]`. Add **non-mutating** fluent methods returning modified copies: `method(_:)`, `path(_:)`, `header(_:_:)`, each `-> Self`.

 Steps look like `"method POST"`, `"path /users"`, `"header Accept json"`. Start from `let base = Request()`, fold the steps with `reduce(base)`, and return `[base.summary, built.summary]` where `summary` = `"<METHOD> <path> <headers sorted as k=v joined by ;>"`.""",
 solution="""
 struct Request {
     var method = "GET"
     var path = "/"
     var headers: [String: String] = [:]

     func method(_ m: String) -> Self { var copy = self; copy.method = m; return copy }
     func path(_ p: String) -> Self { var copy = self; copy.path = p; return copy }
     func header(_ k: String, _ v: String) -> Self { var copy = self; copy.headers[k] = v; return copy }

     var summary: String {
         "\\(method) \\(path) " + headers.sorted { $0.key < $1.key }.map { "\\($0.key)=\\($0.value)" }.joined(separator: ";")
     }
 }

 func requestDemo(_ steps: [String]) -> [String] {
     let base = Request()
     let built = steps.reduce(base) { req, step in
         let p = step.split(separator: " ").map(String.init)
         switch (p.first, p.count) {
         case ("method", 2): return req.method(p[1])
         case ("path", 2): return req.path(p[1])
         case ("header", 3): return req.header(p[1], p[2])
         default: return req
         }
     }
     return [base.summary, built.summary]
 }
 """,
 explain="""With value types, a fluent API can return **modified copies** (`var copy = self`), so `base` is never changed — like SwiftUI modifiers. `Self` as a return type means "the type I'm declared in" and reads nicely in chains.""",
 tests=[({'steps':['method POST','path /users','header Accept json']},['GET / ','POST /users Accept=json']), {'steps':[]}, {'steps':['header b 2','header a 1','nonsense']}]))
P.append(dict(id='tuple-swap-fibonacci', title='Tuple Assignment: Fibonacci & GCD', topic='Tuples', notes='16', diff='easy', concepts=['tuples','control-flow'], docs=[('The Basics — Tuples', TB)],
 sig='func fibAndGcd(_ n: Int, _ a: Int, _ b: Int) -> [Int]',
 statement="""Return `[fib(n), gcd(a, b)]` where both loops update two variables **simultaneously** with tuple assignment — `(x, y) = (y, x + y)` — and no temporary variable. `fib(0) = 0`, `n ≤ 90`; `gcd` of non-negative numbers (`gcd(0, 0) = 0`).""",
 solution="""
 func fibAndGcd(_ n: Int, _ a: Int, _ b: Int) -> [Int] {
     var (x, y) = (0, 1)
     for _ in 0..<n { (x, y) = (y, x + y) }
     var (p, q) = (a, b)
     while q != 0 { (p, q) = (q, p % q) }
     return [x, p]
 }
 """,
 explain="""The right-hand tuple is fully evaluated **before** assignment, so `(x, y) = (y, x + y)` uses the old values of both. `var (x, y) = (0, 1)` declares two variables at once.""",
 tests=[({'n':10,'a':48,'b':18},[55,6]), {'n':0,'a':0,'b':0}, {'n':1,'a':17,'b':5}, {'n':90,'a':270,'b':192}]))
P.append(dict(id='dictionary-unique-keys', title='Building Dictionaries Safely', topic='Dictionaries', notes='7', diff='medium', concepts=['dictionary-basics','tuples'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func indexUsers(_ rows: [[String]]) -> [String: String]',
 statement="""Rows are `[id, name]`, and ids may repeat. `Dictionary(uniqueKeysWithValues:)` **crashes** on duplicate keys — so use `Dictionary(_:uniquingKeysWith:)` keeping the **last** name for each id, but join with `"|"` when the names differ (`"ann|anna"`) — keep first-then-later order.""",
 solution="""
 func indexUsers(_ rows: [[String]]) -> [String: String] {
     Dictionary(rows.map { ($0[0], $0[1]) }, uniquingKeysWith: { old, new in
         old.split(separator: "|").contains(Substring(new)) ? old : old + "|" + new
     })
 }
 """,
 explain="""`Dictionary(uniqueKeysWithValues:)` traps on duplicates (*Fatal error: Duplicate values for key*). The `uniquingKeysWith:` initialiser asks you how to merge — and `merge(_:uniquingKeysWith:)` does the same for existing dictionaries.""",
 tests=[({'rows':[['1','ann'],['2','bo'],['1','anna']]},{'1':'ann|anna','2':'bo'}), {'rows':[]}, {'rows':[['x','a'],['x','a'],['x','b'],['x','a']]}]))
P.append(dict(id='zip-enumerated', title='zip, enumerated & Parallel Arrays', topic='Arrays', notes='6', diff='easy', concepts=['for-in','tuples','array-basics'], docs=[('Collection Types', CT)],
 sig='func podium(_ names: [String], _ times: [Double]) -> [String]',
 statement="""`names[i]` finished in `times[i]` seconds (arrays may differ in length — extras are ignored). Return the top three as `"<place>. <name> (<time>s)"`, fastest first. Use `zip` to pair, `sorted`, `prefix(3)` and `enumerated()` for the place.""",
 solution="""
 func podium(_ names: [String], _ times: [Double]) -> [String] {
     zip(names, times)
         .sorted { $0.1 < $1.1 }
         .prefix(3)
         .enumerated()
         .map { "\\($0.offset + 1). \\($0.element.0) (\\($0.element.1)s)" }
 }
 """,
 explain="""`zip` stops at the shorter sequence, so mismatched lengths are safe. `enumerated()` offsets start at **0** — add 1 for human places. (Note `enumerated()` on a slice gives offsets, not the slice's indices.)""",
 tests=[({'names':['ana','bo','cy','di'],'times':[10.5,9.8,11.0,9.9]},['1. bo (9.8s)','2. di (9.9s)','3. ana (10.5s)']), {'names':[],'times':[]}, {'names':['solo','extra'],'times':[3.0]}]))
P.append(dict(id='stdio-bank-ledger', title='Bank Ledger (stdin)', topic='Error handling', mode='stdio', notes='19', diff='medium', concepts=['error-handling','do-catch' if False else 'multi-pattern-catch','guard'], docs=[('Error Handling', 'LanguageGuide/ErrorHandling')],
 statement="""Process commands from stdin against a balance starting at 0:
 - `deposit <n>`, `withdraw <n>` (n > 0 integer)

 Model failures with `enum LedgerError: Error { case badCommand(String), badAmount(String), insufficient(needed: Int) }` and a throwing `apply` function. For each line print `"ok <balance>"` or `"error: <description>"` where descriptions are `"unknown command <cmd>"`, `"bad amount <text>"`, `"need <n> more"`. Finish with `"final <balance>"`.""",
 starter="var balance = 0\n\nprint(\"final \\(balance)\")\n",
 solution="""
 enum LedgerError: Error {
     case badCommand(String)
     case badAmount(String)
     case insufficient(needed: Int)
 }

 func apply(_ line: String, to balance: inout Int) throws {
     let parts = line.split(separator: " ").map(String.init)
     guard parts.count == 2, ["deposit", "withdraw"].contains(parts[0]) else {
         throw LedgerError.badCommand(parts.first ?? "")
     }
     guard let amount = Int(parts[1]), amount > 0 else { throw LedgerError.badAmount(parts[1]) }
     if parts[0] == "deposit" {
         balance += amount
     } else {
         guard amount <= balance else { throw LedgerError.insufficient(needed: amount - balance) }
         balance -= amount
     }
 }

 var balance = 0
 while let line = readLine() {
     do {
         try apply(line, to: &balance)
         print("ok \\(balance)")
     } catch LedgerError.badCommand(let cmd) {
         print("error: unknown command \\(cmd)")
     } catch LedgerError.badAmount(let text) {
         print("error: bad amount \\(text)")
     } catch LedgerError.insufficient(let needed) {
         print("error: need \\(needed) more")
     } catch {
         print("error: \\(error)")
     }
 }
 print("final \\(balance)")
 """,
 explain="""Throwing functions keep validation logic out of the loop; `catch` patterns with bindings turn each error into a message. Top-level `main.swift` code needs a final bare `catch` because Swift can't prove the others exhaustive.""",
 tests=['deposit 100\nwithdraw 30\nwithdraw 100\nrefund 5\ndeposit -3\n', '', 'withdraw 1\ndeposit x\n'], hidden=1))
P.append(dict(id='protocol-default-args', title='Protocol Requirements with Defaults', topic='Protocols', notes='23', diff='medium', concepts=['protocols','protocol-extension','default-params'], docs=[('Protocols — Protocol Extensions', PT)],
 sig='func notify(_ channels: [String], message: String) -> [String]',
 statement="""Protocol requirements **can't** declare default argument values. Declare `protocol Notifier { func send(_ message: String, urgent: Bool) -> String }` and use a protocol extension to add the convenience `func send(_ message: String) -> String` that forwards with `urgent: false`.

 `EmailNotifier` returns `"email: <msg><!>"` and `SMSNotifier` returns `"sms: <MSG uppercased when urgent>"`. For each channel (`"email"`/`"sms"`), call both `send(message)` and `send(message, urgent: true)`.""",
 solution="""
 protocol Notifier {
     func send(_ message: String, urgent: Bool) -> String
 }

 extension Notifier {
     func send(_ message: String) -> String { send(message, urgent: false) }
 }

 struct EmailNotifier: Notifier {
     func send(_ message: String, urgent: Bool) -> String { "email: \\(message)\\(urgent ? "!" : "")" }
 }

 struct SMSNotifier: Notifier {
     func send(_ message: String, urgent: Bool) -> String { "sms: \\(urgent ? message.uppercased() : message)" }
 }

 func notify(_ channels: [String], message: String) -> [String] {
     channels.flatMap { ch -> [String] in
         let n: any Notifier = ch == "sms" ? SMSNotifier() : EmailNotifier()
         return [n.send(message), n.send(message, urgent: true)]
     }
 }
 """,
 explain="""Writing `func send(_ m: String, urgent: Bool = false)` in a protocol is an error (*default argument not permitted in a protocol method*). The extension overload is the standard workaround.""",
 tests=[({'channels':['email','sms'],'message':'hi'},['email: hi','email: hi!','sms: hi','sms: HI']), {'channels':[],'message':'x'}]))
P.append(dict(id='diag-protocol-default-arg', title='Diagnostic: No Default Args in Protocols', topic='Protocols', mode='diagnostic', notes='23', diff='easy', concepts=['protocols','default-params'], docs=[('Protocols — Method Requirements', PT)],
 statement="""Declare a protocol with a method requirement that has a **default argument value**, e.g. `func send(_ message: String, urgent: Bool = false)`. You pass when the compiler rejects it.""",
 starter="protocol Notifier {\n    func send(_ message: String, urgent: Bool)\n}\n",
 solution="protocol Notifier {\n    func send(_ message: String, urgent: Bool = false)\n}\n",
 explain="""*default argument not permitted in a protocol method*. Provide the convenience overload in a protocol extension instead (see *Protocol Requirements with Defaults*).""",
 tests=[{'name':'Default arg rejected','pattern':'default argument not permitted'}]))
P.append(dict(id='diag-weak-let', title='Diagnostic: weak Must Be an Optional var', topic='Memory management', mode='diagnostic', notes='22', diff='easy', concepts=['weak-unowned'], docs=[('ARC — Weak References','LanguageGuide/AutomaticReferenceCounting')],
 statement="""Inside a class, declare a property `weak let owner: Owner` (non-optional, `let`). You pass when the compiler explains why a weak reference can't be that.""",
 starter="final class Owner {}\n\nfinal class Pet {\n    weak var owner: Owner?\n}\n",
 solution="final class Owner {}\n\nfinal class Pet {\n    weak let owner: Owner\n    init(owner: Owner) { self.owner = owner }\n}\n",
 explain="""ARC sets weak references to `nil` when the object dies — so they must be **optional** (*'weak' variable should have optional type*). Since Swift 5.x, `weak let` of an optional type is allowed; a non-optional weak is never allowed.""",
 tests=[{'name':'weak needs optional','pattern':'weak'}]))
P.append(dict(id='queue-two-stacks', title='Design: Queue from Two Stacks', topic='Structs', notes='21', diff='medium', concepts=['mutating','generics','array-basics'], docs=[('Generics — Generic Types','LanguageGuide/Generics')],
 statement="""Implement `struct TwoStackQueue<Element>` with `mutating func enqueue(_:)`, `mutating func dequeue() -> Element?`, `var peek: Element?` (non-mutating!) and `var count`, using two arrays as stacks with **amortised O(1)** operations.

 The judge drives it with ops `enqueue <n>` / `dequeue` / `peek` / `count`.""",
 starter="""
 struct TwoStackQueue<Element> {
     mutating func enqueue(_ x: Element) {}
     mutating func dequeue() -> Element? { nil }
     var peek: Element? { nil }
     var count: Int { 0 }
 }
 """,
 solution="""
 struct TwoStackQueue<Element> {
     private var inbox: [Element] = []
     private var outbox: [Element] = []

     mutating func enqueue(_ x: Element) { inbox.append(x) }

     mutating func dequeue() -> Element? {
         if outbox.isEmpty {
             outbox = inbox.reversed()
             inbox.removeAll()
         }
         return outbox.popLast()
     }

     var peek: Element? { outbox.last ?? inbox.first }
     var count: Int { inbox.count + outbox.count }
 }
 """,
 harness="""
 struct __Input: Decodable { let ops: [String] }
 func __run(_ __i: __Input) async throws -> [Int?] {
     var q = TwoStackQueue<Int>()
     return __i.ops.map { op -> Int? in
         let parts = op.split(separator: " ")
         switch parts[0] {
         case "enqueue": q.enqueue(Int(parts[1])!); return nil
         case "dequeue": return q.dequeue()
         case "peek": return q.peek
         default: return q.count
         }
     }
 }
 """,
 explain="""Elements move from `inbox` to `outbox` only when `outbox` is empty, so each element is moved at most once — amortised O(1). `peek` can stay non-mutating by looking at `inbox.first` when `outbox` is empty.""",
 tests=[({'ops':['enqueue 1','enqueue 2','peek','dequeue','enqueue 3','count','dequeue','dequeue','dequeue']},[None,None,1,1,None,2,2,3,None]), {'ops':['dequeue','peek','count']}, {'ops':['enqueue 5','dequeue','enqueue 6','peek']}]))

write_all(P, 'intermediate', 500)
