import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CS='LanguageGuide/ClassesAndStructures'; PR='LanguageGuide/Properties'; IH='LanguageGuide/Inheritance'; PT='LanguageGuide/Protocols'; CL='LanguageGuide/Closures'; EH='LanguageGuide/ErrorHandling'; GE='LanguageGuide/Generics'; CT='LanguageGuide/CollectionTypes'; EX='LanguageGuide/Extensions'; IN='LanguageGuide/Initialization'; EN='LanguageGuide/Enumerations'
OPS="struct __Input: Decodable { let ops: [String] }\n"
P=[]
P.append(dict(id='checkpoint-6-car', title='Checkpoint 6: A Car Struct', topic='Structs', concepts=['mutating','private-set','encapsulation'], docs=[('Structures and Classes', CS)],
 sig='func driveCar(maxGears: Int, changes: [Int]) -> [String]',
 statement="""Checkpoint 6: create `struct Car` with a constant `model`, a constant `seats`, a constant `maxGears` and a **`private(set)`** current `gear` starting at 1, plus `mutating func changeGear(by delta: Int) -> Bool` that refuses to go below 1 or above `maxGears`.

 Apply each delta and log `"gear <n>"` or `"refused at <n>"`.""",
 solution="""
 struct Car {
     let model: String
     let seats: Int
     let maxGears: Int
     private(set) var gear = 1

     mutating func changeGear(by delta: Int) -> Bool {
         let next = gear + delta
         guard (1...maxGears).contains(next) else { return false }
         gear = next
         return true
     }
 }

 func driveCar(maxGears: Int, changes: [Int]) -> [String] {
     var car = Car(model: "Swiftmobile", seats: 4, maxGears: maxGears)
     return changes.map { car.changeGear(by: $0) ? "gear \\(car.gear)" : "refused at \\(car.gear)" }
 }
 """,
 explain="""Constants model facts that never change; `private(set)` exposes `gear` for reading while forcing every change through `changeGear`, which enforces the invariant. Because the struct mutates itself, the method is `mutating` and the car must be a `var`.""",
 hints=("Which properties should never change after creation, and which must be protected from outside writes?","Use `let` for model/seats/maxGears and `private(set) var gear = 1`; validate inside a `mutating` method.","`guard (1...maxGears).contains(gear + delta) else { return false }`."),
 tests=[({'maxGears':5,'changes':[1,1,-3,10]},['gear 2','gear 3','refused at 3','refused at 3']), {'maxGears':1,'changes':[1,-1]}, {'maxGears':6,'changes':[]}]))
P.append(dict(id='checkpoint-7-animals', title='Checkpoint 7: Animal Class Hierarchy', topic='Classes & inheritance', concepts=['inheritance','overloading-overriding','initializers'], docs=[('Inheritance', IH)],
 sig='func zoo(_ specs: [String]) -> [String]',
 statement="""Checkpoint 7: `class Animal` with `legs: Int`. Subclasses `Dog` (overrides `speak()` → `"Woof"`) with sub-subclasses `Corgi` (`"Yip"`) and `Poodle` (`"Bark bark"`); `Cat` adds `isTame: Bool` via its own initialiser (and `speak()` → `"Meow"` or `"Hiss"` when not tame), with subclasses `Persian` and `Lion` (`"Roar"`).

 Specs: `corgi`, `poodle`, `dog`, `persian`, `lion`, `wildcat` (a `Cat` with `isTame: false`). Return `"<speak()> (<legs> legs)"` for each.""",
 solution="""
 class Animal {
     let legs: Int
     init(legs: Int) { self.legs = legs }
     func speak() -> String { "..." }
 }

 class Dog: Animal {
     init() { super.init(legs: 4) }
     override func speak() -> String { "Woof" }
 }
 final class Corgi: Dog { override func speak() -> String { "Yip" } }
 final class Poodle: Dog { override func speak() -> String { "Bark bark" } }

 class Cat: Animal {
     let isTame: Bool
     init(isTame: Bool) {
         self.isTame = isTame
         super.init(legs: 4)
     }
     override func speak() -> String { isTame ? "Meow" : "Hiss" }
 }
 final class Persian: Cat { init() { super.init(isTame: true) } }
 final class Lion: Cat {
     init() { super.init(isTame: false) }
     override func speak() -> String { "Roar" }
 }

 func zoo(_ specs: [String]) -> [String] {
     let animals: [Animal] = specs.compactMap {
         switch $0 {
         case "corgi": Corgi()
         case "poodle": Poodle()
         case "dog": Dog()
         case "persian": Persian()
         case "lion": Lion()
         case "wildcat": Cat(isTame: false)
         default: nil
         }
     }
     return animals.map { "\\($0.speak()) (\\($0.legs) legs)" }
 }
 """,
 explain="""Each level adds or overrides behaviour; `Cat`'s designated init sets its own property **before** `super.init` (two-phase initialisation). The array is `[Animal]`, but each call dispatches to the runtime type.""",
 hints=("Model the tree: Animal → Dog → Corgi/Poodle, Animal → Cat → Persian/Lion.","`Cat` needs `init(isTame:)` that sets `isTame` before calling `super.init(legs: 4)`; subclasses call it with fixed values.","Build `[Animal]` with a `switch` in `compactMap`, then map to `\"\\($0.speak()) (\\($0.legs) legs)\"`."),
 tests=[({'specs':['corgi','lion','wildcat','persian']},['Yip (4 legs)','Roar (4 legs)','Hiss (4 legs)','Meow (4 legs)']), {'specs':[]}, {'specs':['dog','poodle','unicorn']}]))
P.append(dict(id='checkpoint-8-building', title='Checkpoint 8: Building Protocol', topic='Protocols', concepts=['protocols','protocol-extension'], docs=[('Protocols', PT)],
 sig='func listings(_ specs: [[Int]]) -> [String]',
 statement="""Checkpoint 8: `protocol Building` requires `rooms: Int`, `cost: Int`, `agent: String` and `func salesSummary() -> String`. Provide the summary in a **protocol extension**: `"<kind> with <rooms> rooms, $<cost>, sold by <agent>"`, where `kind` is another requirement.

 Conform `House` (agent `"Ana"`) and `Office` (agent `"Bo"`). Specs are `[type, rooms, cost]` with type 0 = house, 1 = office.""",
 solution="""
 protocol Building {
     var kind: String { get }
     var rooms: Int { get }
     var cost: Int { get }
     var agent: String { get }
     func salesSummary() -> String
 }

 extension Building {
     func salesSummary() -> String { "\\(kind) with \\(rooms) rooms, $\\(cost), sold by \\(agent)" }
 }

 struct House: Building {
     let rooms: Int, cost: Int
     var kind: String { "House" }
     var agent: String { "Ana" }
 }

 struct Office: Building {
     let rooms: Int, cost: Int
     var kind: String { "Office" }
     var agent: String { "Bo" }
 }

 func listings(_ specs: [[Int]]) -> [String] {
     specs.map { s -> String in
         let b: any Building = s[0] == 0 ? House(rooms: s[1], cost: s[2]) : Office(rooms: s[1], cost: s[2])
         return b.salesSummary()
     }
 }
 """,
 explain="""The protocol states *what* every building has; the extension supplies *how* to summarise, so conforming types get it for free. Computed properties can satisfy `{ get }` requirements.""",
 hints=("A protocol lists requirements; an extension can implement a requirement for everyone.","Add a `kind` requirement and implement `salesSummary()` once in `extension Building`.","Conform `House`/`Office` with stored `rooms`/`cost` and computed `kind`/`agent`."),
 tests=[({'specs':[[0,3,250000],[1,20,1200000]]},['House with 3 rooms, $250000, sold by Ana','Office with 20 rooms, $1200000, sold by Bo']), {'specs':[]}]))
P.append(dict(id='checkpoint-9-optional-random', title='Checkpoint 9: One-Line Optional Default', topic='Optionals', concepts=['nil-coalescing','optional-chaining'], docs=[('Optional Chaining', 'LanguageGuide/OptionalChaining')],
 sig='func pickNumber(_ numbers: [Int]?, index: Int) -> Int',
 statement="""Checkpoint 9 asks for a one-line function that accepts an optional array of integers and returns a random element — or a random number from 1 to 100 if the array is nil or empty. To keep tests deterministic, return the element at `index % count` instead of a random one, or `100` as the fallback — **in one expression**, no `if`.""",
 solution="func pickNumber(_ numbers: [Int]?, index: Int) -> Int {\n    numbers.flatMap { $0.isEmpty ? nil : $0[abs(index) % $0.count] } ?? 100\n}\n",
 explain="""The original Checkpoint 9 answer is `numbers?.randomElement() ?? Int.random(in: 1...100)` — `randomElement()` already returns `nil` for an empty array. Here `Optional.flatMap` does the same job deterministically.""",
 hints=("`??` supplies the fallback; you need one expression that's nil for both a nil and an empty array.","`Optional.flatMap { … }` lets you return `nil` for the empty case too.","`numbers.flatMap { $0.isEmpty ? nil : $0[abs(index) % $0.count] } ?? 100`."),
 tests=[({'numbers':[4,8,15],'index':4},8), ({'numbers':None,'index':0},100), ({'numbers':[],'index':3},100), {'numbers':[7],'index':-5}]))
P.append(dict(id='stdlib-my-map', title='Inside the Standard Library: map', topic='Standard library internals', concepts=['map-filter-reduce','generics','rethrows'], docs=[('Sequence.map', 'https://developer.apple.com/documentation/swift/sequence/map(_:)')],
 sig='func mapDemo(_ numbers: [Int]) -> [String]',
 statement="""Re-implement `map` as `extension Sequence { func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T] }` — reserving capacity with `underestimatedCount`. `mapDemo` returns `numbers.myMap { "#\\($0 * 2)" }`.""",
 solution="""
 extension Sequence {
     func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T] {
         var result: [T] = []
         result.reserveCapacity(underestimatedCount)
         for element in self { result.append(try transform(element)) }
         return result
     }
 }

 func mapDemo(_ numbers: [Int]) -> [String] {
     numbers.myMap { "#\\($0 * 2)" }
 }
 """,
 explain="""This is essentially the real implementation: generic over the output type, `rethrows` so non-throwing closures need no `try`, and `underestimatedCount` to avoid reallocation. Paul's *Inside the Standard Library* walks through the actual source.""",
 hints=("`map` is a generic method on `Sequence`: `Element` in, `T` out.","Loop over `self`, append `try transform(element)`, and mark the method `rethrows`.","`result.reserveCapacity(underestimatedCount)` before the loop."),
 tests=[({'numbers':[1,2,3]},['#2','#4','#6']), {'numbers':[]}, {'numbers':[-5]}]))
P.append(dict(id='stdlib-my-compactmap', title='Inside the Standard Library: compactMap', topic='Standard library internals', concepts=['compactmap-flatmap','generics'], docs=[('Sequence.compactMap', 'https://developer.apple.com/documentation/swift/sequence/compactmap(_:)')],
 sig='func compactDemo(_ tokens: [String]) -> [Int]',
 statement="""Implement `myCompactMap` on `Sequence`: transform each element with a closure returning `T?` and keep only non-nil results. `compactDemo` parses integers from `tokens` with it.""",
 solution="""
 extension Sequence {
     func myCompactMap<T>(_ transform: (Element) throws -> T?) rethrows -> [T] {
         var result: [T] = []
         for element in self {
             if let value = try transform(element) { result.append(value) }
         }
         return result
     }
 }

 func compactDemo(_ tokens: [String]) -> [Int] {
     tokens.myCompactMap { Int($0) }
 }
 """,
 explain="""`compactMap` is `map` + unwrapping: `if let` keeps only the present values. Before Swift 4.1 this was spelled `flatMap`, which is why you still see that in old code.""",
 hints=("It's `map`, but the closure returns an optional.","Loop, call the transform, and append only when `if let value = try transform(element)` succeeds.","`tokens.myCompactMap { Int($0) }`."),
 tests=[({'tokens':['1','x','3']},[1,3]), {'tokens':[]}, {'tokens':['a','b']}, {'tokens':['-7','007']}]))
P.append(dict(id='stdlib-my-flatmap', title='Inside the Standard Library: flatMap', topic='Standard library internals', concepts=['compactmap-flatmap','generics','generic-constraints'], docs=[('Sequence.flatMap', 'https://developer.apple.com/documentation/swift/sequence/flatmap(_:)-jo2y')],
 sig='func flatDemo(_ sentences: [String]) -> [String]',
 statement="""Implement `func myFlatMap<S: Sequence>(_ transform: (Element) throws -> S) rethrows -> [S.Element]` on `Sequence`, concatenating the sequences each element produces. `flatDemo` splits every sentence into words and flattens.""",
 solution="""
 extension Sequence {
     func myFlatMap<S: Sequence>(_ transform: (Element) throws -> S) rethrows -> [S.Element] {
         var result: [S.Element] = []
         for element in self { result.append(contentsOf: try transform(element)) }
         return result
     }
 }

 func flatDemo(_ sentences: [String]) -> [String] {
     sentences.myFlatMap { $0.split(separator: " ").map(String.init) }
 }
 """,
 explain="""The output element type is the **inner** sequence's `Element` — expressed with the associated type `S.Element`. `append(contentsOf:)` concatenates any sequence.""",
 hints=("The closure returns a whole sequence per element; you need to concatenate them.","Make the method generic over `S: Sequence` and return `[S.Element]`.","`result.append(contentsOf: try transform(element))`."),
 tests=[({'sentences':['a b','c']},['a','b','c']), {'sentences':[]}, {'sentences':['','one  two']}]))
P.append(dict(id='stdlib-my-contains', title='Inside the Standard Library: contains', topic='Standard library internals', concepts=['generic-constraints','extensions','equatable-hashable'], docs=[('Sequence.contains', 'https://developer.apple.com/documentation/swift/sequence/contains(_:)')],
 sig='func containsDemo(_ words: [String], target: String, minLength: Int) -> [Bool]',
 statement="""Implement two overloads on `Sequence`:
 - `myContains(where predicate:)` — works for any element type
 - `myContains(_ element:)` — only where `Element: Equatable`, implemented **using** the predicate version

 Return `[words.myContains(target), words.myContains { $0.count >= minLength }]`.""",
 solution="""
 extension Sequence {
     func myContains(where predicate: (Element) throws -> Bool) rethrows -> Bool {
         for element in self where try predicate(element) { return true }
         return false
     }
 }

 extension Sequence where Element: Equatable {
     func myContains(_ element: Element) -> Bool {
         myContains { $0 == element }
     }
 }

 func containsDemo(_ words: [String], target: String, minLength: Int) -> [Bool] {
     [words.myContains(target), words.myContains { $0.count >= minLength }]
 }
 """,
 explain="""The `Equatable` version only exists where `==` does — a constrained extension. Returning early on the first match gives short-circuiting, just like the real `contains`.""",
 hints=("One version takes a predicate; the other compares with `==`, which needs a constraint.","Put the equality version in `extension Sequence where Element: Equatable` and reuse the predicate version.","`for element in self where try predicate(element) { return true }`."),
 tests=[({'words':['apple','fig'],'target':'fig','minLength':5},[True,True]), {'words':[],'target':'x','minLength':0}, {'words':['a'],'target':'b','minLength':2}]))
P.append(dict(id='algorithms-chunked-by', title='Swift Algorithms: chunked(on:)', topic='Algorithms package', diff='medium', concepts=['custom-collection','generics','sort-custom'], docs=[('Swift Algorithms (GitHub)', 'https://github.com/apple/swift-algorithms')],
 sig='func groupRuns(_ words: [String]) -> [[String]]',
 statement="""Paul's *Swift Algorithms* video shows `chunked(on:)`, which groups **consecutive** elements with the same key. Implement `func chunked<K: Equatable>(on key: (Element) -> K) -> [[Element]]` on `Sequence` and use it to group words by their first letter (lowercased) in input order.""",
 solution="""
 extension Sequence {
     func chunked<K: Equatable>(on key: (Element) throws -> K) rethrows -> [[Element]] {
         var chunks: [[Element]] = []
         var lastKey: K?
         for element in self {
             let k = try key(element)
             if let lastKey, lastKey == k {
                 chunks[chunks.count - 1].append(element)
             } else {
                 chunks.append([element])
             }
             lastKey = k
         }
         return chunks
     }
 }

 func groupRuns(_ words: [String]) -> [[String]] {
     words.chunked { $0.first.map { String($0).lowercased() } ?? "" }
 }
 """,
 explain="""Unlike `Dictionary(grouping:)`, chunking only groups **adjacent** runs, so order is preserved and a key can appear in several chunks. The real package returns lazy slices; this version builds arrays for clarity.""",
 hints=("Walk the sequence remembering the previous element's key.","Same key as last time → append to the last chunk; different key → start a new chunk.","`if let lastKey, lastKey == k { chunks[chunks.count - 1].append(element) } else { chunks.append([element]) }`."),
 tests=[({'words':['apple','avocado','banana','Blueberry','apricot']},[['apple','avocado'],['banana','Blueberry'],['apricot']]), {'words':[]}, {'words':['','x','']}]))
P.append(dict(id='algorithms-uniqued', title='Swift Algorithms: uniqued(on:)', topic='Algorithms package', concepts=['set-vs-array','generics','equatable-hashable'], docs=[('Swift Algorithms (GitHub)', 'https://github.com/apple/swift-algorithms')],
 sig='func uniqueByLength(_ words: [String]) -> [String]',
 statement="""Implement `func uniqued<K: Hashable>(on key: (Element) -> K) -> [Element]` keeping the first element for each key, in order. Return the words with unique **lengths**.""",
 solution="""
 extension Sequence {
     func uniqued<K: Hashable>(on key: (Element) throws -> K) rethrows -> [Element] {
         var seen = Set<K>()
         var result: [Element] = []
         for element in self where seen.insert(try key(element)).inserted {
             result.append(element)
         }
         return result
     }
 }

 func uniqueByLength(_ words: [String]) -> [String] {
     words.uniqued { $0.count }
 }
 """,
 explain="""The key projection only needs to be `Hashable`, not the element itself — so you can dedupe structs by an ID without making the whole struct Hashable.""",
 hints=("You need a set of *keys* you've already seen.","Keep an element only if inserting its key into the set succeeds.","`for element in self where seen.insert(try key(element)).inserted { result.append(element) }`."),
 tests=[({'words':['a','bb','c','dd','eee']},['a','bb','eee']), {'words':[]}, {'words':['same','sane','lane']}]))
P.append(dict(id='algorithms-windows', title='Swift Algorithms: windows & adjacentPairs', topic='Algorithms package', diff='medium', concepts=['custom-collection','half-open-range','tuples'], docs=[('Swift Algorithms (GitHub)', 'https://github.com/apple/swift-algorithms')],
 sig='func movingStats(_ values: [Int], window: Int) -> [[Int]]',
 statement="""Implement on `Collection`:
 - `func windows(ofCount k: Int) -> [SubSequence]` — every contiguous slice of length k (none if k > count)
 - `func adjacentPairs() -> [(Element, Element)]`

 Return `[moving sums over windows(ofCount: window), differences b - a over adjacentPairs]`.""",
 solution="""
 extension Collection {
     func windows(ofCount k: Int) -> [SubSequence] {
         guard k > 0, k <= count else { return [] }
         var result: [SubSequence] = []
         var start = startIndex
         var end = index(startIndex, offsetBy: k)
         while true {
             result.append(self[start..<end])
             if end == endIndex { break }
             formIndex(after: &start)
             formIndex(after: &end)
         }
         return result
     }

     func adjacentPairs() -> [(Element, Element)] {
         Array(zip(self, dropFirst()))
     }
 }

 func movingStats(_ values: [Int], window: Int) -> [[Int]] {
     [values.windows(ofCount: window).map { $0.reduce(0, +) }, values.adjacentPairs().map { $1 - $0 }]
 }
 """,
 explain="""Slices (`SubSequence`) share storage with the original, so windows are cheap. `zip(self, dropFirst())` is the classic way to pair each element with its successor.""",
 hints=("A window is a slice `self[start..<end]`; slide both indices forward together.","Use `index(_:offsetBy:)` for the first end, then `formIndex(after:)` on both each step.","`adjacentPairs` is `Array(zip(self, dropFirst()))`."),
 tests=[({'values':[1,2,3,4],'window':2},[[3,5,7],[1,1,1]]), {'values':[],'window':1}, {'values':[5],'window':2}, {'values':[3,1,4,1,5],'window':3}]))
P.append(dict(id='closures-as-parameters', title='Closures as Parameters (with Params & Returns)', topic='Closures', concepts=['closures','trailing-closure','higher-order-functions'], docs=[('Closures', CL)],
 sig='func travel(_ legs: [String]) -> [String]',
 statement="""Write `func plan(route: [String], using describe: (String, Int) -> String) -> [String]` that calls `describe(stop, legNumber)` for each stop (legs numbered from 1). Call it with a **trailing closure** returning `"Leg <n>: to <stop>"`, and a second time with shorthand `$0`/`$1` returning `"<n>-<stop>"`. Return both results concatenated.""",
 solution="""
 func plan(route: [String], using describe: (String, Int) -> String) -> [String] {
     route.enumerated().map { describe($0.element, $0.offset + 1) }
 }

 func travel(_ legs: [String]) -> [String] {
     let verbose = plan(route: legs) { stop, number in
         "Leg \\(number): to \\(stop)"
     }
     let short = plan(route: legs) { "\\($1)-\\($0)" }
     return verbose + short
 }
 """,
 explain="""A closure parameter's type is written like a function type: `(String, Int) -> String`. The caller can name the parameters (`stop, number in`) or use `$0`, `$1` in order.""",
 hints=("A closure parameter has a function type like `(String, Int) -> String`.","Inside `plan`, call `describe(stop, index + 1)` for each stop.","Second call: `plan(route: legs) { \"\\($1)-\\($0)\" }`."),
 tests=[({'legs':['Rome','Oslo']},['Leg 1: to Rome','Leg 2: to Oslo','1-Rome','2-Oslo']), {'legs':[]}]))
P.append(dict(id='returning-closures', title='Returning Closures from Functions', topic='Closures', concepts=['closures','capturing-values','functions-vs-closures'], docs=[('Closures — Capturing Values', CL)],
 sig='func discounts(_ prices: [Int], codes: [String]) -> [Int]',
 statement="""Write `func makeDiscount(code: String) -> (Int) -> Int` returning a pricing closure: `"HALF"` halves, `"TENOFF"` subtracts 10 (min 0), `"FREE"` returns 0, anything else leaves the price. Apply `codes[i]` to `prices[i]` (zip).""",
 solution="""
 func makeDiscount(code: String) -> (Int) -> Int {
     switch code {
     case "HALF": return { $0 / 2 }
     case "TENOFF": return { max(0, $0 - 10) }
     case "FREE": return { _ in 0 }
     default: return { $0 }
     }
 }

 func discounts(_ prices: [Int], codes: [String]) -> [Int] {
     zip(prices, codes).map { makeDiscount(code: $1)($0) }
 }
 """,
 explain="""The return type `(Int) -> Int` is a function type; each branch returns a different closure literal. `makeDiscount(code:)($0)` calls the returned closure immediately.""",
 hints=("A function's return type can itself be a function type: `-> (Int) -> Int`.","Switch on the code and return a different closure literal from each case.","Apply with `makeDiscount(code: code)(price)`."),
 tests=[({'prices':[100,5,40,7],'codes':['HALF','TENOFF','FREE','NOPE']},[50,0,0,7]), {'prices':[],'codes':[]}, {'prices':[1,2],'codes':['HALF']}]))
P.append(dict(id='typealias-closures', title='typealias for Closure Types', topic='Closures', concepts=['typealias','closures','escaping'], docs=[('Declarations — Type Alias Declaration', 'ReferenceManual/Declarations')],
 sig='func validateAll(_ inputs: [String]) -> [String]',
 statement="""Declare `typealias Validator = @Sendable (String) -> String?` (returns an error message or nil) — try it without `@Sendable` first and read Swift 6's error. Build `let validators: [Validator]` checking: non-empty (`"empty"`), max 10 characters (`"too long"`), no spaces (`"has spaces"`). For each input return the **first** error or `"ok"`.""",
 solution="""
 typealias Validator = @Sendable (String) -> String?

 let validators: [Validator] = [
     { $0.isEmpty ? "empty" : nil },
     { $0.count > 10 ? "too long" : nil },
     { $0.contains(" ") ? "has spaces" : nil },
 ]

 func validateAll(_ inputs: [String]) -> [String] {
     inputs.map { input in validators.lazy.compactMap { $0(input) }.first ?? "ok" }
 }
 """,
 explain="""`typealias` names a complex function type once. `lazy.compactMap { … }.first` runs validators only until the first failure. **Swift 6 gotcha:** a global `let` must be `Sendable`, and a plain function type isn't — so `[(String) -> String?]` at global scope is an error (*not concurrency-safe*). Marking the function type `@Sendable` promises the closures don't capture mutable shared state, which makes the array safe to share across threads.""",
 hints=("Name the function type once with `typealias`, then store several closures in a global array — Swift 6 will want that function type to be `@Sendable`.","Each validator returns `String?`; the first non-nil message wins.","`validators.lazy.compactMap { $0(input) }.first ?? \"ok\"`."),
 tests=[({'inputs':['swift','','hi there','averyveryverylong']},['ok','empty','has spaces','too long']), {'inputs':[]}]))
P.append(dict(id='models-sort-filter-map', title='Sort, Filter & Map on Models', topic='Closures', concepts=['map-filter-reduce','sort-custom','key-paths'], docs=[('Closures', CL)],
 sig='func topVerified(_ rows: [[String]]) -> [String]',
 statement="""Swiftful Thinking's sort/filter/map lesson on a user model. Rows are `[name, points, isVerified]`. Decode to `struct UserModel`, keep verified users with at least 50 points, sort by points (desc) then name, and map to `"<name> (<points>)"`.""",
 solution="""
 struct UserModel {
     let name: String
     let points: Int
     let isVerified: Bool
 }

 func topVerified(_ rows: [[String]]) -> [String] {
     rows
         .map { UserModel(name: $0[0], points: Int($0[1]) ?? 0, isVerified: $0[2] == "true") }
         .filter { $0.isVerified && $0.points >= 50 }
         .sorted { ($1.points, $0.name) < ($0.points, $1.name) }
         .map { "\\($0.name) (\\($0.points))" }
 }
 """,
 explain="""Transform raw data into typed models first, then chain `filter` → `sorted` → `map`. The tuple comparison sorts points descending and names ascending in one expression.""",
 hints=("Decode rows into a struct before doing anything else.","`filter` on two conditions, then `sorted` with a tuple comparison.","`.sorted { ($1.points, $0.name) < ($0.points, $1.name) }`."),
 tests=[({'rows':[['ana','90','true'],['bo','95','false'],['cy','90','true'],['di','10','true']]},['ana (90)','cy (90)']), {'rows':[]}]))
P.append(dict(id='oop-bank-accounts', title='Object-Oriented Swift: Accounts', topic='Classes & inheritance', diff='medium', concepts=['inheritance','encapsulation','struct-vs-class'], docs=[('Inheritance', IH)],
 sig='func bank(_ ops: [String]) -> [String]',
 statement="""Swiftful's *What is Object Oriented Programming for Swift*. `class Account` has `let id: String`, a `private(set) var balance` and `func withdraw(_:) -> Bool`. `final class SavingsAccount: Account` overrides `withdraw` to refuse if the balance would drop below 100. Both have `deposit(_:)`.

 Ops: `open <id> <checking|savings>`, `dep <id> <n>`, `wd <id> <n>`, `show <id>`. For each op output `"ok"`, `"refused"`, `"no account"` or (for `show`) `"<id>: <balance>"`. Accounts live in `[String: Account]`.""",
 solution="""
 class Account {
     let id: String
     private(set) var balance = 0
     init(id: String) { self.id = id }
     func deposit(_ amount: Int) { balance += amount }
     func withdraw(_ amount: Int) -> Bool {
         guard amount <= balance else { return false }
         balance -= amount
         return true
     }
 }

 final class SavingsAccount: Account {
     override func withdraw(_ amount: Int) -> Bool {
         guard balance - amount >= 100 else { return false }
         return super.withdraw(amount)
     }
 }

 func bank(_ ops: [String]) -> [String] {
     var accounts: [String: Account] = [:]
     return ops.map { op in
         let p = op.split(separator: " ").map(String.init)
         if p[0] == "open" {
             accounts[p[1]] = p[2] == "savings" ? SavingsAccount(id: p[1]) : Account(id: p[1])
             return "ok"
         }
         guard let account = accounts[p[1]] else { return "no account" }
         switch p[0] {
         case "dep": account.deposit(Int(p[2])!); return "ok"
         case "wd": return account.withdraw(Int(p[2])!) ? "ok" : "refused"
         default: return "\\(account.id): \\(account.balance)"
         }
     }
 }
 """,
 explain="""Classes give identity and shared state: the dictionary holds references, so `account.deposit` mutates the stored object directly (no need to write back). The override calls `super` so the base rule still applies.""",
 hints=("Classes are reference types — the dictionary stores references you can mutate through.","`SavingsAccount` overrides `withdraw` and calls `super.withdraw` after its own check.","`guard balance - amount >= 100 else { return false }; return super.withdraw(amount)`."),
 tests=[({'ops':['open a savings','dep a 150','wd a 60','wd a 50','show a','wd z 1']},['ok','ok','refused','ok','a: 100','no account']), {'ops':[]}, {'ops':['open c checking','wd c 1','dep c 5','wd c 5','show c']}]))
P.append(dict(id='localized-error', title='Custom Errors with LocalizedError', topic='Error handling', concepts=['error-handling','enums'], docs=[('LocalizedError', 'https://developer.apple.com/documentation/foundation/localizederror')],
 sig='func uploadMessages(_ sizes: [Int]) -> [String]',
 statement="""Swiftful's *Custom Errors and Alerts*: `enum UploadError: LocalizedError` with cases `emptyFile`, `tooLarge(limitMB: Int)`, `offline`, providing `errorDescription` (user-facing) and `recoverySuggestion`.

 `func upload(sizeMB: Int) throws -> String` throws `.emptyFile` for 0, `.tooLarge(limitMB: 25)` above 25, `.offline` for negative sizes, else returns `"uploaded <n>MB"`. For each size return the result or `"<errorDescription> — <recoverySuggestion>"` using `error.localizedDescription` where possible.""",
 solution="""
 import Foundation

 enum UploadError: LocalizedError {
     case emptyFile
     case tooLarge(limitMB: Int)
     case offline

     var errorDescription: String? {
         switch self {
         case .emptyFile: "The file is empty."
         case .tooLarge(let limit): "The file is larger than \\(limit) MB."
         case .offline: "You're offline."
         }
     }

     var recoverySuggestion: String? {
         switch self {
         case .emptyFile: "Choose a different file."
         case .tooLarge: "Compress the file and try again."
         case .offline: "Check your connection."
         }
     }
 }

 func upload(sizeMB: Int) throws -> String {
     if sizeMB < 0 { throw UploadError.offline }
     if sizeMB == 0 { throw UploadError.emptyFile }
     if sizeMB > 25 { throw UploadError.tooLarge(limitMB: 25) }
     return "uploaded \\(sizeMB)MB"
 }

 func uploadMessages(_ sizes: [Int]) -> [String] {
     sizes.map { size in
         do {
             return try upload(sizeMB: size)
         } catch let error as LocalizedError {
             return "\\(error.localizedDescription) — \\(error.recoverySuggestion ?? "")"
         } catch {
             return error.localizedDescription
         }
     }
 }
 """,
 explain="""`LocalizedError` lets errors carry user-facing text; `localizedDescription` uses your `errorDescription`. SwiftUI's `.alert(isPresented:error:)` reads these properties, which is how Swiftful wires errors into alerts.""",
 hints=("`LocalizedError` adds `errorDescription` and `recoverySuggestion` to an error type.","Switch on `self` in computed properties to provide text per case (including associated values).","`catch let error as LocalizedError { \"\\(error.localizedDescription) — \\(error.recoverySuggestion ?? \"\")\" }`."),
 tests=[({'sizes':[5,0,30,-1]},['uploaded 5MB','The file is empty. — Choose a different file.','The file is larger than 25 MB. — Compress the file and try again.',"You're offline. — Check your connection."]), {'sizes':[]}, {'sizes':[25,26]}]))
P.append(dict(id='result-map-flatmap', title='Chaining Result with map & flatMap', topic='Error handling', diff='medium', concepts=['result-type','error-handling','compactmap-flatmap'], docs=[('Result', 'https://developer.apple.com/documentation/swift/result')],
 sig='func pipeline(_ inputs: [String]) -> [String]',
 statement="""Build a `Result` pipeline without `do`/`catch`:
 1. `parse(_:) -> Result<Int, PipelineError>` — `.notANumber` if not an integer
 2. `.flatMap(validate)` — `.negative` if < 0
 3. `.map { $0 * $0 }`
 4. `.mapError { … }` — no, keep errors; finally `switch` to `"ok <value>"` / `"error <case>"`.""",
 solution="""
 enum PipelineError: Error { case notANumber, negative }

 func parse(_ s: String) -> Result<Int, PipelineError> {
     Int(s).map(Result.success) ?? .failure(.notANumber)
 }

 func validate(_ n: Int) -> Result<Int, PipelineError> {
     n < 0 ? .failure(.negative) : .success(n)
 }

 func pipeline(_ inputs: [String]) -> [String] {
     inputs.map { input in
         switch parse(input).flatMap(validate).map({ $0 * $0 }) {
         case .success(let value): "ok \\(value)"
         case .failure(let error): "error \\(error)"
         }
     }
 }
 """,
 explain="""`Result.map` transforms the success value; `flatMap` chains a step that can itself fail; the first failure short-circuits the rest. `Int(s).map(Result.success)` passes an enum case as a function.""",
 hints=("`Result` has `map` (transform success) and `flatMap` (chain another Result-returning step).","`parse(input).flatMap(validate).map { $0 * $0 }`, then switch once at the end.","`Int(s).map(Result.success) ?? .failure(.notANumber)` builds the first Result."),
 tests=[({'inputs':['4','x','-2']},['ok 16','error notANumber','error negative']), {'inputs':[]}, {'inputs':['0','3037000499']}]))
P.append(dict(id='identifiable-dedupe', title='Identifiable Models & Updates by ID', topic='Protocols', concepts=['protocols','equatable-hashable','uuid'], docs=[('Identifiable', 'https://developer.apple.com/documentation/swift/identifiable')],
 sig='func applyEdits(_ ops: [String]) -> [String]',
 statement="""`struct Todo: Identifiable, Equatable` with `id: Int`, `title`, `isDone`. Keep a `[Todo]` and apply ops: `add <id> <title>` (ignore duplicate ids), `toggle <id>`, `rename <id> <title>`, `delete <id>`. Use `firstIndex(where: { $0.id == id })` and mutate **in place**. Return `"<id>:<title>:<done|todo>"` for the final list.""",
 solution="""
 struct Todo: Identifiable, Equatable {
     let id: Int
     var title: String
     var isDone = false
 }

 func applyEdits(_ ops: [String]) -> [String] {
     var todos: [Todo] = []
     for op in ops {
         let p = op.split(separator: " ", maxSplits: 2).map(String.init)
         guard p.count >= 2, let id = Int(p[1]) else { continue }
         let index = todos.firstIndex { $0.id == id }
         switch (p[0], index) {
         case ("add", nil) where p.count == 3: todos.append(Todo(id: id, title: p[2]))
         case ("toggle", let i?): todos[i].isDone.toggle()
         case ("rename", let i?) where p.count == 3: todos[i].title = p[2]
         case ("delete", let i?): todos.remove(at: i)
         default: break
         }
     }
     return todos.map { "\\($0.id):\\($0.title):\\($0.isDone ? "done" : "todo")" }
 }
 """,
 explain="""`Identifiable` just requires an `id`; SwiftUI's `List`/`ForEach` use it to track rows. Mutating `todos[i].isDone` writes through the array subscript — no need to copy out and back. `case ("toggle", let i?)` matches only when the index exists.""",
 hints=("Find the element's index by id, then mutate through the subscript.","Switch on `(command, index)` — `let i?` matches only when the item exists, `nil` when it doesn't.","`case (\"toggle\", let i?): todos[i].isDone.toggle()`."),
 tests=[({'ops':['add 1 milk','add 2 eggs','toggle 1','rename 2 bread','add 1 dup','delete 3']},['1:milk:done','2:bread:todo']), {'ops':[]}, {'ops':['add 5 a b c','delete 5','toggle 5']}]))
P.append(dict(id='comparable-enum-synthesis', title='Synthesised Comparable Enums', topic='Enums', concepts=['comparable','enums','case-iterable'], docs=[('Comparable', 'https://developer.apple.com/documentation/swift/comparable')],
 sig='func triage(_ tickets: [String]) -> [String]',
 statement="""`enum Priority: Comparable, CaseIterable { case low, medium, high, critical }` — Swift synthesises `<` from **declaration order**. Tickets are `"<priority> <title>"`; sort by priority descending then title ascending, and return `"[PRIORITY] title"` (uppercased case name).""",
 solution="""
 enum Priority: String, Comparable, CaseIterable {
     case low, medium, high, critical

     static func < (a: Priority, b: Priority) -> Bool {
         allCases.firstIndex(of: a)! < allCases.firstIndex(of: b)!
     }
 }

 func triage(_ tickets: [String]) -> [String] {
     tickets
         .compactMap { t -> (Priority, String)? in
             let p = t.split(separator: " ", maxSplits: 1).map(String.init)
             guard p.count == 2, let priority = Priority(rawValue: p[0]) else { return nil }
             return (priority, p[1])
         }
         .sorted { ($1.0, $0.1) < ($0.0, $1.1) }
         .map { "[\\($0.0.rawValue.uppercased())] \\($0.1)" }
 }
 """,
 explain="""Enums **without** raw values get `Comparable` synthesised from case order. With a `String` raw value (as here, for parsing) you must write `<` yourself — using `allCases` order keeps it in sync with the declaration.""",
 hints=("Enum cases can be compared by declaration order.","With a `String` raw value you need a custom `<` — `allCases.firstIndex(of:)` gives each case's order.","Sort tuples with `($1.0, $0.1) < ($0.0, $1.1)` for priority desc, title asc."),
 tests=[({'tickets':['low typo','critical outage','high login','critical backup']},['[CRITICAL] backup','[CRITICAL] outage','[HIGH] login','[LOW] typo']), {'tickets':[]}, {'tickets':['urgent x','medium y']}]))
P.append(dict(id='dictionary-transforms', title='mapValues, compactMapValues & grouping', topic='Dictionaries', concepts=['dictionary-basics','compactmap-flatmap'], docs=[('Dictionary', 'https://developer.apple.com/documentation/swift/dictionary')],
 sig='func settings(_ raw: [String: String]) -> [String: Int]',
 statement="""Clean a raw settings dictionary: parse values to `Int` dropping anything unparsable (`compactMapValues`), then double every value (`mapValues`), then keep keys that don't start with `"_"` (`filter`).""",
 solution="""
 func settings(_ raw: [String: String]) -> [String: Int] {
     raw.compactMapValues { Int($0) }
         .mapValues { $0 * 2 }
         .filter { !$0.key.hasPrefix("_") }
 }
 """,
 explain="""`mapValues` and `compactMapValues` keep the keys and avoid rehashing; plain `map` on a dictionary returns an **array** of tuples instead.""",
 hints=("Dictionaries have value-only transforms that keep their keys.","`compactMapValues` drops values whose transform returns nil.","`raw.compactMapValues { Int($0) }.mapValues { $0 * 2 }.filter { !$0.key.hasPrefix(\"_\") }`."),
 tests=[({'raw':{'volume':'5','_debug':'1','theme':'dark'}},{'volume':10}), {'raw':{}}, {'raw':{'a':'-3','b':'x'}}]))
P.append(dict(id='custom-string-interpolation', title='Extending String Interpolation', topic='Strings', diff='medium', concepts=['string-interpolation','extensions'], docs=[('DefaultStringInterpolation', 'https://developer.apple.com/documentation/swift/defaultstringinterpolation')],
 sig='func receipts(_ cents: [Int]) -> [String]',
 statement="""Extend `String.StringInterpolation` with `mutating func appendInterpolation(cents value: Int)` so `"Total: \\(cents: 1234)"` produces `"Total: $12.34"` (negatives as `-$0.50`). Map each amount to `"Total: \\(cents: amount)"`.""",
 solution="""
 extension String.StringInterpolation {
     mutating func appendInterpolation(cents value: Int) {
         let sign = value < 0 ? "-" : ""
         let m = value.magnitude
         let fraction = m % 100
         appendLiteral("\\(sign)$\\(m / 100).\\(fraction < 10 ? "0" : "")\\(fraction)")
     }
 }

 func receipts(_ cents: [Int]) -> [String] {
     cents.map { "Total: \\(cents: $0)" }
 }
 """,
 explain="""Every `\\(…)` calls an `appendInterpolation` overload, so adding a labelled overload creates new interpolation syntax — a type-safe alternative to format strings.""",
 hints=("Each `\\(…)` segment calls an `appendInterpolation` method you can overload.","Extend `String.StringInterpolation` with a `mutating func appendInterpolation(cents value: Int)`.","Inside, format the text and call `appendLiteral(…)`."),
 tests=[({'cents':[1234,-50,7]},['Total: $12.34','Total: -$0.50','Total: $0.07']), {'cents':[]}]))
P.append(dict(id='predict-swift-wtf', title='Predict: Swift WTF Moments', topic='Swift quirks', mode='predict', diff='medium', concepts=['strings-are-collections','value-vs-reference','integer-overflow'], docs=[('The Basics', TB if False else 'LanguageGuide/TheBasics')],
 statement="""Inspired by Paul Hudson's *Swift WTF – Surprising behaviors while learning Swift*. Predict each line — every one surprises newcomers.""",
 snippet="""
 let a = [1, 2, 3]
 var b = a
 b[0] = 99
 print(a[0], b[0])
 print("👨‍👩‍👧".count, "👨‍👩‍👧".utf16.count)
 print(Int8.max &+ 1)
 print(-7 % 3, 7.5.truncatingRemainder(dividingBy: 2))
 print([3, 1, 2].sorted() == [1, 2, 3], [1, 2].lexicographicallyPrecedes([1, 3]))
 let optionalOptional: Int?? = .some(nil)
 print(optionalOptional == nil, optionalOptional! == nil)
 print(String(describing: 0.1 + 0.2))
 """,
 explain="""Value semantics mean `b` is an independent copy; a family emoji is one `Character` but 8 UTF-16 code units; `Int8.max &+ 1` wraps to `-128`; `%` keeps the dividend's sign and `Double` needs `truncatingRemainder`. Arrays are `Equatable` but **not** `Comparable` — `[1, 2] < [1, 3]` doesn't compile, so ordering uses `lexicographicallyPrecedes`. `Int??` distinguishes "no value" (`nil`) from "a value that is itself nil" (`.some(nil)`). And binary floating point can't represent 0.1 exactly.""",
 hints=("Arrays are values; emoji families are single characters; `&+` wraps.","`.some(nil)` is not equal to `nil` at the outer level — but its unwrapped value is.","`0.1 + 0.2` prints `0.30000000000000004`.")))
P.append(dict(id='class-copying-predict', title='Predict: Arrays of Classes vs Structs', topic='Value types', mode='predict', concepts=['value-vs-reference','copy-on-write'], docs=[('Structures and Classes', CS)],
 statement="Predict the output. Copying an array copies its elements — but what is an element when it's a class?",
 snippet="""
 final class Box { var value: Int; init(_ v: Int) { value = v } }
 struct Cell { var value: Int }

 let boxes = [Box(1), Box(2)]
 var boxesCopy = boxes
 boxesCopy[0].value = 100
 boxesCopy.append(Box(3))

 let cells = [Cell(value: 1), Cell(value: 2)]
 var cellsCopy = cells
 cellsCopy[0].value = 100

 print(boxes.map(\\.value), boxesCopy.map(\\.value))
 print(cells.map(\\.value), cellsCopy.map(\\.value))
 print(boxes[0] === boxesCopy[0], boxes.count, boxesCopy.count)
 """,
 explain="""Copying an array of classes copies the **references**: both arrays point to the same `Box` objects, so mutating one box is visible through both — but appending only changes one array. Arrays of structs copy the values themselves.""",
 hints=("The array itself is copied; its class elements are references.","Mutating `boxesCopy[0].value` changes the shared object; `append` changes only the copy.","Line 1: `[100, 2] [100, 2, 3]`.")))
P.append(dict(id='self-instance', title='Referring to the Current Instance', topic='Structs', concepts=['self-usage','initializers','mutating'], docs=[('Methods — The self Property', 'LanguageGuide/Methods')],
 sig='func vectors(_ pairs: [[Int]]) -> [String]',
 statement="""`struct Vector { var x: Int; var y: Int }` with:
 - `init(x: Int, y: Int)` written by hand, using `self.x = x`
 - `func isEqual(to other: Vector) -> Bool` comparing `self` with `other`
 - `mutating func flip() { self = Vector(x: y, y: x) }` — assigning a whole new value to `self`

 For each pair create a vector, flip it, and return `"(x, y) same:<isEqual(to: original)>"`.""",
 solution="""
 struct Vector {
     var x: Int
     var y: Int

     init(x: Int, y: Int) {
         self.x = x
         self.y = y
     }

     func isEqual(to other: Vector) -> Bool {
         self.x == other.x && self.y == other.y
     }

     mutating func flip() {
         self = Vector(x: y, y: x)
     }
 }

 func vectors(_ pairs: [[Int]]) -> [String] {
     pairs.map { p in
         let original = Vector(x: p[0], y: p[1])
         var v = original
         v.flip()
         return "(\\(v.x), \\(v.y)) same:\\(v.isEqual(to: original))"
     }
 }
 """,
 explain="""`self.x = x` disambiguates a property from a parameter with the same name. In a `mutating` method of a value type you can even replace `self` entirely — impossible for classes.""",
 hints=("`self.x` means \"my property x\" when a parameter is also called `x`.","In a `mutating` struct method, `self` is assignable.","`mutating func flip() { self = Vector(x: y, y: x) }`."),
 tests=[({'pairs':[[1,2],[3,3]]},['(2, 1) same:false','(3, 3) same:true']), {'pairs':[]}]))
P.append(dict(id='protocols-pop-swiftful', title='Protocols for Flexible Data Sources', topic='Protocols', diff='medium', concepts=['pop','protocols','dependency-injection'], docs=[('Protocols', PT)],
 sig='func screens(_ sources: [String]) -> [String]',
 statement="""From Swiftful's *How to use Protocols in Swift*: a view model shouldn't care where its text comes from. Define `protocol ButtonTextProtocol { var buttonText: String { get } }` and `protocol ButtonPressedProtocol { func buttonPressed() -> String }`, then `typealias ButtonDataSourceProtocol = ButtonTextProtocol & ButtonPressedProtocol`.

 Implement `DefaultDataSource` (`"Protocols are awesome!"`, pressed → `"default pressed"`) and `AlternativeDataSource` (`"Protocols are lame."`, pressed → `"alternative pressed"`). `struct ScreenModel` takes an `any ButtonDataSourceProtocol`. For each source name (`default`/`alternative`) return `"<text> | <pressed>"`.""",
 solution="""
 protocol ButtonTextProtocol { var buttonText: String { get } }
 protocol ButtonPressedProtocol { func buttonPressed() -> String }
 typealias ButtonDataSourceProtocol = ButtonTextProtocol & ButtonPressedProtocol

 struct DefaultDataSource: ButtonDataSourceProtocol {
     var buttonText: String { "Protocols are awesome!" }
     func buttonPressed() -> String { "default pressed" }
 }

 struct AlternativeDataSource: ButtonDataSourceProtocol {
     var buttonText: String { "Protocols are lame." }
     func buttonPressed() -> String { "alternative pressed" }
 }

 struct ScreenModel {
     let dataSource: any ButtonDataSourceProtocol
     func render() -> String { "\\(dataSource.buttonText) | \\(dataSource.buttonPressed())" }
 }

 func screens(_ sources: [String]) -> [String] {
     sources.map { name in
         let source: any ButtonDataSourceProtocol = name == "alternative" ? AlternativeDataSource() : DefaultDataSource()
         return ScreenModel(dataSource: source).render()
     }
 }
 """,
 explain="""Small protocols composed with `&` let each consumer ask for exactly what it needs (interface segregation), and swapping the data source requires no change to `ScreenModel` — the basis of dependency injection and mocking.""",
 hints=("Two small protocols, combined into one requirement with `&`.","`typealias ButtonDataSourceProtocol = ButtonTextProtocol & ButtonPressedProtocol`, then inject it into `ScreenModel`.","`ScreenModel(dataSource: source).render()` for each name."),
 tests=[({'sources':['default','alternative']},['Protocols are awesome! | default pressed','Protocols are lame. | alternative pressed']), {'sources':[]}]))
P.append(dict(id='failable-throwing-init', title='Throwing Initialisers vs Failable', topic='Structs', diff='medium', concepts=['failable-init','initializers','error-handling'], docs=[('Initialization — Failable Initializers', IN)],
 sig='func makeEmails(_ inputs: [String]) -> [String]',
 statement="""Write `struct Email` two ways:
 - `init?(_ raw: String)` — returns nil if invalid
 - `init(validating raw: String) throws` — throws `EmailError.missingAt`, `.emptyUser` or `.emptyDomain`

 Valid = exactly one `@`, non-empty parts. For each input return `"<email> ok"` using the failable init, else the error case name from the throwing init.""",
 solution="""
 enum EmailError: Error { case missingAt, emptyUser, emptyDomain }

 struct Email {
     let value: String

     init(validating raw: String) throws {
         let parts = raw.split(separator: "@", omittingEmptySubsequences: false)
         guard parts.count == 2 else { throw EmailError.missingAt }
         guard !parts[0].isEmpty else { throw EmailError.emptyUser }
         guard !parts[1].isEmpty else { throw EmailError.emptyDomain }
         value = raw.lowercased()
     }

     init?(_ raw: String) {
         guard let email = try? Email(validating: raw) else { return nil }
         self = email
     }
 }

 func makeEmails(_ inputs: [String]) -> [String] {
     inputs.map { raw in
         if let email = Email(raw) { return "\\(email.value) ok" }
         do { _ = try Email(validating: raw); return "?" } catch { return "\\(error)" }
     }
 }
 """,
 explain="""A failable `init?` says *whether* construction worked; a throwing `init` also says *why*. Here the failable one reuses the throwing one via `try?` and assigns `self` (allowed for value types).""",
 hints=("`init?` can only say \"no\"; a throwing init can say *why*.","Validate in the throwing init; the failable init can call it with `try?` and assign `self`.","`guard let email = try? Email(validating: raw) else { return nil }; self = email`."),
 tests=[({'inputs':['Ana@Mail.com','nope','@x.io','a@','a@b@c']},['ana@mail.com ok','missingAt','emptyUser','emptyDomain','missingAt']), {'inputs':[]}]))
P.append(dict(id='enum-computed-properties', title='Enums with Computed Properties & Static Members', topic='Enums', concepts=['enums','computed-properties','static-properties'], docs=[('Enumerations', EN)],
 sig='func planetFacts(_ names: [String]) -> [String]',
 statement="""`enum Planet: String, CaseIterable` with cases `mercury…neptune`. Add computed `index` (1-based order), `isInner` (first four), a `static var giants: [Planet]` (jupiter, saturn, uranus, neptune) and a `static func named(_:) -> Planet?` that's case-insensitive.

 For each name return `"<name> #<index> inner:<Bool> giant:<Bool>"` or `"unknown"`.""",
 solution="""
 enum Planet: String, CaseIterable {
     case mercury, venus, earth, mars, jupiter, saturn, uranus, neptune

     var index: Int { Planet.allCases.firstIndex(of: self)! + 1 }
     var isInner: Bool { index <= 4 }
     static var giants: [Planet] { [.jupiter, .saturn, .uranus, .neptune] }
     static func named(_ name: String) -> Planet? { Planet(rawValue: name.lowercased()) }
 }

 func planetFacts(_ names: [String]) -> [String] {
     names.map { name in
         guard let p = Planet.named(name) else { return "unknown" }
         return "\\(p.rawValue) #\\(p.index) inner:\\(p.isInner) giant:\\(Planet.giants.contains(p))"
     }
 }
 """,
 explain="""Enums can hold computed properties, static members and methods — they're full types. Deriving facts from `allCases` keeps a single source of truth.""",
 hints=("Enums can have computed properties and static members, just like structs.","`index` can come from `allCases.firstIndex(of: self)`.","`static func named(_ name: String) -> Planet? { Planet(rawValue: name.lowercased()) }`."),
 tests=[({'names':['Earth','JUPITER','pluto']},['earth #3 inner:true giant:false','jupiter #5 inner:false giant:true','unknown']), {'names':[]}]))
P.append(dict(id='protocol-associated-default', title='Protocol Requirements with Associated Defaults', topic='Protocols', diff='hard', concepts=['associated-types','protocol-extension','generic-constraints'], docs=[('Generics — Associated Types', GE)],
 sig='func scoreAll(_ ints: [Int], _ words: [String]) -> [Int]',
 statement="""`protocol Scorer { associatedtype Item; func score(_ item: Item) -> Int }` plus an extension method `func total<S: Sequence>(_ items: S) -> Int where S.Element == Item`. Conform `LengthScorer` (String → count) and `ParityScorer` (Int → 2 if even else 1). Return `[ParityScorer().total(ints), LengthScorer().total(words)]`.""",
 solution="""
 protocol Scorer {
     associatedtype Item
     func score(_ item: Item) -> Int
 }

 extension Scorer {
     func total<S: Sequence>(_ items: S) -> Int where S.Element == Item {
         items.reduce(0) { $0 + score($1) }
     }
 }

 struct LengthScorer: Scorer {
     func score(_ item: String) -> Int { item.count }
 }

 struct ParityScorer: Scorer {
     func score(_ item: Int) -> Int { item.isMultiple(of: 2) ? 2 : 1 }
 }

 func scoreAll(_ ints: [Int], _ words: [String]) -> [Int] {
     [ParityScorer().total(ints), LengthScorer().total(words)]
 }
 """,
 explain="""`Item` is inferred from each conformer's `score` signature. The extension's generic `where S.Element == Item` ties any sequence to the protocol's associated type — reuse without inheritance.""",
 hints=("Each conforming type decides what `Item` is by how it writes `score`.","Write `total` once in an extension, generic over any sequence whose elements are `Item`.","`func total<S: Sequence>(_ items: S) -> Int where S.Element == Item { items.reduce(0) { $0 + score($1) } }`."),
 tests=[({'ints':[1,2,3,4],'words':['hi','swift']},[6,7]), {'ints':[],'words':[]}]))
P.append(dict(id='access-control-module', title='Access Levels in One File', topic='Access control', mode='diagnostic', concepts=['fileprivate-vs-private','access-control'], docs=[('Access Control', 'LanguageGuide/AccessControl')],
 statement="""`private` is visible to the enclosing declaration **and its extensions in the same file**; it's not visible to *other* types in the file. Write `struct Safe { private var code = 42 }`, an `extension Safe` that reads `code` (allowed), and a separate `struct Thief` whose method reads `Safe().code` (rejected). You pass when only the `Thief` access is an error.""",
 starter="struct Safe {\n    private var code = 42\n}\n\nextension Safe {\n    func peek() -> Int { code }\n}\n",
 solution="struct Safe {\n    private var code = 42\n}\n\nextension Safe {\n    func peek() -> Int { code }\n}\n\nstruct Thief {\n    func steal() -> Int { Safe().code }\n}\n",
 explain="""Since Swift 4, same-file extensions can see `private` members. Other types in the file need `fileprivate` (or `internal`). Access control is about **scope**, not about instances.""",
 hints=("An extension in the same file counts as \"inside\" for `private`.","Add a separate type that tries to read the private property.","`struct Thief { func steal() -> Int { Safe().code } }`."),
 tests=[{'name':'Other type rejected','pattern':"inaccessible due to 'private' protection level"}]))
P.append(dict(id='closure-multiple-params', title='Closures with Multiple Parameters', topic='Closures', concepts=['closures','reduce-into' if False else 'map-filter-reduce','higher-order-functions'], docs=[('Closures — Closure Expressions', CL)],
 sig='func combine(_ a: [Int], _ b: [Int], op: String) -> [Int]',
 statement="""Write `func zipWith(_ a: [Int], _ b: [Int], _ f: (Int, Int) -> Int) -> [Int]`. `combine` chooses the closure from `op`: `"add"`, `"max"`, `"pow"` (a to the power b, b ≥ 0) — passing operators directly where possible (`zipWith(a, b, +)`).""",
 solution="""
 func zipWith(_ a: [Int], _ b: [Int], _ f: (Int, Int) -> Int) -> [Int] {
     zip(a, b).map(f)
 }

 func combine(_ a: [Int], _ b: [Int], op: String) -> [Int] {
     switch op {
     case "add": zipWith(a, b, +)
     case "max": zipWith(a, b, max)
     default:
         zipWith(a, b) { base, exponent in
             (0..<max(0, exponent)).reduce(1) { acc, _ in acc * base }
         }
     }
 }
 """,
 explain="""Operators and global functions like `max` are values of function type, so `zipWith(a, b, +)` works. `zip(a, b).map(f)` passes each tuple straight into a two-parameter function.""",
 hints=("Operators such as `+` and functions such as `max` can be passed as closures.","`zip(a, b).map(f)` feeds each `(x, y)` pair into a two-argument function.","For power: `(0..<exponent).reduce(1) { acc, _ in acc * base }`."),
 tests=[({'a':[1,5,2],'b':[3,1,10],'op':'add'},[4,6,12]), {'a':[1,5],'b':[3,1],'op':'max'}, {'a':[2,3],'b':[10,0],'op':'pow'}, {'a':[],'b':[1],'op':'add'}]))
write_all(P, 'intermediate', 800)
