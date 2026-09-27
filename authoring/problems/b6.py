import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
GE='LanguageGuide/Generics'; PT='LanguageGuide/Protocols'; OT='LanguageGuide/OpaqueTypes'; AO='LanguageGuide/AdvancedOperators'; SU='LanguageGuide/Subscripts'; EN='LanguageGuide/Enumerations'; AT='ReferenceManual/Attributes'; EXP='ReferenceManual/Expressions'
OPS = "struct __Input: Decodable { let ops: [String]; let args: [[Int]] }\n"
P=[]
P.append(dict(id='generic-swap-and-stack', title='Generic Stack<Element>', topic='Generics', diff='easy', concepts=['generics','mutating'], docs=[('Generics — Generic Types', GE)],
 sig='func stackDemo(_ ints: [Int], _ words: [String]) -> [String]',
 statement="""Write `struct Stack<Element>` with `push`, `pop() -> Element?`, `peek: Element?` and `isEmpty`. Push all `ints` onto an `Stack<Int>` and all `words` onto a `Stack<String>`, then pop everything from each and return the popped values as strings (ints first, then words).""",
 solution="""
 struct Stack<Element> {
     private var items: [Element] = []
     var isEmpty: Bool { items.isEmpty }
     var peek: Element? { items.last }
     mutating func push(_ item: Element) { items.append(item) }
     mutating func pop() -> Element? { items.popLast() }
 }

 func stackDemo(_ ints: [Int], _ words: [String]) -> [String] {
     var a = Stack<Int>()
     var b = Stack<String>()
     ints.forEach { a.push($0) }
     words.forEach { b.push($0) }
     var out: [String] = []
     while let x = a.pop() { out.append(String(x)) }
     while let w = b.pop() { out.append(w) }
     return out
 }
 """,
 explain="""One generic definition, many concrete types — `Stack<Int>` and `Stack<String>` are distinct, fully type-checked types. `while let x = a.pop()` drains until `nil`.""",
 tests=[({'ints':[1,2,3],'words':['a','b']},['3','2','1','b','a']), {'ints':[],'words':[]}, {'ints':[9],'words':[]}]))
P.append(dict(id='generic-constraints-max', title='Generic Constraints: Most Frequent', topic='Generics', diff='medium', concepts=['generic-constraints','equatable-hashable','generics'], docs=[('Generics — Type Constraints', GE)],
 sig='func modeDemo(ints: [Int], words: [String]) -> [String]',
 statement="""Write `func mostFrequent<T: Hashable & Comparable>(_ items: [T]) -> T?` returning the most frequent element — ties broken by the **smallest** value. Return `[mostFrequent(ints) as String, mostFrequent(words)]`, using `"none"` for `nil`.""",
 solution="""
 func mostFrequent<T: Hashable & Comparable>(_ items: [T]) -> T? {
     let counts = items.reduce(into: [T: Int]()) { $0[$1, default: 0] += 1 }
     return counts.max { a, b in (a.value, b.key) < (b.value, a.key) }?.key
 }

 func modeDemo(ints: [Int], words: [String]) -> [String] {
     [mostFrequent(ints).map(String.init) ?? "none", mostFrequent(words) ?? "none"]
 }
 """,
 explain="""`T: Hashable & Comparable` composes two constraints — `Hashable` for dictionary keys, `Comparable` for tie-breaking. The tuple comparison `(count, -key)` trick is expressed as `(a.value, b.key) < (b.value, a.key)` so a *smaller* key wins ties.""",
 tests=[({'ints':[3,1,3,1,2],'words':['b','a','b']},['1','b']), {'ints':[],'words':[]}, {'ints':[5],'words':['z','y','x']}]))
P.append(dict(id='where-clause-extension', title='Constrained Extensions with where', topic='Generics', diff='medium', concepts=['where-clause','generic-constraints','extensions'], docs=[('Generics — Extensions with a Generic Where Clause', GE)],
 sig='func statsDemo(_ ints: [Int], _ doubles: [Double]) -> [Double]',
 compare='float:1e-9',
 statement="""Add `average` to **any** `Collection` whose `Element: BinaryInteger` (returns `Double`), and a separate `average` for `Element: BinaryFloatingPoint` (returns `Element`). Empty collections average to 0. Return `[ints.average, Double(doubles.average), Array(ints.prefix(2)).average]`.""",
 solution="""
 extension Collection where Element: BinaryInteger {
     var average: Double {
         isEmpty ? 0 : Double(reduce(0, +)) / Double(count)
     }
 }

 extension Collection where Element: BinaryFloatingPoint {
     var average: Element {
         isEmpty ? 0 : reduce(0, +) / Element(count)
     }
 }

 func statsDemo(_ ints: [Int], _ doubles: [Double]) -> [Double] {
     [ints.average, Double(doubles.average), Array(ints.prefix(2)).average]
 }
 """,
 explain="""`extension Collection where Element: BinaryInteger` adds API only where it makes sense — `["a"].average` doesn't compile. Two constrained extensions can define the same name; overload resolution picks by element type.""",
 tests=[({'ints':[1,2,3,4],'doubles':[0.5,1.5]},[2.5,1.0,1.5]), {'ints':[],'doubles':[]}, {'ints':[7],'doubles':[2]}]))
P.append(dict(id='associated-type-container', title='Protocol with an Associated Type', topic='Generics', diff='medium', concepts=['associated-types','protocols','generics'], docs=[('Generics — Associated Types', GE)],
 sig='func containerDemo(_ ints: [Int], _ words: [String]) -> [String]',
 statement="""Define `protocol Container { associatedtype Item; mutating func append(_ item: Item); var count: Int { get }; subscript(i: Int) -> Item { get } }`. Conform `IntBag` (stores `[Int]`) and a generic `Queue<T>`. Then write a generic function `func allItemsMatch<C1: Container, C2: Container>(_ a: C1, _ b: C2) -> Bool where C1.Item == C2.Item, C1.Item: Equatable`.

 Return `["<bag.count>", "<queue.count>", "\\(allItemsMatch(bag, Queue(ints)))", "\\(allItemsMatch(Queue(words), Queue(words.reversed())))"]` (the reversed comparison uses `Queue` of the reversed words).""",
 solution="""
 protocol Container {
     associatedtype Item
     mutating func append(_ item: Item)
     var count: Int { get }
     subscript(i: Int) -> Item { get }
 }

 struct IntBag: Container {
     private var items: [Int] = []
     mutating func append(_ item: Int) { items.append(item) }
     var count: Int { items.count }
     subscript(i: Int) -> Int { items[i] }
 }

 struct Queue<T>: Container {
     private var items: [T] = []
     init(_ items: [T] = []) { self.items = items }
     mutating func append(_ item: T) { items.append(item) }
     var count: Int { items.count }
     subscript(i: Int) -> T { items[i] }
 }

 func allItemsMatch<C1: Container, C2: Container>(_ a: C1, _ b: C2) -> Bool
 where C1.Item == C2.Item, C1.Item: Equatable {
     guard a.count == b.count else { return false }
     return (0..<a.count).allSatisfy { a[$0] == b[$0] }
 }

 func containerDemo(_ ints: [Int], _ words: [String]) -> [String] {
     var bag = IntBag()
     ints.forEach { bag.append($0) }
     let queue = Queue(words)
     return ["\\(bag.count)", "\\(queue.count)", "\\(allItemsMatch(bag, Queue(ints)))", "\\(allItemsMatch(queue, Queue(Array(words.reversed()))))"]
 }
 """,
 explain="""`associatedtype Item` is a placeholder each conformer fills in — `IntBag` infers `Item == Int` from its methods. `where C1.Item == C2.Item` relates two generic parameters' associated types. This is exactly how `Sequence.Element` works.""",
 tests=[({'ints':[1,2],'words':['a','b','a']},['2','3','true','true']), {'ints':[],'words':[]}, {'ints':[5],'words':['x','y']}]))
P.append(dict(id='opaque-some-return', title='Opaque Types with some', topic='Opaque & existential types', diff='medium', concepts=['opaque-types','opaque-vs-generics','existential-any'], docs=[('Opaque and Boxed Protocol Types', OT)],
 sig='func drawAll(_ sizes: [Int]) -> [String]',
 statement="""`protocol Drawable { func draw() -> String }`. Write:
 - `func makeTriangle(_ n: Int) -> some Drawable` (lines of `*` growing from 1 to `n`, joined by `"/"`)
 - `func flipped(_ d: some Drawable) -> some Drawable` (reverses the `"/"`-separated lines)

 For each size return `flipped(makeTriangle(size)).draw()`. Then answer in `explanation`: why can't `makeTriangle` return a `Triangle` for small `n` and a `Square` otherwise?""",
 solution="""
 protocol Drawable { func draw() -> String }

 struct Triangle: Drawable {
     let size: Int
     func draw() -> String { (1...max(size, 1)).map { String(repeating: "*", count: $0) }.joined(separator: "/") }
 }

 struct Flipped<D: Drawable>: Drawable {
     let base: D
     func draw() -> String { base.draw().split(separator: "/").reversed().joined(separator: "/") }
 }

 func makeTriangle(_ n: Int) -> some Drawable { Triangle(size: n) }
 func flipped(_ d: some Drawable) -> some Drawable { Flipped(base: d) }

 func drawAll(_ sizes: [Int]) -> [String] {
     sizes.map { flipped(makeTriangle($0)).draw() }
 }
 """,
 explain="""`some Drawable` as a **return** type means "one specific type, chosen by me, hidden from you" — the compiler still knows it's `Flipped<Triangle>`, so there's no boxing. That's why all return paths must yield the **same** type (returning `Triangle` or `Square` would need `any Drawable`). `some` in **parameter** position is sugar for a generic parameter.""",
 tests=[({'sizes':[3,1]},['***/**/*','*']), {'sizes':[]}, {'sizes':[5]}]))
P.append(dict(id='type-erasure-any-shape', title='Type Erasure by Hand', topic='Opaque & existential types', diff='hard', concepts=['type-erasure','associated-types','closures'], docs=[('Opaque and Boxed Protocol Types', OT)],
 sig='func pipelineDemo(_ inputs: [String]) -> [String]',
 statement="""`protocol Transformer { associatedtype Input; associatedtype Output; func transform(_ x: Input) -> Output }`. Implement `Uppercaser` (String→String), `Length` (String→Int) and `Stars` (Int→String, `n` stars).

 Write a type-erased wrapper `struct AnyTransformer<In, Out>: Transformer` that stores a closure, with `init<T: Transformer>(_ base: T) where T.Input == In, T.Output == Out`, and a `func then<Next>(_ next: AnyTransformer<Out, Next>) -> AnyTransformer<In, Next>`.

 Build `AnyTransformer(Length()).then(AnyTransformer(Stars()))` and also an `[AnyTransformer<String, String>]` holding `Uppercaser` and that chain; apply each to each input, returning results in order (for each input, both transformers).""",
 solution="""
 protocol Transformer {
     associatedtype Input
     associatedtype Output
     func transform(_ x: Input) -> Output
 }

 struct Uppercaser: Transformer { func transform(_ x: String) -> String { x.uppercased() } }
 struct Length: Transformer { func transform(_ x: String) -> Int { x.count } }
 struct Stars: Transformer { func transform(_ x: Int) -> String { String(repeating: "*", count: x) } }

 struct AnyTransformer<In, Out>: Transformer {
     private let _transform: (In) -> Out

     init<T: Transformer>(_ base: T) where T.Input == In, T.Output == Out {
         _transform = base.transform
     }

     private init(closure: @escaping (In) -> Out) { _transform = closure }

     func transform(_ x: In) -> Out { _transform(x) }

     func then<Next>(_ next: AnyTransformer<Out, Next>) -> AnyTransformer<In, Next> {
         AnyTransformer<In, Next>(closure: { next.transform(self.transform($0)) })
     }
 }

 func pipelineDemo(_ inputs: [String]) -> [String] {
     let stars = AnyTransformer(Length()).then(AnyTransformer(Stars()))
     let all: [AnyTransformer<String, String>] = [AnyTransformer(Uppercaser()), stars]
     return inputs.flatMap { input in all.map { $0.transform(input) } }
 }
 """,
 explain="""A protocol with associated types can't be stored in a homogeneous array as-is: `Uppercaser` and the Length→Stars chain are different types. Type erasure hides the concrete type behind a generic struct that forwards to a stored closure — the pattern behind `AnySequence`, `AnyHashable` and Combine's `AnyPublisher`. (Swift 5.7+ also offers `any Transformer<String, String>` with primary associated types.)""",
 tests=[({'inputs':['hi','Swift']},['HI','**','SWIFT','*****']), {'inputs':[]}, {'inputs':['']}]))
P.append(dict(id='phantom-types-ids', title='Phantom Types for Safe IDs & Units', topic='Generics', diff='hard', concepts=['phantom-types','generics','operator-overloading'], docs=[('Generics', GE)],
 sig='func distances(_ meters: [Double], _ feet: [Double]) -> [Double]',
 compare='float:1e-9',
 statement="""Write `struct Length<Unit: LengthUnit>` storing a `Double`, where `protocol LengthUnit { static var metersPerUnit: Double { get } }` and `enum Meters`, `enum Feet` (0.3048) conform. `Unit` is never stored — it's a **phantom type**.

 Add `+` for two lengths of the **same** unit, and `func converted<To>(to: To.Type) -> Length<To>`. Sum all meters, sum all feet, convert the feet total to meters, and return `[meterTotal, feetTotal, meterTotal + feetInMeters]`. (Try `Length<Meters> + Length<Feet>` — it won't compile.)""",
 solution="""
 protocol LengthUnit { static var metersPerUnit: Double { get } }
 enum Meters: LengthUnit { static let metersPerUnit = 1.0 }
 enum Feet: LengthUnit { static let metersPerUnit = 0.3048 }

 struct Length<Unit: LengthUnit> {
     let value: Double

     static func + (a: Length, b: Length) -> Length { Length(value: a.value + b.value) }

     func converted<To: LengthUnit>(to: To.Type) -> Length<To> {
         Length<To>(value: value * Unit.metersPerUnit / To.metersPerUnit)
     }
 }

 func distances(_ meters: [Double], _ feet: [Double]) -> [Double] {
     let m = meters.map { Length<Meters>(value: $0) }.reduce(Length(value: 0), +)
     let f = feet.map { Length<Feet>(value: $0) }.reduce(Length(value: 0), +)
     return [m.value, f.value, (m + f.converted(to: Meters.self)).value]
 }
 """,
 explain="""Phantom type parameters tag values at compile time with **zero runtime cost**. `Length<Meters>` and `Length<Feet>` are different types, so mixing units (the Mars Climate Orbiter bug) is a type error rather than a crash in orbit. Same trick: `ID<User>` vs `ID<Order>`.""",
 tests=[({'meters':[1,2],'feet':[10]},[3.0,10.0,6.048]), {'meters':[],'feet':[]}, {'meters':[0.5],'feet':[3.28084]}]))
P.append(dict(id='conditional-conformance-pair', title='Conditional Conformance', topic='Generics', diff='medium', concepts=['conditional-conformance','equatable-hashable','generics'], docs=[('Generics — Conditional Conformance', PT)],
 sig='func pairDemo(_ a: [Int], _ b: [Int]) -> [String]',
 statement="""Write `struct Pair<A, B> { let first: A; let second: B }` and make it:
 - `Equatable` when `A: Equatable, B: Equatable`
 - `Hashable` when both are `Hashable`
 - `CustomStringConvertible` always: `"(<first>, <second>)"`

 Build pairs `Pair(a[i], b[i])` (zip), put them in a `Set` to deduplicate, and return the **sorted** descriptions of the unique pairs followed by `"<first pair == last pair>"` (or `"false"` if there are none).""",
 solution="""
 struct Pair<A, B> {
     let first: A
     let second: B
 }

 extension Pair: Equatable where A: Equatable, B: Equatable {}
 extension Pair: Hashable where A: Hashable, B: Hashable {}
 extension Pair: CustomStringConvertible {
     var description: String { "(\\(first), \\(second))" }
 }

 func pairDemo(_ a: [Int], _ b: [Int]) -> [String] {
     let pairs = zip(a, b).map { Pair(first: $0, second: $1) }
     let unique = Set(pairs).map(\\.description).sorted()
     let same = pairs.first.flatMap { f in pairs.last.map { f == $0 } } ?? false
     return unique + ["\\(same)"]
 }
 """,
 explain="""Empty extensions with `where` clauses are enough: the compiler synthesises `==` and `hash(into:)` when the constraints hold. `Pair<Int, () -> Void>` still exists — it just isn't Equatable. The standard library uses this for `Array`, `Optional` and `Dictionary`.""",
 tests=[({'a':[1,2,1],'b':[3,4,3]},['(1, 3)','(2, 4)','true']), {'a':[],'b':[]}, {'a':[1,2],'b':[5]}]))
P.append(dict(id='dynamic-member-lookup', title='@dynamicMemberLookup JSON Wrapper', topic='Advanced features', diff='medium', concepts=['dynamic-member-lookup','subscripts','optional-chaining'], docs=[('Attributes — dynamicMemberLookup', AT)],
 sig='func jsonPaths(_ json: [String: String], paths: [String]) -> [String]',
 statement="""Make a `@dynamicMemberLookup struct Config` wrapping `[String: String]` so that `config.host` returns `config.storage["host"]`. Also add a dotted-path helper for nested keys stored flat as `"db.port"`: `config.db.port` — hint: return another `Config` scoped to the prefix when the key isn't found directly.

 For each path like `"db.port"`, walk it with **dynamic member syntax** via a helper (`func value(at path: String) -> String?` that uses `self[dynamicMember:]`) and return the value or `"missing"`.""",
 solution="""
 @dynamicMemberLookup
 struct Config {
     let storage: [String: String]
     let prefix: String

     init(_ storage: [String: String], prefix: String = "") {
         self.storage = storage
         self.prefix = prefix
     }

     var value: String? { storage[prefix] }

     subscript(dynamicMember member: String) -> Config {
         Config(storage, prefix: prefix.isEmpty ? member : "\\(prefix).\\(member)")
     }

     func value(at path: String) -> String? {
         path.split(separator: ".").reduce(self) { $0[dynamicMember: String($1)] }.value
     }
 }

 func jsonPaths(_ json: [String: String], paths: [String]) -> [String] {
     let config = Config(json)
     precondition(config.db.port.value == json["db.port"])
     return paths.map { config.value(at: $0) ?? "missing" }
 }
 """,
 explain="""`@dynamicMemberLookup` routes `x.anything` to `subscript(dynamicMember:)`. With `String` members you get dynamic, stringly-typed access (great for JSON/Python interop); with `KeyPath` members you get type-safe forwarding. `config.db.port.value` compiles even though `Config` has no `db` property.""",
 tests=[({'json':{'host':'localhost','db.port':'5432'},'paths':['host','db.port','db.user']},['localhost','5432','missing']), {'json':{},'paths':[]}, {'json':{'a.b.c':'deep'},'paths':['a.b.c','a.b']}]))
P.append(dict(id='keypath-writable', title='WritableKeyPath Updates', topic='Advanced features', diff='medium', concepts=['key-paths','generics','inout'], docs=[('Expressions — Key-Path Expression', EXP)],
 sig='func applyUpdates(_ updates: [String]) -> [String]',
 statement="""`struct Profile { var name = "anon"; var age = 0; var city = "?" }`. Write a generic `func update<T, V>(_ value: inout T, _ keyPath: WritableKeyPath<T, V>, to newValue: V)`.

 Updates look like `"name=Ana"`, `"age=31"`, `"city=Porto"` (ignore unknown fields or bad ages). Apply them in order, then return `[name, "\\(age)", city]` read via a `[PartialKeyPath<Profile>]` array — `[\\.name, \\.age, \\.city]`.""",
 solution="""
 struct Profile {
     var name = "anon"
     var age = 0
     var city = "?"
 }

 func update<T, V>(_ value: inout T, _ keyPath: WritableKeyPath<T, V>, to newValue: V) {
     value[keyPath: keyPath] = newValue
 }

 func applyUpdates(_ updates: [String]) -> [String] {
     var profile = Profile()
     for u in updates {
         let parts = u.split(separator: "=", maxSplits: 1).map(String.init)
         guard parts.count == 2 else { continue }
         switch parts[0] {
         case "name": update(&profile, \\.name, to: parts[1])
         case "age": if let a = Int(parts[1]) { update(&profile, \\.age, to: a) }
         case "city": update(&profile, \\.city, to: parts[1])
         default: break
         }
     }
     let fields: [PartialKeyPath<Profile>] = [\\.name, \\.age, \\.city]
     return fields.map { "\\(profile[keyPath: $0])" }
 }
 """,
 explain="""`KeyPath` reads, `WritableKeyPath` reads and writes (on `var` properties), and `PartialKeyPath<Root>` erases the value type so different properties fit in one array (reads come back as `Any`). Key paths are values — you can store and pass them.""",
 tests=[({'updates':['name=Ana','age=31','city=Porto']},['Ana','31','Porto']), {'updates':[]}, {'updates':['age=x','zip=1','name=a=b']}]))
P.append(dict(id='custom-subscript-matrix', title='Custom Subscripts: Matrix', topic='Advanced features', diff='medium', concepts=['subscripts','precondition' if False else 'assert','operator-overloading'], docs=[('Subscripts', SU)],
 sig='func matrixDemo(rows: Int, cols: Int, sets: [[Int]]) -> [[Int]]',
 statement="""`struct Matrix` with `rows`, `cols`, flat `grid: [Int]` and a **two-parameter** subscript `subscript(row: Int, col: Int) -> Int { get set }` that uses `precondition` to check bounds. Add a `static func *` for matrix multiplication (precondition on dimensions).

 Apply each `[r, c, v]` in `sets` to an all-zero matrix `m`, then return `(m * transpose(m))` as nested arrays, where you also write `var transposed: Matrix`.""",
 solution="""
 struct Matrix {
     let rows: Int, cols: Int
     private(set) var grid: [Int]

     init(rows: Int, cols: Int) {
         self.rows = rows
         self.cols = cols
         grid = Array(repeating: 0, count: rows * cols)
     }

     subscript(row: Int, col: Int) -> Int {
         get {
             precondition(row >= 0 && row < rows && col >= 0 && col < cols, "index out of range")
             return grid[row * cols + col]
         }
         set {
             precondition(row >= 0 && row < rows && col >= 0 && col < cols, "index out of range")
             grid[row * cols + col] = newValue
         }
     }

     var transposed: Matrix {
         var t = Matrix(rows: cols, cols: rows)
         for r in 0..<rows { for c in 0..<cols { t[c, r] = self[r, c] } }
         return t
     }

     var nested: [[Int]] { (0..<rows).map { r in (0..<cols).map { self[r, $0] } } }

     static func * (a: Matrix, b: Matrix) -> Matrix {
         precondition(a.cols == b.rows, "dimension mismatch")
         var out = Matrix(rows: a.rows, cols: b.cols)
         for i in 0..<a.rows { for j in 0..<b.cols { for k in 0..<a.cols { out[i, j] += a[i, k] * b[k, j] } } }
         return out
     }
 }

 func matrixDemo(rows: Int, cols: Int, sets: [[Int]]) -> [[Int]] {
     var m = Matrix(rows: rows, cols: cols)
     for s in sets { m[s[0], s[1]] = s[2] }
     return (m * m.transposed).nested
 }
 """,
 explain="""Subscripts can take several parameters (`m[1, 2]`) and have getters and setters, so `out[i, j] += …` works. `precondition` stays on in release builds (unlike `assert`), giving a clear message instead of silent corruption.""",
 tests=[({'rows':2,'cols':2,'sets':[[0,0,1],[0,1,2],[1,0,3],[1,1,4]]},[[5,11],[11,25]]), {'rows':1,'cols':3,'sets':[[0,2,7]]}, {'rows':0,'cols':0,'sets':[]}]))
P.append(dict(id='custom-operator-vector', title='Operator Overloading: 2-D Vectors', topic='Advanced features', diff='easy', concepts=['operator-overloading','custom-operators','equatable-hashable'], docs=[('Advanced Operators — Operator Methods', AO)],
 sig='func vectorDemo(_ a: [Double], _ b: [Double]) -> [Double]',
 compare='float:1e-9',
 statement="""`struct Vector2: Equatable { var x, y: Double }` with `+`, binary `-`, **prefix** `-`, `*` by a scalar (both orders), `+=`, and a custom infix operator `•` for the dot product (declare `infix operator • : MultiplicationPrecedence`).

 Return `[(a+b).x, (a+b).y, (-a).x, (a*2).y, (3*b).x, a•b, (a == b) ? 1 : 0]` and also compute `var c = a; c += b` and append `c.x`.""",
 solution="""
 infix operator • : MultiplicationPrecedence

 struct Vector2: Equatable {
     var x: Double, y: Double

     static func + (l: Vector2, r: Vector2) -> Vector2 { Vector2(x: l.x + r.x, y: l.y + r.y) }
     static func - (l: Vector2, r: Vector2) -> Vector2 { l + -r }
     static prefix func - (v: Vector2) -> Vector2 { Vector2(x: -v.x, y: -v.y) }
     static func * (v: Vector2, k: Double) -> Vector2 { Vector2(x: v.x * k, y: v.y * k) }
     static func * (k: Double, v: Vector2) -> Vector2 { v * k }
     static func += (l: inout Vector2, r: Vector2) { l = l + r }
     static func • (l: Vector2, r: Vector2) -> Double { l.x * r.x + l.y * r.y }
 }

 func vectorDemo(_ a: [Double], _ b: [Double]) -> [Double] {
     let u = Vector2(x: a[0], y: a[1]), v = Vector2(x: b[0], y: b[1])
     var c = u
     c += v
     return [(u + v).x, (u + v).y, (-u).x, (u * 2).y, (3 * v).x, u • v, u == v ? 1 : 0, c.x]
 }
 """,
 explain="""Operators are `static func`s on the type. Compound assignment takes `inout` left side. Prefix/postfix need the modifier. New operators must be declared once with a precedence group — `MultiplicationPrecedence` makes `a + b • c` parse as `a + (b • c)`.""",
 tests=[({'a':[1,2],'b':[3,4]},[4,6,-1,4,9,11,0,4]), {'a':[0,0],'b':[0,0]}, {'a':[1.5,-2],'b':[1.5,-2]}]))
P.append(dict(id='pattern-match-operator', title='Custom ~= Patterns in switch', topic='Advanced features', diff='medium', concepts=['pattern-matching-operator','pattern-matching'], docs=[('Patterns — Expression Pattern','ReferenceManual/Patterns')],
 sig='func classifyAll(_ words: [String]) -> [String]',
 statement="""Make `switch` understand two custom patterns by overloading `~=`:
 - a `Regex`-free `struct Prefix { let text: String }` matching strings with that prefix
 - a closure pattern `(String) -> Bool`

 Classify each word: `Prefix(text: "un")` → `"negation"`, `{ $0.count > 8 }` → `"long"`, `Prefix(text: "re")` → `"repeat"`, else `"plain"` (checked in that order).""",
 solution="""
 struct Prefix { let text: String }

 func ~= (pattern: Prefix, value: String) -> Bool { value.hasPrefix(pattern.text) }
 func ~= (pattern: (String) -> Bool, value: String) -> Bool { pattern(value) }

 func classifyAll(_ words: [String]) -> [String] {
     let isLong: (String) -> Bool = { $0.count > 8 }
     return words.map { word in
         switch word {
         case Prefix(text: "un"): "negation"
         case isLong: "long"
         case Prefix(text: "re"): "repeat"
         default: "plain"
         }
     }
 }
 """,
 explain="""An **expression pattern** in a `case` is checked with `pattern ~= value`. The standard library defines it for `Equatable` values and ranges; your overloads extend `switch` to any matching logic.""",
 tests=[({'words':['undo','refactoring','redo','swift']},['negation','long','repeat','plain']), {'words':[]}, {'words':['unbelievable','re','']}]))
P.append(dict(id='custom-sequence-fibonacci', title='Custom Sequence: Fibonacci', topic='Collections deep dive', diff='medium', concepts=['custom-collection','lazy-sequences'], docs=[('Protocols — Collections', PT)],
 sig='func fibDemo(limit: Int, take: Int) -> [[Int]]',
 statement="""Write `struct Fibonacci: Sequence` (infinite) with a nested `Iterator: IteratorProtocol`, starting 0, 1, 1, 2…

 Return `[Array(Fibonacci().prefix(take)), Fibonacci().lazy.filter { $0.isMultiple(of: 2) }.prefix(while: { $0 <= limit }) as array]`. Laziness is essential — the sequence never ends.""",
 solution="""
 struct Fibonacci: Sequence {
     struct Iterator: IteratorProtocol {
         var a = 0, b = 1
         mutating func next() -> Int? {
             defer { (a, b) = (b, a &+ b) }
             return a
         }
     }
     func makeIterator() -> Iterator { Iterator() }
 }

 func fibDemo(limit: Int, take: Int) -> [[Int]] {
     [Array(Fibonacci().prefix(take)),
      Array(Fibonacci().lazy.filter { $0.isMultiple(of: 2) }.prefix(while: { $0 <= limit }))]
 }
 """,
 explain="""`Sequence` only needs `makeIterator()`; the iterator's `next()` returns `nil` to finish (never, here). You then get `prefix`, `map`, `filter`, `contains`… for free. On an infinite sequence, eager `filter` would never return — `.lazy` evaluates on demand. `defer` returns the old `a` before advancing.""",
 tests=[({'limit':100,'take':8},[[0,1,1,2,3,5,8,13],[0,2,8,34]]), {'limit':0,'take':0}, {'limit':4000000,'take':1}]))
P.append(dict(id='custom-collection-ring', title='Custom Collection: Ring Buffer', topic='Collections deep dive', diff='hard', concepts=['custom-collection','subscripts','mutating'], docs=[('Generics', GE)],
 statement="""Implement `struct RingBuffer<Element>: Collection` with fixed `capacity`: `mutating func append(_:)` overwrites the **oldest** element when full. Conform to `Collection` (`startIndex`, `endIndex`, `index(after:)`, `subscript(position:)`) so it iterates oldest → newest — then `map`, `first`, `count`, `reduce` and slicing come for free.

 The judge sends `{"capacity": n, "values": [...]}` and prints `[Array(buffer), [buffer.first ?? -1], [buffer.count], [buffer.reduce(0, +)], Array(buffer.dropFirst())]`.""",
 starter="""
 struct RingBuffer<Element>: Collection {
     init(capacity: Int) {}
     mutating func append(_ element: Element) {}

     var startIndex: Int { 0 }
     var endIndex: Int { 0 }
     func index(after i: Int) -> Int { i + 1 }
     subscript(position: Int) -> Element { fatalError() }
 }
 """,
 solution="""
 struct RingBuffer<Element>: Collection {
     private var storage: [Element] = []
     private var head = 0
     let capacity: Int

     init(capacity: Int) { self.capacity = capacity }

     mutating func append(_ element: Element) {
         guard capacity > 0 else { return }
         if storage.count < capacity {
             storage.append(element)
         } else {
             storage[head] = element
             head = (head + 1) % capacity
         }
     }

     var startIndex: Int { 0 }
     var endIndex: Int { storage.count }
     func index(after i: Int) -> Int { i + 1 }
     subscript(position: Int) -> Element { storage[(head + position) % storage.count] }
 }
 """,
 harness="""
 struct __Input: Decodable { let capacity: Int; let values: [Int] }
 func __run(_ __i: __Input) async throws -> [[Int]] {
     var buffer = RingBuffer<Int>(capacity: __i.capacity)
     __i.values.forEach { buffer.append($0) }
     return [Array(buffer), [buffer.first ?? -1], [buffer.count], [buffer.reduce(0, +)], Array(buffer.dropFirst())]
 }
 """,
 explain="""`Collection` requires four members; everything else is a default implementation in protocol extensions. Logical positions `0..<count` map to physical slots `(head + i) % count`, hiding the wraparound. `dropFirst()` returns a `Slice<RingBuffer>` sharing the same indices.""",
 tests=[({'capacity':3,'values':[1,2,3,4,5]},[[3,4,5],[3],[3],[12],[4,5]]), {'capacity':3,'values':[]}, {'capacity':0,'values':[1]}, {'capacity':5,'values':[9,8]}]))
P.append(dict(id='copy-on-write', title='Implement Copy-on-Write', topic='Collections deep dive', diff='hard', concepts=['copy-on-write','value-semantics','memory-layout'], docs=[('Structures and Classes', 'LanguageGuide/ClassesAndStructures')],
 statement="""Build `struct COWArray` that stores its elements in a private `final class Storage { var items: [Int] }` and only **copies the storage when mutated while shared**, using `isKnownUniquelyReferenced(&storage)`. Count copies in a `static`-free way: each `Storage` records `copies` in a shared counter object you pass in.

 Required API: `init(counter:)`, `mutating func append(_:)`, `var items: [Int]`.

 The judge runs: `var a = COWArray(...)`, appends `values`; `var b = a` (no copy yet); appends `extra` to `b`; appends 1 more to `b` (still no extra copy); returns `[a.items, b.items, [counter.copies]]`.""",
 starter="""
 final class CopyCounter { var copies = 0 }

 struct COWArray {
     init(counter: CopyCounter) {}
     mutating func append(_ x: Int) {}
     var items: [Int] { [] }
 }
 """,
 solution="""
 final class CopyCounter { var copies = 0 }

 struct COWArray {
     private final class Storage {
         var items: [Int]
         init(_ items: [Int]) { self.items = items }
     }

     private var storage = Storage([])
     private let counter: CopyCounter

     init(counter: CopyCounter) { self.counter = counter }

     var items: [Int] { storage.items }

     mutating func append(_ x: Int) {
         if !isKnownUniquelyReferenced(&storage) {
             storage = Storage(storage.items)
             counter.copies += 1
         }
         storage.items.append(x)
     }
 }
 """,
 harness="""
 struct __Input: Decodable { let values: [Int]; let extra: Int }
 func __run(_ __i: __Input) async throws -> [[Int]] {
     let counter = CopyCounter()
     var a = COWArray(counter: counter)
     __i.values.forEach { a.append($0) }
     var b = a
     b.append(__i.extra)
     b.append(__i.extra + 1)
     return [a.items, b.items, [counter.copies]]
 }
 """,
 explain="""Assigning a struct copies only the **reference** to its class storage. Before mutating, `isKnownUniquelyReferenced` asks ARC whether anyone else shares it; if so, clone first. That's exactly how `Array`, `String` and `Dictionary` achieve cheap copies with value semantics. Expected copies: exactly 1.""",
 tests=[({'values':[1,2],'extra':9},[[1,2],[1,2,9,10],[1]]), {'values':[],'extra':0}, {'values':[5,5,5],'extra':-1}]))
P.append(dict(id='indirect-enum-expression', title='indirect enum: Expression Trees', topic='Enums deep dive', diff='medium', concepts=['indirect-enums','associated-values','pattern-matching'], docs=[('Enumerations — Recursive Enumerations', EN)],
 sig='func evaluateRPN(_ tokens: [String]) -> Int?',
 statement="""Model `indirect enum Expr { case number(Int); case add(Expr, Expr); case multiply(Expr, Expr); case negate(Expr) }` with an `evaluate() -> Int` method.

 Parse **Reverse Polish Notation** tokens (`"3"`, `"+"`, `"*"`, `"neg"`) into an `Expr` using a stack, then evaluate it. Return `nil` if the tokens don't form exactly one expression.

 ```swift
 evaluateRPN(["2", "3", "+", "4", "*"])   // 20
 evaluateRPN(["5", "neg", "1", "+"])      // -4
 ```""",
 solution="""
 indirect enum Expr {
     case number(Int)
     case add(Expr, Expr)
     case multiply(Expr, Expr)
     case negate(Expr)

     func evaluate() -> Int {
         switch self {
         case .number(let n): n
         case let .add(a, b): a.evaluate() + b.evaluate()
         case let .multiply(a, b): a.evaluate() * b.evaluate()
         case .negate(let e): -e.evaluate()
         }
     }
 }

 func evaluateRPN(_ tokens: [String]) -> Int? {
     var stack: [Expr] = []
     for token in tokens {
         switch token {
         case "+", "*":
             guard let b = stack.popLast(), let a = stack.popLast() else { return nil }
             stack.append(token == "+" ? .add(a, b) : .multiply(a, b))
         case "neg":
             guard let e = stack.popLast() else { return nil }
             stack.append(.negate(e))
         default:
             guard let n = Int(token) else { return nil }
             stack.append(.number(n))
         }
     }
     return stack.count == 1 ? stack[0].evaluate() : nil
 }
 """,
 explain="""A recursive enum needs `indirect` so the payload is boxed on the heap (otherwise the type would have infinite size). Compared to a class hierarchy you keep **value semantics** and an exhaustive `switch` — adding a case forces you to update `evaluate`.""",
 tests=[({'tokens':['2','3','+','4','*']},20), ({'tokens':['5','neg','1','+']},-4), {'tokens':[]}, {'tokens':['1','+']}, {'tokens':['1','2']}, {'tokens':['7']}, {'tokens':['2','x','*']}]))
P.append(dict(id='indirect-linked-list', title='indirect enum: Immutable Linked List', topic='Enums deep dive', diff='medium', concepts=['indirect-enums','custom-collection','value-semantics'], docs=[('Enumerations — Recursive Enumerations', EN)],
 sig='func listDemo(_ values: [Int]) -> [[Int]]',
 statement="""`indirect enum List<T> { case empty; case node(T, List<T>) }`. Add `func prepending(_:)`, `var reversed: List`, and conform to `Sequence` (via `AnyIterator` or a custom iterator).

 Build the list by prepending each value in order, then return `[Array(list), Array(list.reversed), [list.reduce(0, +)]]`.""",
 solution="""
 indirect enum List<T>: Sequence {
     case empty
     case node(T, List<T>)

     func prepending(_ value: T) -> List<T> { .node(value, self) }

     var reversed: List<T> {
         reduce(List.empty) { $0.prepending($1) }
     }

     func makeIterator() -> AnyIterator<T> {
         var current = self
         return AnyIterator {
             guard case let .node(value, next) = current else { return nil }
             current = next
             return value
         }
     }
 }

 func listDemo(_ values: [Int]) -> [[Int]] {
     let list = values.reduce(List<Int>.empty) { $0.prepending($1) }
     return [Array(list), Array(list.reversed), [list.reduce(0, +)]]
 }
 """,
 explain="""`indirect` on the whole enum boxes every recursive case. `AnyIterator { … }` builds an iterator from a closure that captures mutable state. Prepending is O(1) and old versions are untouched — **persistent** data structures share their tails.""",
 tests=[({'values':[1,2,3]},[[3,2,1],[1,2,3],[6]]), {'values':[]}, {'values':[42]}]))
P.append(dict(id='equatable-hashable-custom', title='Custom Equatable & Hashable', topic='Protocols', diff='medium', concepts=['equatable-hashable','set-vs-array'], docs=[('Protocols — Adopting a Protocol Using a Synthesized Implementation', PT)],
 sig='func uniqueEmails(_ raw: [String]) -> Int',
 statement="""Email identity rules: case-insensitive; in the local part (before `@`) dots are ignored and anything after a `+` is ignored. So `"J.Doe+news@Mail.com"` equals `"jdoe@mail.com"`.

 Write `struct Email: Hashable` storing the **original** string, but implement `==` and `hash(into:)` on the **normalised** form yourself. Return how many distinct emails there are (a `Set<Email>`).""",
 solution="""
 struct Email: Hashable {
     let raw: String

     private var normalized: String {
         let lower = raw.lowercased()
         guard let at = lower.firstIndex(of: "@") else { return lower }
         var local = lower[..<at]
         if let plus = local.firstIndex(of: "+") { local = local[..<plus] }
         return local.replacingOccurrences(of: ".", with: "") + lower[at...]
     }

     static func == (a: Email, b: Email) -> Bool { a.normalized == b.normalized }
     func hash(into hasher: inout Hasher) { hasher.combine(normalized) }
 }

 func uniqueEmails(_ raw: [String]) -> Int {
     Set(raw.map(Email.init)).count
 }
 """,
 explain="""If you customise `==`, you **must** hash exactly the same fields — equal values must produce equal hashes, or `Set` and `Dictionary` silently break. `hash(into:)` feeds components into a `Hasher`, which is randomly seeded per process (never persist hash values).""",
 tests=[({'raw':['J.Doe+news@Mail.com','jdoe@mail.com','jane@mail.com']},2), {'raw':[]}, {'raw':['a@b.c','a.@b.c','A+x@B.C','a@bc']}]))
P.append(dict(id='predict-self-vs-Self', title='Predict: self, Self and type(of:)', topic='Protocols', mode='predict', diff='medium', concepts=['self-vs-Self','type-casting'], docs=[('Types — Self Type','ReferenceManual/Types')],
 statement="Predict the output. `Self` refers to the **dynamic** type in a class.",
 snippet="""
 class Animal {
     required init() {}
     class var kind: String { "animal" }
     func clone() -> Self { Self() }
     func describe() -> String { "\\(type(of: self)) is a \\(Self.kind)" }
 }
 final class Dog: Animal {
     override class var kind: String { "dog" }
 }

 let pet: Animal = Dog()
 print(pet.describe())
 print(type(of: pet.clone()))
 print(pet is Dog, type(of: pet) == Animal.self)
 print(Animal().describe())
 """,
 explain="""`type(of: self)` and `Self` both resolve to the **runtime** type, so a `Dog` stored in an `Animal` variable describes and clones itself as a `Dog`. `Self()` requires a `required init` so every subclass can be constructed that way."""))

write_all(P, 'advanced', 100)
