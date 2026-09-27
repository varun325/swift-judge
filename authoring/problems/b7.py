import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
ARC='LanguageGuide/AutomaticReferenceCounting'; CC='LanguageGuide/Concurrency'; PR='LanguageGuide/Properties'; AT='ReferenceManual/Attributes'; MS='LanguageGuide/MemorySafety'; ST='ReferenceManual/Statements'; EH='LanguageGuide/ErrorHandling'
CODABLE='https://developer.apple.com/documentation/foundation/encoding-and-decoding-custom-types'
REGEX='https://developer.apple.com/documentation/swift/regex'
P=[]
# ---------- ARC & memory
P.append(dict(id='retain-cycle-parent-child', title='Break a Retain Cycle with weak', topic='Memory management', notes='22', diff='medium', concepts=['retain-cycle','weak-unowned','arc','deinit'], docs=[('ARC — Strong Reference Cycles Between Class Instances', ARC)],
 sig='func cycleDemo(_ childNames: [String]) -> [String]',
 statement="""`final class Parent` holds `var children: [Child]`; `final class Child` holds a back-reference `parent`. Both log `"deinit <name>"` in `deinit` (into a shared `Log`).

 Starter code leaks: nothing is ever deinitialised. Fix it so that when `cycleDemo`'s inner `do { }` scope ends, **every** object is freed. The log should end with `"end"`.""",
 starter="""
 final class Log { var lines: [String] = [] }

 final class Parent {
     let name: String, log: Log
     var children: [Child] = []
     init(_ name: String, log: Log) { self.name = name; self.log = log }
     deinit { log.lines.append("deinit \\(name)") }
 }

 final class Child {
     let name: String, log: Log
     var parent: Parent?
     init(_ name: String, log: Log) { self.name = name; self.log = log }
     deinit { log.lines.append("deinit \\(name)") }
 }

 func cycleDemo(_ childNames: [String]) -> [String] {
     let log = Log()
     do {
         let mom = Parent("mom", log: log)
         for n in childNames {
             let child = Child(n, log: log)
             child.parent = mom
             mom.children.append(child)
         }
     }
     log.lines.append("end")
     return log.lines
 }
 """,
 solution="""
 final class Log { var lines: [String] = [] }

 final class Parent {
     let name: String, log: Log
     var children: [Child] = []
     init(_ name: String, log: Log) { self.name = name; self.log = log }
     deinit { log.lines.append("deinit \\(name)") }
 }

 final class Child {
     let name: String, log: Log
     weak var parent: Parent?
     init(_ name: String, log: Log) { self.name = name; self.log = log }
     deinit { log.lines.append("deinit \\(name)") }
 }

 func cycleDemo(_ childNames: [String]) -> [String] {
     let log = Log()
     do {
         let mom = Parent("mom", log: log)
         for n in childNames {
             let child = Child(n, log: log)
             child.parent = mom
             mom.children.append(child)
         }
     }
     log.lines.append("end")
     return log.lines
 }
 """,
 explain="""Parent → child (strong) and child → parent (strong) keep each other's reference counts above zero forever. Making the **back-reference** `weak` breaks the cycle: when `mom` goes out of scope she's freed, which releases her children. `deinit` logging is the simplest leak detector.""",
 tests=[({'childNames':['kid']},['deinit mom','deinit kid','end']), {'childNames':[]}, {'childNames':['a','b','c']}]))
P.append(dict(id='closure-retain-cycle', title='[weak self] in Stored Closures', topic='Memory management', diff='medium', concepts=['closures-memory','capture-list','retain-cycle'], docs=[('ARC — Strong Reference Cycles for Closures', ARC)],
 sig='func timerDemo(ticks: Int) -> [String]',
 statement="""`final class Ticker` stores `var onTick: (() -> Void)?`. In `start()` it sets `onTick` to a closure that increments `self.count` and logs `"tick <count>"`. Starter captures `self` strongly — the ticker never deinits.

 Fix `start()` with a capture list so `timerDemo` logs `"deinit ticker"` before `"end"`. Keep the closure working: calling `onTick` `ticks` times must still log every tick.""",
 starter="""
 final class Log { var lines: [String] = [] }

 final class Ticker {
     var count = 0
     var onTick: (() -> Void)?
     let log: Log
     init(log: Log) { self.log = log }

     func start() {
         onTick = {
             self.count += 1
             self.log.lines.append("tick \\(self.count)")
         }
     }

     deinit { log.lines.append("deinit ticker") }
 }

 func timerDemo(ticks: Int) -> [String] {
     let log = Log()
     do {
         let ticker = Ticker(log: log)
         ticker.start()
         for _ in 0..<ticks { ticker.onTick?() }
     }
     log.lines.append("end")
     return log.lines
 }
 """,
 solution="""
 final class Log { var lines: [String] = [] }

 final class Ticker {
     var count = 0
     var onTick: (() -> Void)?
     let log: Log
     init(log: Log) { self.log = log }

     func start() {
         onTick = { [weak self] in
             guard let self else { return }
             count += 1
             log.lines.append("tick \\(count)")
         }
     }

     deinit { log.lines.append("deinit ticker") }
 }

 func timerDemo(ticks: Int) -> [String] {
     let log = Log()
     do {
         let ticker = Ticker(log: log)
         ticker.start()
         for _ in 0..<ticks { ticker.onTick?() }
     }
     log.lines.append("end")
     return log.lines
 }
 """,
 explain="""`self` → `onTick` closure → `self` is a cycle. `[weak self]` captures a weak optional reference; `guard let self` (Swift 5.8 shorthand) upgrades it for the closure body and allows implicit `self`. `[unowned self]` also works if the closure can never outlive the object.""",
 tests=[({'ticks':2},['tick 1','tick 2','deinit ticker','end']), {'ticks':0}, {'ticks':5}]))
P.append(dict(id='unowned-customer-card', title='unowned References', topic='Memory management', diff='medium', concepts=['weak-unowned','arc'], docs=[('ARC — Unowned References', ARC)],
 sig='func cardDemo(_ customers: [String], withCard: [Bool]) -> [String]',
 statement="""The Swift book's example: a `Customer` optionally owns a `CreditCard`, and every card **must** have a customer — so the card's reference is `unowned let customer: Customer` (non-optional, non-owning).

 For each customer create the objects inside a scope, log `"<card number> belongs to <name>"` if they have a card (card numbers start at 1000 and increase by 1 per card), and let them deallocate — both classes log `"deinit <name|card number>"`. Return the log.""",
 solution="""
 final class Log { var lines: [String] = [] }

 final class Customer {
     let name: String
     var card: CreditCard?
     let log: Log
     init(name: String, log: Log) { self.name = name; self.log = log }
     deinit { log.lines.append("deinit \\(name)") }
 }

 final class CreditCard {
     let number: Int
     unowned let customer: Customer
     let log: Log
     init(number: Int, customer: Customer, log: Log) { self.number = number; self.customer = customer; self.log = log }
     deinit { log.lines.append("deinit \\(number)") }
 }

 func cardDemo(_ customers: [String], withCard: [Bool]) -> [String] {
     let log = Log()
     var nextNumber = 1000
     for (name, hasCard) in zip(customers, withCard) {
         let customer = Customer(name: name, log: log)
         if hasCard {
             customer.card = CreditCard(number: nextNumber, customer: customer, log: log)
             nextNumber += 1
             if let card = customer.card { log.lines.append("\\(card.number) belongs to \\(card.customer.name)") }
         }
     }
     return log.lines
 }
 """,
 explain="""Use `unowned` when the other object has the **same or longer** lifetime — it's non-optional, so no unwrapping, but accessing it after deallocation traps. Use `weak` when the referent may disappear first. Here the customer owns the card, so the card can safely be unowned.""",
 tests=[({'customers':['ann','bo'],'withCard':[True,False]},['1000 belongs to ann','deinit ann','deinit 1000','deinit bo']), {'customers':[],'withCard':[]}, {'customers':['a','b'],'withCard':[True,True]}]))
P.append(dict(id='noncopyable-file-handle', title='~Copyable: Unique Ownership', topic='Memory management', diff='hard', concepts=['ownership','memory-safety','deinit'], docs=[('Declarations — Noncopyable types','ReferenceManual/Declarations'),('Swift Evolution SE-0390','https://github.com/swiftlang/swift-evolution/blob/main/proposals/0390-noncopyable-structs-and-enums.md')],
 sig='func ownershipDemo(_ writes: [String], closeEarly: Bool) -> [String]',
 statement="""Model a file handle that must have exactly **one owner**: `struct FileHandle: ~Copyable` with a `name`, a `Log`, a private `closed` flag and:
 - `mutating func write(_:)` — logs `"write <text>"`
 - **`consuming func close()`** — logs `"close <name>"` and marks itself closed; since it *consumes* `self`, the caller can't use the handle afterwards
 - `deinit` — logs `"auto-close <name>"` **only if** it wasn't closed explicitly

 Also write `func inspect(_ h: borrowing FileHandle) -> String` returning `"inspect <name>"`.

 In the demo: create the handle, `inspect` it (append to log), write each string, then call `close()` if `closeEarly`, else let it go out of scope. Log `"done"` last.""",
 solution="""
 final class Log { var lines: [String] = [] }

 struct FileHandle: ~Copyable {
     let name: String
     let log: Log
     private var closed = false

     init(name: String, log: Log) {
         self.name = name
         self.log = log
     }

     mutating func write(_ text: String) { log.lines.append("write \\(text)") }

     consuming func close() {
         log.lines.append("close \\(name)")
         closed = true
     }

     deinit {
         if !closed { log.lines.append("auto-close \\(name)") }
     }
 }

 func inspect(_ h: borrowing FileHandle) -> String { "inspect \\(h.name)" }

 func ownershipDemo(_ writes: [String], closeEarly: Bool) -> [String] {
     let log = Log()
     do {
         var handle = FileHandle(name: "data.txt", log: log)
         log.lines.append(inspect(handle))
         for w in writes { handle.write(w) }
         if closeEarly { handle.close() }
     }
     log.lines.append("done")
     return log.lines
 }
 """,
 explain="""A `~Copyable` value can't be implicitly copied — `let b = a` **moves** it, and using `a` afterwards is a compile error. `borrowing` parameters get temporary read access; `consuming` ones take ownership, so after `handle.close()` the handle is gone and its `deinit` runs at the end of `close()` (seeing `closed == true`). Structs with `deinit` — impossible for copyable structs — are how Swift models unique resources. (`discard self` can skip `deinit` entirely, but only for types whose stored properties are trivially destroyed — not `String` or class references.)""",
 tests=[({'writes':['a'],'closeEarly':True},['inspect data.txt','write a','close data.txt','done']), ({'writes':['a','b'],'closeEarly':False},['inspect data.txt','write a','write b','auto-close data.txt','done']), {'writes':[],'closeEarly':True}]))
P.append(dict(id='diag-noncopyable-use-after-move', title='Diagnostic: Use After consume', topic='Memory management', mode='diagnostic', diff='medium', concepts=['ownership'], docs=[('Swift Evolution SE-0390','https://github.com/swiftlang/swift-evolution/blob/main/proposals/0390-noncopyable-structs-and-enums.md')],
 statement="""Declare `struct Token: ~Copyable { let id: Int }`. Create `let a = Token(id: 1)`, then `let b = a` (a **move**), then try to `print(a.id)`. You pass when the compiler reports that `a` is used after being consumed.""",
 starter="struct Token: ~Copyable { let id: Int }\n\nlet a = Token(id: 1)\nlet b = a\nprint(b.id)\n",
 solution="struct Token: ~Copyable { let id: Int }\n\nfunc demo() {\n    let a = Token(id: 1)\n    let b = a\n    print(a.id)\n    print(b.id)\n}\ndemo()\n",
 explain="""For noncopyable types, assignment moves ownership; the old binding is dead. The ownership checker (a SIL pass — which is why the judge runs past type-checking) reports *'a' consumed more than once* / *used after consume*.""",
 tests=[{'name':'Use after move rejected','pattern':'consumed|after consume|used after'}]))
P.append(dict(id='diag-exclusivity', title='Diagnostic: Overlapping inout Access', topic='Memory management', mode='diagnostic', diff='medium', concepts=['memory-safety','inout'], docs=[('Memory Safety — Conflicting Access to In-Out Parameters', MS)],
 statement="""Write `func balance(_ x: inout Int, _ y: inout Int)` and call it as `balance(&score, &score)` on a single variable. You pass when the compiler rejects the aliasing `inout` arguments (the law of exclusivity).""",
 starter="func balance(_ x: inout Int, _ y: inout Int) {\n    let sum = x + y\n    x = sum / 2\n    y = sum - x\n}\n\nvar a = 42, b = 30\nbalance(&a, &b)\nprint(a, b)\n",
 solution="func balance(_ x: inout Int, _ y: inout Int) {\n    let sum = x + y\n    x = sum / 2\n    y = sum - x\n}\n\nvar score = 42\nbalance(&score, &score)\n",
 explain="""Swift 6.4 reports *inout arguments are not allowed to alias each other* (other forms of the same bug say *overlapping accesses …, but modification requires exclusive access*). Two simultaneous write accesses to the same memory are forbidden; Swift catches this statically when it can and at runtime otherwise. Copy one value first if you really need both.""",
 tests=[{'name':'Exclusivity violation reported','pattern':'overlapping accesses|not allowed to alias'}]))
P.append(dict(id='memory-layout', title='MemoryLayout & Padding', topic='Memory management', diff='medium', concepts=['memory-layout','value-semantics'], docs=[('MemoryLayout','https://developer.apple.com/documentation/swift/memorylayout')],
 sig='func layouts() -> [[Int]]',
 statement="""Declare `struct Loose { let flag: Bool; let value: Int64; let small: Bool }` and `struct Packed` with the **same fields reordered** to minimise padding. Return `[size, stride, alignment]` for `Loose`, `Packed`, `Int`, `Bool`, `String?` and a class reference `AnyObject` — using `MemoryLayout<T>`.

 Let the compiler tell you the numbers (the expected values come from the real toolchain).""",
 solution="""
 struct Loose { let flag: Bool; let value: Int64; let small: Bool }
 struct Packed { let value: Int64; let flag: Bool; let small: Bool }

 func info<T>(_: T.Type) -> [Int] {
     [MemoryLayout<T>.size, MemoryLayout<T>.stride, MemoryLayout<T>.alignment]
 }

 func layouts() -> [[Int]] {
     [info(Loose.self), info(Packed.self), info(Int.self), info(Bool.self), info(String?.self), info(AnyObject.self)]
 }
 """,
 explain="""`size` is the bytes a value occupies; `stride` is the distance between consecutive elements in an array (size rounded up to alignment). Putting the 8-byte field first lets the two `Bool`s share one trailing word — `Loose` is 17 bytes of size but 24 of stride. `String?` costs nothing extra thanks to spare bits.""",
 tests=[{}], hidden=0))
# ---------- Concurrency
P.append(dict(id='async-await-basics', title='async/await: Sequential vs async let', topic='Concurrency', diff='medium', concepts=['async-await'], docs=[('Concurrency — Calling Asynchronous Functions in Parallel', CC)],
 sig='func fetchAll(_ ids: [Int]) async -> [String]',
 statement="""`func fetchUser(_ id: Int) async -> String` (given) sleeps briefly and returns `"user<id>"`. Your `fetchAll` must return users for **all** ids in input order, but run the fetches **concurrently** — the judge's time limit is tight enough that doing them one by one fails for long inputs.

 Use a `TaskGroup` that returns `(index, user)` pairs and reassemble in order.""",
 timeLimitMs=1500,
 starter="""
 func fetchUser(_ id: Int) async -> String {
     try? await Task.sleep(for: .milliseconds(100))
     return "user\\(id)"
 }

 func fetchAll(_ ids: [Int]) async -> [String] {
     var users: [String] = []
     for id in ids { users.append(await fetchUser(id)) }
     return users
 }
 """,
 solution="""
 func fetchUser(_ id: Int) async -> String {
     try? await Task.sleep(for: .milliseconds(100))
     return "user\\(id)"
 }

 func fetchAll(_ ids: [Int]) async -> [String] {
     await withTaskGroup(of: (Int, String).self) { group in
         for (i, id) in ids.enumerated() {
             group.addTask { (i, await fetchUser(id)) }
         }
         var result = Array(repeating: "", count: ids.count)
         for await (i, user) in group { result[i] = user }
         return result
     }
 }
 """,
 explain="""`await` in a loop runs fetches **one after another**. A `TaskGroup` starts child tasks concurrently and yields results in **completion order** — carrying the index lets you rebuild input order. For a fixed small number of calls, `async let a = f(); async let b = g()` is simpler.""",
 tests=[({'ids':[1,2,3]},['user1','user2','user3']), {'ids':[]}, {'ids':list(range(30))}]))
P.append(dict(id='actor-bank', title='Actors Protect Mutable State', topic='Concurrency', diff='medium', concepts=['actors','sendable','async-await'], docs=[('Concurrency — Actors', CC)],
 sig='func concurrentDeposits(_ amounts: [Int]) async -> Int',
 statement="""Make `actor Account` with a private `balance` and `func deposit(_ amount: Int)`, plus `var current: Int`. Deposit every amount from a **separate child task** (all at once, via a task group) and return the final balance.

 With a plain class this would be a data race — and in Swift 6 language mode it won't even compile. Try it.""",
 solution="""
 actor Account {
     private var balance = 0
     func deposit(_ amount: Int) { balance += amount }
     var current: Int { balance }
 }

 func concurrentDeposits(_ amounts: [Int]) async -> Int {
     let account = Account()
     await withTaskGroup(of: Void.self) { group in
         for amount in amounts {
             group.addTask { await account.deposit(amount) }
         }
     }
     return await account.current
 }
 """,
 explain="""An actor serialises access to its state: calls from outside are `await`ed and run one at a time, so `balance += amount` can't interleave. Swift 6's strict concurrency checking rejects capturing a non-`Sendable` class in concurrent tasks; actors are `Sendable` by construction.""",
 tests=[({'amounts':[1,2,3]},6), {'amounts':[]}, {'amounts':[1]*500}, {'amounts':list(range(-50,51))}]))
P.append(dict(id='task-cancellation', title='Cooperative Cancellation', topic='Concurrency', diff='hard', concepts=['async-await','task-group'], docs=[('Concurrency — Task Cancellation', CC)],
 sig='func firstMatch(_ haystacks: [[Int]], target: Int) async -> Int',
 statement="""Search each array in its own child task (`withTaskGroup(of: Int?.self)`); a task returns its **array index** if it contains `target`. Return the **smallest** matching index found, or `-1`.

 When any task finds a match, call `group.cancelAll()`. Inside the search loop, check `Task.isCancelled` so remaining work stops early — but because you want the *smallest* index, only cancel tasks with a larger index… (simplify: keep collecting all results and take the minimum; cancellation just speeds things up).""",
 solution="""
 func firstMatch(_ haystacks: [[Int]], target: Int) async -> Int {
     await withTaskGroup(of: Int?.self) { group in
         for (i, hay) in haystacks.enumerated() {
             group.addTask {
                 for value in hay {
                     if Task.isCancelled { return nil }
                     if value == target { return i }
                 }
                 return nil
             }
         }
         var best: Int?
         for await found in group {
             if let found { best = min(best ?? found, found) }
         }
         return best ?? -1
     }
 }
 """,
 explain="""Cancellation in Swift is **cooperative**: `cancelAll()` just sets a flag; tasks must check `Task.isCancelled` (or call `try Task.checkCancellation()`) and stop. The group always waits for every child before returning — structured concurrency means no task outlives its scope.""",
 tests=[({'haystacks':[[1,2],[3,4],[4]],'target':4},1), {'haystacks':[],'target':1}, {'haystacks':[[9],[8]],'target':7}, {'haystacks':[[0]*1000+[5],[5]],'target':5}]))
P.append(dict(id='async-sequence', title='AsyncSequence & AsyncStream', topic='Concurrency', diff='hard', concepts=['async-await','custom-collection'], docs=[('Concurrency — Asynchronous Sequences', CC)],
 sig='func streamDemo(_ values: [Int], limit: Int) async -> [Int]',
 statement="""Build an `AsyncStream<Int>` that yields each value (with `continuation.yield`) and then finishes. Consume it with `for await`, keeping only even values, stopping once you've collected `limit` of them.""",
 solution="""
 func streamDemo(_ values: [Int], limit: Int) async -> [Int] {
     let stream = AsyncStream<Int> { continuation in
         for v in values { continuation.yield(v) }
         continuation.finish()
     }
     var evens: [Int] = []
     for await v in stream where v.isMultiple(of: 2) {
         evens.append(v)
         if evens.count == limit { break }
     }
     return evens
 }
 """,
 explain="""`AsyncSequence` is `Sequence`'s async twin: `for await` suspends between elements. `AsyncStream` adapts callback-style producers — call `yield` for each value and `finish()` at the end. `where` and `break` work just like in a regular loop.""",
 tests=[({'values':[1,2,3,4,6,8],'limit':2},[2,4]), {'values':[],'limit':3}, {'values':[2,4],'limit':5}]))
P.append(dict(id='diag-sendable-race', title='Diagnostic: Swift 6 Catches a Data Race', topic='Concurrency', mode='diagnostic', diff='medium', concepts=['sendable','actors'], docs=[('Concurrency — Sendable Types', CC)],
 statement="""In Swift 6 language mode, write a **non-final class** `Counter { var value = 0 }`, then in an `async` function capture one instance in a `Task { counter.value += 1 }` while also mutating it from the enclosing function. You pass when the compiler reports a data-race / sending / Sendable error.""",
 starter="actor Counter { var value = 0; func bump() { value += 1 } }\n\nfunc work() async {\n    let counter = Counter()\n    Task { await counter.bump() }\n    await counter.bump()\n}\n",
 solution="class Counter { var value = 0 }\n\nfunc work() async {\n    let counter = Counter()\n    Task { counter.value += 1 }\n    counter.value += 1\n}\n",
 explain="""Swift 6 turns data-race warnings into **errors**: a non-Sendable class instance can't be sent into a concurrently executing task while still being used locally (*sending 'counter' risks causing data races*). The fix is an actor, a `Sendable` type, or not sharing.""",
 tests=[{'name':'Race rejected','pattern':'data race|Sendable|sending'}]))
P.append(dict(id='main-actor-isolation', title='@MainActor & nonisolated', topic='Concurrency', diff='hard', concepts=['actors','sendable'], docs=[('Concurrency — The Main Actor', CC)],
 sig='func uiDemo(_ names: [String]) async -> [String]',
 statement="""`@MainActor final class ViewModel` holds `var items: [String]` and a method `func load(_ names: [String]) async` that fetches uppercased names using a **`nonisolated`** static helper `nonisolated static func transform(_ s: String) async -> String` (runs off the main actor), then appends them on the main actor.

 From `uiDemo` (not main-actor), create the view model and call it with `await`, then read `items` (also with `await`). Return the items plus `"count <n>"`.""",
 solution="""
 @MainActor
 final class ViewModel {
     var items: [String] = []

     nonisolated static func transform(_ s: String) async -> String { s.uppercased() }

     func load(_ names: [String]) async {
         for name in names {
             let value = await Self.transform(name)
             items.append(value)
         }
     }
 }

 func uiDemo(_ names: [String]) async -> [String] {
     let vm = await ViewModel()
     await vm.load(names)
     let items = await vm.items
     return items + ["count \\(items.count)"]
 }
 """,
 explain="""`@MainActor` isolates all of a type's state to the main actor — reaching in from elsewhere requires `await` (even the initialiser here). `nonisolated` opts a member out, so it can run on the global concurrent executor. This is the model SwiftUI view models use.""",
 tests=[({'names':['a','b']},['A','B','count 2']), {'names':[]}]))
# ---------- Property wrappers & result builders
P.append(dict(id='property-wrapper-clamped', title='Property Wrapper: @Clamped', topic='Advanced features', diff='medium', concepts=['property-wrappers','generic-constraints'], docs=[('Properties — Property Wrappers', PR)],
 sig='func wrapperDemo(_ volumes: [Int], _ names: [String]) -> [String]',
 statement="""Write `@propertyWrapper struct Clamped<Value: Comparable>` (initialised with `wrappedValue` and a `ClosedRange`) and `@propertyWrapper struct Trimmed` (trims whitespace, lowercases). Also give `Clamped` a **projected value** `$volume` that reports how many times a write was clamped.

 `struct Settings { @Clamped(0...100) var volume = 50; @Trimmed var username = "" }`. Apply each volume and each name, logging `"v=<volume>"` and `"u=<username>"`; finally log `"clamps=<$volume>"`.""",
 solution="""
 @propertyWrapper
 struct Clamped<Value: Comparable> {
     private var value: Value
     private let range: ClosedRange<Value>
     private(set) var projectedValue = 0

     init(wrappedValue: Value, _ range: ClosedRange<Value>) {
         self.range = range
         self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
     }

     var wrappedValue: Value {
         get { value }
         set {
             let clamped = min(max(newValue, range.lowerBound), range.upperBound)
             if clamped != newValue { projectedValue += 1 }
             value = clamped
         }
     }
 }

 @propertyWrapper
 struct Trimmed {
     private var value = ""
     init(wrappedValue: String) { self.wrappedValue = wrappedValue }
     var wrappedValue: String {
         get { value }
         set { value = newValue.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() }
     }
 }

 import Foundation

 struct Settings {
     @Clamped(0...100) var volume = 50
     @Trimmed var username = ""
 }

 func wrapperDemo(_ volumes: [Int], _ names: [String]) -> [String] {
     var s = Settings()
     var log: [String] = []
     for v in volumes { s.volume = v; log.append("v=\\(s.volume)") }
     for n in names { s.username = n; log.append("u=\\(s.username)") }
     log.append("clamps=\\(s.$volume)")
     return log
 }
 """,
 explain="""A property wrapper moves "how this property is stored" into a reusable type. `@Clamped(0...100) var volume = 50` calls `init(wrappedValue: 50, 0...100)`. The `projectedValue` is exposed with a `$` prefix — that's how SwiftUI's `$binding` works. (`trimmingCharacters` comes from Foundation.)""",
 tests=[({'volumes':[20,150,-5],'names':['  Varun ']},['v=20','v=100','v=0','u=varun','clamps=2']), {'volumes':[],'names':[]}, {'volumes':[100,0],'names':['A B','\\tx\\n']}]))
P.append(dict(id='result-builder-html', title='Result Builder: Tiny HTML DSL', topic='Advanced features', diff='hard', concepts=['result-builders','closures'], docs=[('Attributes — resultBuilder', AT)],
 sig='func renderPage(title: String, items: [String], showFooter: Bool) -> String',
 statement="""Write `@resultBuilder struct HTMLBuilder` with `buildBlock`, `buildOptional`, `buildEither(first:)/(second:)`, `buildArray` and `buildExpression(_ s: String)` — building a `[String]` of fragments.

 Then `func html(@HTMLBuilder _ content: () -> [String]) -> String` joins fragments. Render:
 ```swift
 html {
     "<h1>\\(title)</h1>"
     if items.isEmpty { "<p>empty</p>" } else { "<ul>"; for i in items { "<li>\\(i)</li>" }; "</ul>" }
     if showFooter { "<footer/>" }
 }
 ```
 (Write the `else` branch across lines — semicolons are shown only for brevity.)""",
 solution="""
 @resultBuilder
 struct HTMLBuilder {
     static func buildExpression(_ s: String) -> [String] { [s] }
     static func buildBlock(_ parts: [String]...) -> [String] { parts.flatMap { $0 } }
     static func buildOptional(_ part: [String]?) -> [String] { part ?? [] }
     static func buildEither(first: [String]) -> [String] { first }
     static func buildEither(second: [String]) -> [String] { second }
     static func buildArray(_ parts: [[String]]) -> [String] { parts.flatMap { $0 } }
 }

 func html(@HTMLBuilder _ content: () -> [String]) -> String {
     content().joined()
 }

 func renderPage(title: String, items: [String], showFooter: Bool) -> String {
     html {
         "<h1>\\(title)</h1>"
         if items.isEmpty {
             "<p>empty</p>"
         } else {
             "<ul>"
             for i in items {
                 "<li>\\(i)</li>"
             }
             "</ul>"
         }
         if showFooter {
             "<footer/>"
         }
     }
 }
 """,
 explain="""A result builder rewrites the statements in a closure into calls: each expression → `buildExpression`, the sequence → `buildBlock`, `if` without else → `buildOptional`, `if/else` → `buildEither`, `for` → `buildArray`. SwiftUI's `@ViewBuilder` and `RegexBuilder` are exactly this.""",
 tests=[({'title':'Hi','items':['a','b'],'showFooter':True},'<h1>Hi</h1><ul><li>a</li><li>b</li></ul><footer/>'), {'title':'Empty','items':[],'showFooter':False}, {'title':'','items':['x'],'showFooter':False}]))
# ---------- Codable & Foundation
P.append(dict(id='codable-snake-case', title='Codable with snake_case & CodingKeys', topic='Codable', diff='medium', concepts=['codable','codable-keys'], docs=[('Encoding and Decoding Custom Types', CODABLE)],
 sig='func decodeUsers(_ json: String) -> [String]',
 statement="""Decode JSON like:
 ```json
 [{"user_id": 1, "first_name": "Ana", "is_admin": true, "e-mail": "a@x.io"}]
 ```
 into `struct User: Codable { let userId: Int; let firstName: String; let isAdmin: Bool; let email: String? }` using `keyDecodingStrategy = .convertFromSnakeCase` **plus** a `CodingKeys` enum to map `"e-mail"` (which snake case conversion can't handle).

 Return `"<id>:<name>:<admin|user>:<email or none>"` per user, or `["invalid"]` if decoding fails.""",
 solution="""
 import Foundation

 struct User: Codable {
     let userId: Int
     let firstName: String
     let isAdmin: Bool
     let email: String?

     enum CodingKeys: String, CodingKey {
         case userId, firstName, isAdmin
         case email = "e-mail"
     }
 }

 func decodeUsers(_ json: String) -> [String] {
     let decoder = JSONDecoder()
     decoder.keyDecodingStrategy = .convertFromSnakeCase
     guard let users = try? decoder.decode([User].self, from: Data(json.utf8)) else { return ["invalid"] }
     return users.map { "\\($0.userId):\\($0.firstName):\\($0.isAdmin ? "admin" : "user"):\\($0.email ?? "none")" }
 }
 """,
 explain="""With `.convertFromSnakeCase`, the decoder converts JSON keys to camelCase **before** matching `CodingKeys` raw values — so custom raw values must be written in the converted form (`"e-mail"` has no underscore, so it passes through unchanged). Optional properties decode missing keys as `nil`.""",
 tests=[({'json':'[{"user_id": 1, "first_name": "Ana", "is_admin": true, "e-mail": "a@x.io"}]'},['1:Ana:admin:a@x.io']), {'json':'[{"user_id": 2, "first_name": "Bo", "is_admin": false}]'}, {'json':'[]'}, {'json':'[{"user_id": "x"}]'}, {'json':'not json'}]))
P.append(dict(id='codable-custom-init', title='Custom init(from:) for Messy JSON', topic='Codable', diff='hard', concepts=['codable','codable-keys','error-handling'], docs=[('Encoding and Decoding Custom Types', CODABLE)],
 sig='func decodeProducts(_ json: String) -> [String]',
 statement="""A legacy API sends prices **either** as numbers or as strings (`"price": "9.99"` or `9.99`), may omit `tags` (default `[]`), and nests the name: `{"info": {"name": "Pen"}}`.

 Write `struct Product: Decodable` with `name: String`, `priceCents: Int` (rounded), `tags: [String]`, implementing `init(from decoder:)` with a **nested container**. Return `"<name> <cents> [tags joined by ,]"` per product, or `["error: <DecodingError case name>"]` on failure (`"keyNotFound"`, `"typeMismatch"`, `"dataCorrupted"`, `"valueNotFound"`).""",
 solution="""
 import Foundation

 struct Product: Decodable {
     let name: String
     let priceCents: Int
     let tags: [String]

     enum CodingKeys: String, CodingKey { case info, price, tags }
     enum InfoKeys: String, CodingKey { case name }

     init(from decoder: Decoder) throws {
         let c = try decoder.container(keyedBy: CodingKeys.self)
         let info = try c.nestedContainer(keyedBy: InfoKeys.self, forKey: .info)
         name = try info.decode(String.self, forKey: .name)
         let price: Double
         if let d = try? c.decode(Double.self, forKey: .price) {
             price = d
         } else {
             let s = try c.decode(String.self, forKey: .price)
             guard let d = Double(s) else {
                 throw DecodingError.dataCorruptedError(forKey: .price, in: c, debugDescription: "bad price \\(s)")
             }
             price = d
         }
         priceCents = Int((price * 100).rounded())
         tags = try c.decodeIfPresent([String].self, forKey: .tags) ?? []
     }
 }

 func decodeProducts(_ json: String) -> [String] {
     do {
         let products = try JSONDecoder().decode([Product].self, from: Data(json.utf8))
         return products.map { "\\($0.name) \\($0.priceCents) [\\($0.tags.joined(separator: ","))]" }
     } catch let error as DecodingError {
         let name = switch error {
         case .keyNotFound: "keyNotFound"
         case .typeMismatch: "typeMismatch"
         case .valueNotFound: "valueNotFound"
         case .dataCorrupted: "dataCorrupted"
         @unknown default: "unknown"
         }
         return ["error: \\(name)"]
     } catch {
         return ["error: other"]
     }
 }
 """,
 explain="""`container(keyedBy:)` gives keyed access; `nestedContainer` steps into sub-objects; `decodeIfPresent` handles optional keys. Trying one type then another with `try?` absorbs inconsistent APIs. `DecodingError`'s cases tell you exactly what went wrong and where (`codingPath`). `@unknown default` handles cases added in future SDKs.""",
 tests=[({'json':'[{"info":{"name":"Pen"},"price":"1.5"},{"info":{"name":"Ink"},"price":2.999,"tags":["a","b"]}]'},['Pen 150 []','Ink 300 [a,b]']), {'json':'[{"price":1}]'}, {'json':'[{"info":{"name":"X"},"price":true}]'}, {'json':'[{"info":{"name":"X"},"price":"abc"}]'}, {'json':'{'}]))
P.append(dict(id='codable-round-trip', title='Encode → Decode Round Trip', topic='Codable', diff='medium', concepts=['codable','enums','associated-values'], docs=[('Encoding and Decoding Custom Types', CODABLE)],
 sig='func roundTrip(_ events: [String]) -> [String]',
 statement="""`enum Event: Codable, Equatable { case login(user: String); case purchase(item: String, cents: Int); case logout }` — Swift synthesises `Codable` for enums with associated values.

 Parse specs (`"login ana"`, `"purchase pen 150"`, `"logout"`), encode the array with `JSONEncoder` (`.sortedKeys`), decode it back, and return: the JSON string, then `"equal"` or `"different"`.""",
 solution="""
 import Foundation

 enum Event: Codable, Equatable {
     case login(user: String)
     case purchase(item: String, cents: Int)
     case logout
 }

 func roundTrip(_ events: [String]) -> [String] {
     let parsed: [Event] = events.compactMap { spec in
         let p = spec.split(separator: " ").map(String.init)
         switch (p.first, p.count) {
         case ("login", 2): return .login(user: p[1])
         case ("purchase", 3): return Int(p[2]).map { .purchase(item: p[1], cents: $0) }
         case ("logout", 1): return .logout
         default: return nil
         }
     }
     let encoder = JSONEncoder()
     encoder.outputFormatting = [.sortedKeys]
     guard let data = try? encoder.encode(parsed),
           let back = try? JSONDecoder().decode([Event].self, from: data) else { return ["failed"] }
     return [String(decoding: data, as: UTF8.self), back == parsed ? "equal" : "different"]
 }
 """,
 explain="""Synthesised enum coding (Swift 5.5+) uses the case name as the key and the associated values' labels as nested keys — a case without values encodes as an empty object. `Equatable` synthesis makes the round-trip check a one-liner.""",
 tests=[({'events':['login ana','logout']},['[{"login":{"user":"ana"}},{"logout":{}}]','equal']), {'events':[]}, {'events':['purchase pen 150','bad','purchase x y']}]))
P.append(dict(id='regex-extract', title='Swift Regex: Extract Dates', topic='Strings deep dive', diff='medium', concepts=['regex','strings-are-collections'], docs=[('Regex', REGEX)],
 sig='func extractDates(_ text: String) -> [String]',
 statement="""Find every date written `YYYY-MM-DD` in the text using a Swift **regex literal** with named or positional captures, and reformat each as `DD/MM/YYYY`. Only accept months 01–12 and days 01–31 (check numerically after matching).

 ```swift
 extractDates("Due 2024-03-15, moved to 2024-13-01 then 2025-01-02.")
 // ["15/03/2024", "02/01/2025"]
 ```""",
 solution="""
 func extractDates(_ text: String) -> [String] {
     let pattern = /(\\d{4})-(\\d{2})-(\\d{2})/
     return text.matches(of: pattern).compactMap { match in
         let (_, year, month, day) = match.output
         guard let m = Int(month), (1...12).contains(m), let d = Int(day), (1...31).contains(d) else { return nil }
         return "\\(day)/\\(month)/\\(year)"
     }
 }
 """,
 explain="""Regex literals `/…/` are checked **at compile time**, and their captures are typed: `match.output` is `(Substring, Substring, Substring, Substring)`. `matches(of:)`, `firstMatch(of:)` and `wholeMatch(of:)` cover most needs; `RegexBuilder` offers a DSL for complex patterns.""",
 tests=[({'text':'Due 2024-03-15, moved to 2024-13-01 then 2025-01-02.'},['15/03/2024','02/01/2025']), {'text':''}, {'text':'2024-02-30 and 1999-12-31 and 12024-01-01'}]))
P.append(dict(id='regex-builder-log', title='RegexBuilder: Parse Log Lines', topic='Strings deep dive', diff='hard', concepts=['regex','result-builders'], docs=[('Regex', REGEX)],
 sig='func parseLogs(_ lines: [String]) -> [String]',
 statement="""Use `import RegexBuilder` to parse lines like `"[ERROR] 2024-05-01 disk full (code 28)"`: level (`INFO|WARN|ERROR`), date, message, and a numeric code captured with `TryCapture` transforming to `Int`.

 Return `"<level>|<code>|<message>"` for lines that match the **whole** line, and `"skip"` otherwise.""",
 solution="""
 import RegexBuilder

 func parseLogs(_ lines: [String]) -> [String] {
     let level = Reference(Substring.self)
     let message = Reference(Substring.self)
     let code = Reference(Int.self)
     let regex = Regex {
         "["
         Capture(as: level) { ChoiceOf { "INFO"; "WARN"; "ERROR" } }
         "] "
         Repeat(.digit, count: 4); "-"; Repeat(.digit, count: 2); "-"; Repeat(.digit, count: 2)
         " "
         Capture(as: message) { OneOrMore(.any, .reluctant) }
         " (code "
         TryCapture(as: code) { OneOrMore(.digit) } transform: { Int($0) }
         ")"
     }
     return lines.map { line in
         guard let m = line.wholeMatch(of: regex) else { return "skip" }
         return "\\(m[level])|\\(m[code])|\\(m[message])"
     }
 }
 """,
 explain="""`RegexBuilder` is a **result builder** DSL: readable, composable and still compiled to the same engine. `Reference` names captures; `TryCapture` transforms (and can reject) a capture; `.reluctant` makes the message lazy so `" (code "` can match after it.""",
 tests=[({'lines':['[ERROR] 2024-05-01 disk full (code 28)','[INFO] 2024-05-01 ok']},['ERROR|28|disk full','skip']), {'lines':[]}, {'lines':['[WARN] 2023-12-31 low battery (code 7)','[DEBUG] 2023-12-31 x (code 1)']}]))
P.append(dict(id='sha256-hash', title='SHA-256 with CryptoKit', topic='Foundation essentials', diff='easy', concepts=['hashing','equatable-hashable'], docs=[('CryptoKit — SHA256','https://developer.apple.com/documentation/cryptokit/sha256')],
 sig='func digests(_ inputs: [String]) -> [String]',
 statement="""Return the lowercase hex SHA-256 digest of each string's UTF-8 bytes, using CryptoKit. Then answer for yourself: why is `hashValue` **not** a substitute?""",
 solution="""
 import CryptoKit
 import Foundation

 func digests(_ inputs: [String]) -> [String] {
     inputs.map { input in
         SHA256.hash(data: Data(input.utf8)).map { String(format: "%02x", $0) }.joined()
     }
 }
 """,
 explain="""`SHA256.hash(data:)` returns a digest that's a `Sequence` of bytes; hex-encode with `%02x`. `hashValue` / `Hasher` are randomly seeded **per process** (to resist hash-flooding) — the same string hashes differently on each run, and it isn't cryptographically secure.""",
 tests=[({'inputs':['']},['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']), {'inputs':['abc','Swift 🦅']}]))
P.append(dict(id='uuid-and-identifiable', title='UUID & Identifiable', topic='Foundation essentials', diff='easy', concepts=['uuid','protocols'], docs=[('UUID','https://developer.apple.com/documentation/foundation/uuid')],
 sig='func uuidChecks(_ strings: [String]) -> [String]',
 statement="""For each string, return `"valid <UPPERCASED uuidString>"` if `UUID(uuidString:)` accepts it, else `"invalid"`. Finally append `"unique"` if two freshly generated `UUID()`s differ, and `"<n>"` = the character count of a generated `uuidString`.

 Also declare `struct Todo: Identifiable { let id = UUID(); let title: String }` and use it once (e.g. confirm two todos with the same title have different ids) — append `"ids differ"`.""",
 solution="""
 import Foundation

 struct Todo: Identifiable {
     let id = UUID()
     let title: String
 }

 func uuidChecks(_ strings: [String]) -> [String] {
     var out = strings.map { s in UUID(uuidString: s).map { "valid \\($0.uuidString)" } ?? "invalid" }
     out.append(UUID() != UUID() ? "unique" : "collision")
     out.append("\\(UUID().uuidString.count)")
     out.append(Todo(title: "x").id != Todo(title: "x").id ? "ids differ" : "same")
     return out
 }
 """,
 explain="""`UUID()` generates a random (v4) 128-bit identifier; `uuidString` is the canonical 36-character uppercase form, and `UUID(uuidString:)` is failable and case-insensitive. `Identifiable` just requires an `id` — perfect for models that have no natural key.""",
 tests=[({'strings':['e621e1f8-c36c-495a-93fc-0c247a3e6e5f','nope']},['valid E621E1F8-C36C-495A-93FC-0C247A3E6E5F','invalid','unique','36','ids differ']), {'strings':[]}]))
P.append(dict(id='file-manager-listing', title='FileManager: List a Directory', topic='Foundation essentials', diff='medium', concepts=['file-manager','error-handling','defer'], docs=[('FileManager','https://developer.apple.com/documentation/foundation/filemanager')],
 sig='func listing(_ files: [String]) throws -> [String]',
 statement="""Create a unique temporary directory (`FileManager.default.temporaryDirectory` + a UUID), create each given file inside it (paths may contain one subfolder, like `"docs/a.md"` — create intermediate directories), then return the **sorted** relative paths of all *files* found recursively with `enumerator(at:includingPropertiesForKeys:)`. Always delete the directory at the end — use `defer`.""",
 solution="""
 import Foundation

 func listing(_ files: [String]) throws -> [String] {
     let fm = FileManager.default
     let root = fm.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
     try fm.createDirectory(at: root, withIntermediateDirectories: true)
     defer { try? fm.removeItem(at: root) }

     for path in files {
         let url = root.appendingPathComponent(path)
         try fm.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
         try Data(path.utf8).write(to: url)
     }

     var found: [String] = []
     let base = root.resolvingSymlinksInPath().path + "/"
     if let e = fm.enumerator(at: root, includingPropertiesForKeys: [.isRegularFileKey]) {
         for case let url as URL in e {
             let isFile = (try? url.resourceValues(forKeys: [.isRegularFileKey]))?.isRegularFile ?? false
             if isFile { found.append(url.resolvingSymlinksInPath().path.replacingOccurrences(of: base, with: "")) }
         }
     }
     return found.sorted()
 }
 """,
 explain="""`FileManager` APIs throw, so the function is `throws`. `defer` guarantees cleanup even if a write fails. The enumerator yields `Any`, hence `for case let url as URL`. On macOS the temp dir is behind a symlink (`/var` → `/private/var`), so resolve both sides before computing relative paths.""",
 tests=[({'files':['a.txt','docs/b.md']},['a.txt','docs/b.md']), {'files':[]}, {'files':['z/1','z/2','y.txt']}]))
P.append(dict(id='compiler-directives', title='Conditional Compilation', topic='Advanced features', diff='easy', concepts=['compiler-directives','availability','assert'], docs=[('Statements — Compiler Control Statements', ST)],
 sig='func buildInfo() -> [String]',
 statement="""Return facts about **this** build using compile-time conditions, one per line:
 1. `"swift>=6"` or `"swift<6"` via `#if swift(>=6.0)`
 2. `"macOS"`, `"Linux"` or `"other"` via `#if os(...)`
 3. `"arm64"` or `"x86_64"` via `#if arch(...)`
 4. `"has Foundation"` via `#if canImport(Foundation)`
 5. `"debug"` or `"release"` — the judge compiles with `-Onone` and **without** `-D DEBUG`, so check `#if DEBUG`
 6. `"macOS 13+"` if `#available(macOS 13, *)`, else `"older"`""",
 solution="""
 func buildInfo() -> [String] {
     var out: [String] = []
     #if swift(>=6.0)
     out.append("swift>=6")
     #else
     out.append("swift<6")
     #endif
     #if os(macOS)
     out.append("macOS")
     #elseif os(Linux)
     out.append("Linux")
     #else
     out.append("other")
     #endif
     #if arch(arm64)
     out.append("arm64")
     #else
     out.append("x86_64")
     #endif
     #if canImport(Foundation)
     out.append("has Foundation")
     #endif
     #if DEBUG
     out.append("debug")
     #else
     out.append("release")
     #endif
     if #available(macOS 13, *) {
         out.append("macOS 13+")
     } else {
         out.append("older")
     }
     return out
 }
 """,
 explain="""`#if` removes code **before** type checking — the other branches needn't even compile for this platform. `DEBUG` is just a flag Xcode passes (`-D DEBUG`) in debug configurations; plain `swiftc` doesn't define it. `#available` is a **runtime** OS check that also unlocks newer APIs inside the branch.""",
 tests=[{}], hidden=0))
P.append(dict(id='diag-error-directive', title='Diagnostic: #error', topic='Advanced features', mode='diagnostic', diff='easy', concepts=['compiler-directives'], docs=[('Statements — Compile-Time Diagnostic Statement', ST)],
 statement="""Use `#error("Set API_KEY before building")` so that the build **fails with your own message** unless a compilation condition `HAS_KEY` is defined. You pass when the compiler emits your error text.""",
 starter="#if HAS_KEY\nlet apiKey = \"secret\"\n#else\n// fail the build with a helpful message\nlet apiKey = \"\"\n#endif\n",
 solution="#if HAS_KEY\nlet apiKey = \"secret\"\n#else\n#error(\"Set API_KEY before building\")\n#endif\n",
 explain="""`#error("…")` and `#warning("…")` emit diagnostics on purpose — handy for configuration mistakes and TODOs you can't ignore.""",
 tests=[{'name':'Custom error emitted','pattern':'Set API_KEY before building'}]))
P.append(dict(id='diag-main-attribute', title='Diagnostic: @main vs Top-Level Code', topic='Advanced features', mode='diagnostic', diff='medium', concepts=['main-attribute'], docs=[('Attributes — main', AT)],
 statement="""A program has exactly one entry point. The judge compiles your code as `main.swift`, which **already** has top-level code as its entry point. Add a type marked `@main` with a `static func main()`. You pass when the compiler rejects having both.""",
 starter="struct App {\n    static func main() {\n        print(\"hello\")\n    }\n}\nApp.main()\n",
 solution="@main\nstruct App {\n    static func main() {\n        print(\"hello\")\n    }\n}\n",
 explain="""`@main` designates the entry point via `static func main()` (which can be `async throws`). It can't be combined with top-level code — in a package you'd name the file anything *but* `main.swift`, or compile with `-parse-as-library`.""",
 tests=[{'name':'Conflicting entry points','pattern':"'main' attribute cannot be used in a module that contains top-level code|main"}]))
P.append(dict(id='assert-precondition', title='assert vs precondition vs fatalError', topic='Error handling', diff='medium', concepts=['assert','never-type'], docs=[('The Basics — Assertions and Preconditions','LanguageGuide/TheBasics')],
 sig='func checkedAges(_ ages: [Int]) -> [String]',
 statement="""Write `func validatedAge(_ age: Int) -> Int` that uses `precondition(age >= 0, "age must be non-negative")` and returns the age. Then `checkedAges` returns `"ok <age>"` for each age.

 The hidden tests include a negative age — so the judge will report a **runtime error** whose message is your precondition text. That's the expected behaviour here: the reference solution *also* traps… so instead, have `checkedAges` **filter out negatives before** calling `validatedAge`, and append `"rejected <n>"` for how many were filtered. Use `assert` for the internal invariant that the output count equals the input count.""",
 solution="""
 func validatedAge(_ age: Int) -> Int {
     precondition(age >= 0, "age must be non-negative")
     return age
 }

 func checkedAges(_ ages: [Int]) -> [String] {
     let valid = ages.filter { $0 >= 0 }
     var out = valid.map { "ok \\(validatedAge($0))" }
     out.append("rejected \\(ages.count - valid.count)")
     assert(out.count == valid.count + 1, "one line per valid age plus the summary")
     return out
 }
 """,
 explain="""`assert` is checked in debug builds only (`-Onone`), `precondition` in release too (except `-Ounchecked`), `fatalError` always. Use them for **programmer errors**; validate user input with normal control flow. Try calling `validatedAge(-1)` and look at the judge's runtime-error message.""",
 tests=[({'ages':[3,-1,40]},['ok 3','ok 40','rejected 1']), {'ages':[]}, {'ages':[-5,-6]}]))
# ---------- Patterns: singleton, DI, LRU cache
P.append(dict(id='lru-cache', title='Design: LRU Cache (O(1))', topic='Design patterns', diff='hard', concepts=['caching','dictionary-basics','class-definition'], docs=[('Structures and Classes', 'LanguageGuide/ClassesAndStructures')],
 statement="""Implement `final class LRUCache` with `init(capacity: Int)`, `func get(_ key: Int) -> Int` (`-1` if missing) and `func put(_ key: Int, _ value: Int)`, both **O(1)**, evicting the least-recently-used key when over capacity.

 Use a dictionary of key → node plus a doubly linked list of `final class Node`s (with `weak`/`unowned` or plain optional links — think about retain cycles). The judge drives it like LeetCode #146.""",
 starter="""
 final class LRUCache {
     init(capacity: Int) {}
     func get(_ key: Int) -> Int { -1 }
     func put(_ key: Int, _ value: Int) {}
 }
 """,
 solution="""
 final class LRUCache {
     private final class Node {
         let key: Int
         var value: Int
         var prev: Node?
         var next: Node?
         init(_ key: Int, _ value: Int) { self.key = key; self.value = value }
     }

     private let capacity: Int
     private var map: [Int: Node] = [:]
     private let head = Node(0, 0)   // most recent after head
     private let tail = Node(0, 0)   // least recent before tail

     init(capacity: Int) {
         self.capacity = capacity
         head.next = tail
         tail.prev = head
     }

     deinit {
         // Break the doubly-linked chain so ARC can free every node.
         var node = head.next
         while let n = node { node = n.next; n.prev = nil; n.next = nil }
     }

     private func unlink(_ n: Node) {
         n.prev?.next = n.next
         n.next?.prev = n.prev
     }

     private func pushFront(_ n: Node) {
         n.next = head.next
         n.prev = head
         head.next?.prev = n
         head.next = n
     }

     func get(_ key: Int) -> Int {
         guard let n = map[key] else { return -1 }
         unlink(n)
         pushFront(n)
         return n.value
     }

     func put(_ key: Int, _ value: Int) {
         guard capacity > 0 else { return }
         if let n = map[key] {
             n.value = value
             unlink(n)
             pushFront(n)
             return
         }
         let n = Node(key, value)
         map[key] = n
         pushFront(n)
         if map.count > capacity, let lru = tail.prev, lru !== head {
             unlink(lru)
             map[lru.key] = nil
         }
     }
 }
 """,
 harness="""
 struct __Input: Decodable { let ops: [String]; let args: [[Int]] }
 func __run(_ __i: __Input) async throws -> [Int?] {
     var cache: LRUCache?
     var out: [Int?] = []
     for (op, a) in zip(__i.ops, __i.args) {
         switch op {
         case "init": cache = LRUCache(capacity: a[0]); out.append(nil)
         case "put": cache!.put(a[0], a[1]); out.append(nil)
         default: out.append(cache!.get(a[0]))
         }
     }
     return out
 }
 """,
 explain="""The dictionary finds nodes in O(1); the linked list orders them by recency with O(1) moves. Sentinel `head`/`tail` nodes remove edge cases. A doubly linked list of strong `prev`/`next` references **is** a set of retain cycles — make `prev` weak, or break the links in `deinit` as here.""",
 tests=[({'ops':['init','put','put','get','put','get','put','get','get','get'],'args':[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]},[None,None,None,1,None,-1,None,-1,3,4]),
        {'ops':['init','get'],'args':[[1],[5]]},
        {'ops':['init','put','put','get'],'args':[[1],[1,1],[1,9],[1]]},
        {'ops':['init','put','get'],'args':[[0],[1,1],[1]]}]))
P.append(dict(id='memoization', title='Memoize Any Function', topic='Design patterns', diff='medium', concepts=['caching','closures','generics','capturing-values'], docs=[('Closures — Capturing Values','LanguageGuide/Closures')],
 sig='func memoDemo(_ n: Int) -> [Int]',
 statement="""Write a generic `func memoizeRecursive<In: Hashable, Out>(_ body: @escaping ((In) -> Out, In) -> Out) -> (In) -> Out` that caches results in a captured dictionary and lets `body` call the memoised function recursively.

 Use it for Fibonacci and return `[fib(n), callCount]`, where `callCount` counts how many times `body` actually ran (should be `n + 1` for `n ≥ 1`, thanks to the cache). `n ≤ 90`.""",
 solution="""
 final class Box<T> { var value: T; init(_ v: T) { value = v } }

 func memoizeRecursive<In: Hashable, Out>(_ body: @escaping ((In) -> Out, In) -> Out) -> (In) -> Out {
     let cache = Box<[In: Out]>([:])
     let recurse = Box<((In) -> Out)?>(nil)
     let memo: (In) -> Out = { input in
         if let hit = cache.value[input] { return hit }
         let result = body(recurse.value!, input)
         cache.value[input] = result
         return result
     }
     recurse.value = memo
     return memo
 }

 func memoDemo(_ n: Int) -> [Int] {
     let calls = Box(0)
     let fib: (Int) -> Int = memoizeRecursive { fib, k in
         calls.value += 1
         return k < 2 ? k : fib(k - 1) + fib(k - 2)
     }
     return [fib(n), calls.value]
 }
 """,
 explain="""Memoisation trades memory for time: naive Fibonacci is O(2ⁿ), memoised O(n). The recursion trick passes the memoised function into `body`, tying the knot through a mutable box. Note the box creates a cycle (`memo` → box → `memo`) — acceptable for a demo, but real code would break it or use a class with a method.""",
 tests=[({'n':10},[55,11]), {'n':0}, {'n':1}, {'n':90}]))
P.append(dict(id='dependency-injection', title='Dependency Injection with Protocols', topic='Design patterns', diff='medium', concepts=['dependency-injection','protocols','singleton'], docs=[('Protocols', 'LanguageGuide/Protocols')],
 sig='func greetingsAt(_ hours: [Int], useLive: Bool) -> [String]',
 statement="""`struct Greeter` produces `"Good morning"` (<12), `"Good afternoon"` (<18) or `"Good evening"` based on the hour from a **clock**. Instead of reading the real time inside `Greeter`, inject a `protocol Clock { var hour: Int { get } }` through the initialiser.

 Provide `struct FixedClock: Clock` for tests and `final class SystemClock: Clock` as a **singleton** (Swift 6 will insist it's `Sendable`) (`static let shared`, `private init`) that reads the real hour with `Calendar`. With `useLive == false`, greet at each fixed hour. With `useLive == true`, return just `["live ok"]` if the system clock's greeting is one of the three valid greetings.""",
 solution="""
 import Foundation

 protocol Clock { var hour: Int { get } }

 struct FixedClock: Clock { let hour: Int }

 final class SystemClock: Clock, Sendable {
     static let shared = SystemClock()
     private init() {}
     var hour: Int { Calendar.current.component(.hour, from: Date()) }
 }

 struct Greeter {
     let clock: any Clock
     init(clock: any Clock = SystemClock.shared) { self.clock = clock }

     func greeting() -> String {
         switch clock.hour {
         case ..<12: "Good morning"
         case ..<18: "Good afternoon"
         default: "Good evening"
         }
     }
 }

 func greetingsAt(_ hours: [Int], useLive: Bool) -> [String] {
     if useLive {
         let g = Greeter().greeting()
         return ["Good morning", "Good afternoon", "Good evening"].contains(g) ? ["live ok"] : ["bad"]
     }
     return hours.map { Greeter(clock: FixedClock(hour: $0)).greeting() }
 }
 """,
 explain="""Code that reaches for globals (the current time, a network singleton) is hard to test. **Initialiser injection** with a protocol lets tests pass a fake. A default argument (`= SystemClock.shared`) keeps production call sites short. Singletons are fine for truly global resources — inject them rather than referencing them everywhere. **Swift 6 gotcha:** `static let shared = SystemClock()` is rejected (*static property 'shared' is not concurrency-safe because non-'Sendable' type*) unless the class is `Sendable` — fine here because it has no mutable state. A singleton *with* mutable state should be an `actor` or `@MainActor`.""",
 tests=[({'hours':[9,13,20],'useLive':False},['Good morning','Good afternoon','Good evening']), {'hours':[],'useLive':True}, {'hours':[0,11,12,17,18,23],'useLive':False}]))

write_all(P, 'advanced', 300)
