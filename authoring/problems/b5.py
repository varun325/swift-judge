import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CS='LanguageGuide/ClassesAndStructures'; PR='LanguageGuide/Properties'; ME='LanguageGuide/Methods'; IN='LanguageGuide/Initialization'; IH='LanguageGuide/Inheritance'
DE='LanguageGuide/Deinitialization'; PT='LanguageGuide/Protocols'; EX='LanguageGuide/Extensions'; AC='LanguageGuide/AccessControl'; TC='LanguageGuide/TypeCasting'; ARC='LanguageGuide/AutomaticReferenceCounting'
P=[]
OPS_HARNESS_HEADER = "struct __Input: Decodable { let ops: [String]; let args: [[Int]] }\n"
# ---------- Structs (§21)
P.append(dict(id='fix-vacation-setter', title='Fix the Bug: Computed Property Setter', topic='Structs', notes='21', concepts=['computed-properties','struct-vs-class'], docs=[('Properties — Computed Properties', PR)],
 sig='func vacationRoundTrip(taken: Int, remaining: Int) -> [Int]',
 statement="""From your notes: the setter has its arithmetic backwards, so `e.vacationRemaining = 5; e.vacationRemaining` doesn't read back 5. Fix the struct. `vacationRoundTrip` sets `vacationTaken`, then `vacationRemaining`, and returns `[vacationAllowed, vacationRemaining]`.""",
 starter="""
 struct Employee {
     let name: String
     var vacationAllowed = 14
     var vacationTaken = 0

     var vacationRemaining: Int {
         get { vacationAllowed - vacationTaken }
         set { vacationAllowed = vacationTaken - newValue }
     }
 }

 func vacationRoundTrip(taken: Int, remaining: Int) -> [Int] {
     var e = Employee(name: "varun")
     e.vacationTaken = taken
     e.vacationRemaining = remaining
     return [e.vacationAllowed, e.vacationRemaining]
 }
 """,
 solution="""
 struct Employee {
     let name: String
     var vacationAllowed = 14
     var vacationTaken = 0

     var vacationRemaining: Int {
         get { vacationAllowed - vacationTaken }
         set { vacationAllowed = vacationTaken + newValue }
     }
 }

 func vacationRoundTrip(taken: Int, remaining: Int) -> [Int] {
     var e = Employee(name: "varun")
     e.vacationTaken = taken
     e.vacationRemaining = remaining
     return [e.vacationAllowed, e.vacationRemaining]
 }
 """,
 explain="""Any get/set pair should satisfy the round trip `x.p = v; x.p == v`. The setter receives `newValue`; solving `allowed - taken = newValue` gives `allowed = taken + newValue`.""",
 tests=[({'taken':0,'remaining':5},[5,5]), {'taken':3,'remaining':5}, {'taken':10,'remaining':0}, {'taken':2,'remaining':20}]))
P.append(dict(id='property-observers-clamp', title='Property Observers: Clamp & Log', topic='Structs', notes='21', concepts=['property-observers'], docs=[('Properties — Property Observers', PR)],
 sig='func volumeLog(_ changes: [Int]) -> [String]',
 statement="""`struct Speaker` has `var volume = 50` with:
 - `willSet`: append `"will <old>-><new>"` to `log`
 - `didSet`: clamp the stored value into `0...100`, then append `"did <final>"`

 (`log` is a `var log: [String] = []` property of the struct.) Apply every change and return the log.""",
 solution="""
 struct Speaker {
     var log: [String] = []
     var volume = 50 {
         willSet { log.append("will \\(volume)->\\(newValue)") }
         didSet {
             volume = min(max(volume, 0), 100)
             log.append("did \\(volume)")
         }
     }
 }

 func volumeLog(_ changes: [Int]) -> [String] {
     var speaker = Speaker()
     for change in changes { speaker.volume = change }
     return speaker.log
 }
 """,
 explain="""`willSet` sees `newValue` before the store; `didSet` sees `oldValue` after it. Assigning to the property **inside its own `didSet`** doesn't re-trigger observers — which is exactly what makes clamping there safe.""",
 tests=[({'changes':[70,150,-3]},['will 50->70','did 70','will 70->150','did 100','will 100->-3','did 0']), {'changes':[]}, {'changes':[50]}]))
P.append(dict(id='mutating-bank-account', title='mutating Methods & private(set)', topic='Structs', notes='21', concepts=['mutating','private-set','encapsulation'], docs=[('Methods — Modifying Value Types from Within Instance Methods', ME),('Access Control — Getters and Setters', AC)],
 sig='func bankOps(_ ops: [String]) -> [String]',
 statement="""`struct BankAccount` has `private(set) var funds = 0`, `mutating func deposit(_:)` and `mutating func withdraw(_:) -> Bool` (refuses if `amount > funds` — note your notes' version refused when `funds == amount`).

 Each op is `"d <n>"` or `"w <n>"`. Log `"ok <funds>"` or `"refused <funds>"` after each.""",
 solution="""
 struct BankAccount {
     private(set) var funds = 0

     mutating func deposit(_ amount: Int) {
         funds += amount
     }

     mutating func withdraw(_ amount: Int) -> Bool {
         guard amount <= funds else { return false }
         funds -= amount
         return true
     }
 }

 func bankOps(_ ops: [String]) -> [String] {
     var account = BankAccount()
     return ops.map { op in
         let parts = op.split(separator: " ")
         let amount = Int(parts[1])!
         let ok = parts[0] == "d" ? { account.deposit(amount); return true }() : account.withdraw(amount)
         return "\\(ok ? "ok" : "refused") \\(account.funds)"
     }
 }
 """,
 explain="""Struct methods that change stored properties must be `mutating`, and can only be called on a `var`. `private(set)` lets anyone **read** `funds` but only the type **write** it — so every change goes through `deposit`/`withdraw`.""",
 tests=[({'ops':['d 100','w 100','w 1']},['ok 100','ok 0','refused 0']), {'ops':[]}, {'ops':['w 5','d 5','w 3','w 3']}]))
P.append(dict(id='custom-init-keeps-memberwise', title='Custom init in an Extension', topic='Structs', notes='21', concepts=['initializers','extensions'], docs=[('Initialization — Memberwise Initializers for Structure Types', IN)],
 sig='func players(_ names: [String]) -> [String]',
 statement="""`struct Player { let name: String; let number: Int }`. Add `init(name: String)` that assigns `number` = the sum of the Unicode scalar values of the name's characters, modulo 100 — **in an extension**, so the free memberwise `init(name:number:)` still exists.

 `players` makes the first player with `Player(name:number: 10)` and the rest with `Player(name:)`, returning `"<name>#<number>"`.""",
 solution="""
 struct Player {
     let name: String
     let number: Int
 }

 extension Player {
     init(name: String) {
         self.name = name
         self.number = name.unicodeScalars.reduce(0) { $0 + Int($1.value) } % 100
     }
 }

 func players(_ names: [String]) -> [String] {
     names.enumerated().map { i, name in
         let p = i == 0 ? Player(name: name, number: 10) : Player(name: name)
         return "\\(p.name)#\\(p.number)"
     }
 }
 """,
 explain="""Writing an `init` inside the struct body **removes** the synthesised memberwise initialiser. Putting custom inits in an **extension** keeps both — a well-known Swift idiom.""",
 tests=[{'names':['Ana','Bo']}, {'names':[]}, {'names':['X','Zoë','Ω']}]))
P.append(dict(id='static-counter', title='static Properties', topic='Structs', notes='21', concepts=['static-properties','struct-vs-class'], docs=[('Properties — Type Properties', PR)],
 sig='func schoolRoll(_ names: [String]) -> [String]',
 statement="""`struct School` should have a **type-level** `static let capacity = 3` and a `static func enroll(_ roster: inout [String], _ name: String) -> String` that returns `"enrolled <name> (<n>/3)"` or `"full"` once capacity is reached.

 (Swift 6 forbids a global or `static var` of mutable shared state without isolation — so the roster is passed `inout` rather than stored in a `static var`.)""",
 solution="""
 struct School {
     static let capacity = 3

     static func enroll(_ roster: inout [String], _ name: String) -> String {
         guard roster.count < capacity else { return "full" }
         roster.append(name)
         return "enrolled \\(name) (\\(roster.count)/\\(capacity))"
     }
 }

 func schoolRoll(_ names: [String]) -> [String] {
     var roster: [String] = []
     return names.map { School.enroll(&roster, $0) }
 }
 """,
 explain="""`static` members belong to the type, accessed as `School.capacity`. `static let` is lazily initialised once, thread-safely. Under Swift 6 strict concurrency, `static var counter = 0` is an **error** (*not concurrency-safe*) unless isolated to an actor (e.g. `@MainActor`) — a common surprise from older tutorials.""",
 tests=[({'names':['a','b','c','d']},['enrolled a (1/3)','enrolled b (2/3)','enrolled c (3/3)','full']), {'names':[]}, {'names':['solo']}]))
P.append(dict(id='diag-mutating-let', title='Diagnostic: mutating Method on a let', topic='Structs', mode='diagnostic', notes='21', concepts=['mutating','let-vs-var'], docs=[('Methods — Modifying Value Types', ME)],
 statement="""Declare `struct Counter { var count = 0; mutating func increment() { count += 1 } }`, create it with **`let`**, and call `increment()`. You pass when the compiler rejects the call.""",
 starter="struct Counter {\n    var count = 0\n    mutating func increment() { count += 1 }\n}\n\nvar c = Counter()\nc.increment()\nprint(c.count)\n",
 solution="struct Counter {\n    var count = 0\n    mutating func increment() { count += 1 }\n}\n\nlet c = Counter()\nc.increment()\nprint(c.count)\n",
 explain="""*cannot use mutating member on immutable value: 'c' is a 'let' constant*. For a struct, `let` freezes the **whole value**, including every `var` property — the opposite of a class, where `let` only freezes the reference.""",
 tests=[{'name':'Mutating call on let rejected','pattern':'cannot use mutating member on immutable value'}]))
P.append(dict(id='diag-struct-needs-mutating', title='Diagnostic: Forgetting mutating', topic='Structs', mode='diagnostic', notes='21', concepts=['mutating'], docs=[('Methods — Modifying Value Types', ME)],
 statement="""Write a struct with a `var score = 0` and a method `func addPoint()` (without `mutating`) that does `score += 1`. You pass when the compiler explains that `self` is immutable.""",
 starter="struct Game {\n    var score = 0\n    mutating func addPoint() { score += 1 }\n}\n",
 solution="struct Game {\n    var score = 0\n    func addPoint() { score += 1 }\n}\n",
 explain="""*left side of mutating operator isn't mutable: 'self' is immutable*. In a non-mutating method, `self` is a `let`. The fix-it suggests adding `mutating`.""",
 tests=[{'name':'self is immutable','pattern':"'self' is immutable"}]))
# ---------- Classes & inheritance (§22)
P.append(dict(id='dynamic-dispatch-employees', title='Overriding & Dynamic Dispatch', topic='Classes & inheritance', notes='22', concepts=['inheritance','overloading-overriding','method-dispatch'], docs=[('Inheritance — Overriding', IH)],
 sig='func summaries(_ roles: [String], hours: Int) -> [String]',
 statement="""From your notes: `class Employee` with `init(hours:)` and `func summary() -> String` returning `"I work <h> hours a day."`; `class Developer: Employee` overrides it with `"I spend <h> hours a day fighting over tabs vs spaces"`; `class Manager: Employee` overrides it as `"I schedule meetings for <h> hours, then " + super.summary()`.

 Build an `[Employee]` from `roles` (`"dev"`, `"mgr"`, anything else = plain employee) and return each `summary()` — the method chosen at **runtime**.""",
 solution="""
 class Employee {
     let hours: Int
     init(hours: Int) { self.hours = hours }
     func summary() -> String { "I work \\(hours) hours a day." }
 }

 final class Developer: Employee {
     override func summary() -> String { "I spend \\(hours) hours a day fighting over tabs vs spaces" }
 }

 final class Manager: Employee {
     override func summary() -> String { "I schedule meetings for \\(hours) hours, then " + super.summary() }
 }

 func summaries(_ roles: [String], hours: Int) -> [String] {
     let staff: [Employee] = roles.map {
         switch $0 {
         case "dev": Developer(hours: hours)
         case "mgr": Manager(hours: hours)
         default: Employee(hours: hours)
         }
     }
     return staff.map { $0.summary() }
 }
 """,
 explain="""The variable's static type is `Employee`, but the **object's** dynamic type picks the implementation — dynamic dispatch through the class vtable. `super.summary()` calls the parent's version. Marking leaf classes `final` lets the compiler dispatch statically.""",
 tests=[({'roles':['dev','mgr','x'],'hours':8},['I spend 8 hours a day fighting over tabs vs spaces','I schedule meetings for 8 hours, then I work 8 hours a day.','I work 8 hours a day.']), {'roles':[],'hours':1}, {'roles':['mgr'],'hours':3}]))
P.append(dict(id='diag-missing-override', title="Diagnostic: Missing override", topic='Classes & inheritance', mode='diagnostic', notes='22', concepts=['inheritance','overloading-overriding'], docs=[('Inheritance — Overriding', IH)],
 statement="""Write a base class with `func speak()`, and a subclass that redeclares `func speak()` **without** `override`. You pass when Swift refuses the accidental shadowing.""",
 starter="class Animal {\n    func speak() { print(\"...\") }\n}\n\nclass Dog: Animal {\n    override func speak() { print(\"Woof\") }\n}\n",
 solution="class Animal {\n    func speak() { print(\"...\") }\n}\n\nclass Dog: Animal {\n    func speak() { print(\"Woof\") }\n}\n",
 explain="""*overriding declaration requires an 'override' keyword*. The reverse mistake — `override` where the parent has no such method — gives *method does not override any method from its superclass*. Both protect you from typos and silent API drift.""",
 tests=[{'name':'override required','pattern':"requires an 'override' keyword"}]))
P.append(dict(id='diag-super-init-order', title='Diagnostic: Two-Phase Initialisation', topic='Classes & inheritance', mode='diagnostic', notes='22', concepts=['two-phase-init','initializers'], docs=[('Initialization — Two-Phase Initialization', IN)],
 statement="""From your notes: `class Vehicle { let isElectric: Bool; init(isElectric:) }` and `class Car: Vehicle` with its own `let isConvertible: Bool`. In `Car`'s init, call `super.init(isElectric:)` **before** assigning `self.isConvertible`. You pass when the compiler rejects it.""",
 starter="""
 class Vehicle {
     let isElectric: Bool
     init(isElectric: Bool) { self.isElectric = isElectric }
 }

 class Car: Vehicle {
     let isConvertible: Bool
     init(isElectric: Bool, isConvertible: Bool) {
         self.isConvertible = isConvertible
         super.init(isElectric: isElectric)
     }
 }
 """,
 solution="""
 class Vehicle {
     let isElectric: Bool
     init(isElectric: Bool) { self.isElectric = isElectric }
 }

 class Car: Vehicle {
     let isConvertible: Bool
     init(isElectric: Bool, isConvertible: Bool) {
         super.init(isElectric: isElectric)
         self.isConvertible = isConvertible
     }
 }
 """,
 explain="""Phase 1 initialises every stored property from the subclass **up**; only after `super.init` returns (phase 2) may you use `self`. Swapping the order is rejected — your notes recorded the exact wording from Swift 6.4.""",
 tests=[{'name':'Order enforced','pattern':'not initialized at super.init call|may only be initialized once'}]))
P.append(dict(id='diag-no-initializers', title='Diagnostic: Class Has No Initializers', topic='Classes & inheritance', mode='diagnostic', notes='22', concepts=['initializers','class-definition'], docs=[('Initialization — Automatic Initializer Inheritance', IN)],
 statement="""From your notes' demonstration table: subclass `Vehicle` as `class Truck: Vehicle { var axles: Int }` — a new stored property with **no default and no init**. You pass when the compiler reports the class has no initialisers.""",
 starter="class Vehicle {\n    let wheels: Int\n    init(wheels: Int) { self.wheels = wheels }\n}\n\nclass Truck: Vehicle {\n    var axles: Int = 2\n}\n",
 solution="class Vehicle {\n    let wheels: Int\n    init(wheels: Int) { self.wheels = wheels }\n}\n\nclass Truck: Vehicle {\n    var axles: Int\n}\n",
 explain="""A subclass inherits its parent's designated initialisers **only** if it adds no stored properties without defaults. `axles` has no value, so nothing can initialise it: *class 'Truck' has no initializers*. Fix with a default or an `init(wheels:axles:)`.""",
 tests=[{'name':'No initializers','pattern':"class 'Truck' has no initializers"}]))
P.append(dict(id='convenience-init', title='Designated vs Convenience Initialisers', topic='Classes & inheritance', notes='22', diff='medium', concepts=['convenience-init','initializer-delegation','failable-init'], docs=[('Initialization — Initializer Delegation for Class Types', IN)],
 sig='func makeColors(_ specs: [String]) -> [String]',
 statement="""`final class Color` stores `red`, `green`, `blue` (`Int`, 0…255) via a designated `init(red:green:blue:)`. Add:
 - `convenience init(white: Int)` → all three equal
 - `convenience init?(hex: String)` → parses `"#RRGGBB"` (fails otherwise)

 Specs look like `"white 128"` or `"#1A2B3C"`. Return `"rgb(r,g,b)"` or `"invalid"`.""",
 solution="""
 final class Color {
     let red: Int, green: Int, blue: Int

     init(red: Int, green: Int, blue: Int) {
         self.red = red
         self.green = green
         self.blue = blue
     }

     convenience init(white: Int) {
         self.init(red: white, green: white, blue: white)
     }

     convenience init?(hex: String) {
         guard hex.count == 7, hex.first == "#", let value = Int(hex.dropFirst(), radix: 16) else { return nil }
         self.init(red: (value >> 16) & 0xFF, green: (value >> 8) & 0xFF, blue: value & 0xFF)
     }
 }

 func makeColors(_ specs: [String]) -> [String] {
     specs.map { spec in
         let color: Color? = if spec.hasPrefix("white "), let w = Int(spec.dropFirst(6)) {
             Color(white: w)
         } else {
             Color(hex: spec)
         }
         guard let c = color else { return "invalid" }
         return "rgb(\\(c.red),\\(c.green),\\(c.blue))"
     }
 }
 """,
 explain="""Designated inits fully initialise the class (delegating **up** to `super.init` in subclasses); convenience inits must delegate **across** with `self.init(...)`. A failable `init?` returns `nil` on bad input. Bit shifts and masks extract the channels.""",
 tests=[({'specs':['white 128','#1A2B3C','#12']},['rgb(128,128,128)','rgb(26,43,60)','invalid']), {'specs':[]}, {'specs':['#FFFFFF','#GGGGGG','white x']}]))
P.append(dict(id='deinit-lifecycle', title='deinit and Object Lifetime', topic='Classes & inheritance', notes='22', concepts=['deinit','arc'], docs=[('Deinitialization', DE)],
 sig='func lifecycle(_ names: [String]) -> [String]',
 statement="""`final class Tracked` logs `"init <name>"` in its initialiser and `"deinit <name>"` in `deinit` into a shared `Log` object passed to `init`.

 In `lifecycle`: inside a `do { }` scope create one `Tracked` per name into an array; then remove the **first** element (log `"removed"`); then leave the scope (log `"after scope"`). Return the log.""",
 solution="""
 final class Log { var lines: [String] = [] }

 final class Tracked {
     let name: String
     let log: Log
     init(_ name: String, log: Log) {
         self.name = name
         self.log = log
         log.lines.append("init \\(name)")
     }
     deinit { log.lines.append("deinit \\(name)") }
 }

 func lifecycle(_ names: [String]) -> [String] {
     let log = Log()
     do {
         var items = names.map { Tracked($0, log: log) }
         if !items.isEmpty {
             items.removeFirst()
             log.lines.append("removed")
         }
     }
     log.lines.append("after scope")
     return log.lines
 }
 """,
 explain="""ARC frees an object the moment its **last strong reference** disappears, running `deinit` right then — deterministic, unlike garbage collection. Removing from the array drops one reference immediately; the rest go when `items` goes out of scope.""",
 tests=[({'names':['a','b']},['init a','init b','deinit a','removed','deinit b','after scope']), {'names':[]}, {'names':['x','y','z']}]))
P.append(dict(id='class-let-reference', title='let on a Class Reference', topic='Classes & inheritance', notes='22', concepts=['let-vs-var','value-vs-reference','equality-vs-identity'], docs=[('Structures and Classes — Classes Are Reference Types', CS)],
 sig='func referenceDemo(_ renames: [String]) -> [String]',
 statement="""`final class Singer { var name = "Taylor" }`. Create `let original = Singer()` and `let alias = original`. Apply each rename to **`alias.name`** (legal even though `alias` is a `let`!). Return `[original.name, "\\(original === alias)"]`, then create `let clone = Singer(); clone.name = original.name` and append `"\\(clone === original)"`.""",
 solution="""
 final class Singer { var name = "Taylor" }

 func referenceDemo(_ renames: [String]) -> [String] {
     let original = Singer()
     let alias = original
     for name in renames { alias.name = name }
     let clone = Singer()
     clone.name = original.name
     return [original.name, "\\(original === alias)", "\\(clone === original)"]
 }
 """,
 explain="""`let` on a class reference freezes **which object** you point at, not the object's `var` properties. `===` compares identity — `clone` has equal contents but is a different instance.""",
 tests=[({'renames':['Justin','Ed']},['Ed','true','false']), {'renames':[]}]))
P.append(dict(id='static-vs-class-method', title='static vs class Methods', topic='Classes & inheritance', notes='22', diff='medium', concepts=['static-vs-class','final'], docs=[('Methods — Type Methods', ME)],
 sig='func typeNames(_ kinds: [String]) -> [String]',
 statement="""`class Shape` has `class func kind() -> String { "shape" }` and `static func library() -> String { "geometry" }`. `final class Circle: Shape` **overrides** `kind()` to return `"circle"`. (Try overriding `library()` — you can't.)

 For each input (`"shape"` / `"circle"`), pick the **metatype** (`Shape.self` or `Circle.self` stored as `Shape.Type`) and return `"<kind()>/<library()>"`.""",
 solution="""
 class Shape {
     class func kind() -> String { "shape" }
     static func library() -> String { "geometry" }
 }

 final class Circle: Shape {
     override class func kind() -> String { "circle" }
 }

 func typeNames(_ kinds: [String]) -> [String] {
     kinds.map { k in
         let type: Shape.Type = k == "circle" ? Circle.self : Shape.self
         return "\\(type.kind())/\\(type.library())"
     }
 }
 """,
 explain="""`class func` can be overridden and is dispatched on the **metatype** at runtime; `static func` is `class final func`. `Shape.Type` is the type of `Shape.self` and of any subclass's `.self`.""",
 tests=[({'kinds':['shape','circle']},['shape/geometry','circle/geometry']), {'kinds':[]}]))
P.append(dict(id='required-init-factory', title='required init & Self', topic='Classes & inheritance', diff='hard', notes='22', concepts=['required-init','self-vs-Self'], docs=[('Initialization — Required Initializers', IN)],
 sig='func spawnAll(_ kinds: [String]) -> [String]',
 statement="""`class Enemy` has `required init(level: Int)` and `class func make(level: Int) -> Self { Self(level: level) }`, plus `func describe() -> String` (`"enemy L<level>"`). Subclasses `Goblin` and `Dragon` override `describe()` (`"goblin L…"`, `"dragon L…"`) and must provide the `required` init.

 Inputs are `"goblin 3"`, `"dragon 10"` or `"enemy 1"`: call `make(level:)` on the right metatype and return `describe()`.""",
 solution="""
 class Enemy {
     let level: Int
     required init(level: Int) { self.level = level }
     class func make(level: Int) -> Self { Self(level: level) }
     func describe() -> String { "enemy L\\(level)" }
 }

 final class Goblin: Enemy {
     override func describe() -> String { "goblin L\\(level)" }
 }

 final class Dragon: Enemy {
     required init(level: Int) { super.init(level: level * 2) }
     override func describe() -> String { "dragon L\\(level)" }
 }

 func spawnAll(_ kinds: [String]) -> [String] {
     kinds.map { spec in
         let parts = spec.split(separator: " ")
         let type: Enemy.Type = switch parts[0] {
         case "goblin": Goblin.self
         case "dragon": Dragon.self
         default: Enemy.self
         }
         return type.make(level: Int(parts[1])!).describe()
     }
 }
 """,
 explain="""`Self(level:)` constructs whatever subclass the metatype refers to — only legal because `required` guarantees every subclass has that init (Goblin inherits it; Dragon re-declares it and doubles the level). `Self` in a class means the **dynamic** type.""",
 tests=[({'kinds':['goblin 3','dragon 10','enemy 1']},['goblin L3','dragon L20','enemy L1']), {'kinds':[]}]))
P.append(dict(id='type-casting-zoo', title='Type Casting with is / as?', topic='Classes & inheritance', notes='22', concepts=['type-casting','upcast-downcast','any-anyobject'], docs=[('Type Casting', TC)],
 sig='func castReport(_ items: [String]) -> [String]',
 statement="""Build an `[Any]` from the tokens: integers become `Int`, decimals `Double`, `"true"/"false"` `Bool`, anything else `String`. Then describe each element with a `switch` using **type-casting patterns**: `"int <n>"`, `"double <d>"`, `"bool <b>"`, `"string <s>"`. Finally append `"<count of strings>"` computed with `is`.""",
 solution="""
 func castReport(_ items: [String]) -> [String] {
     let values: [Any] = items.map { token -> Any in
         if let i = Int(token) { return i }
         if let d = Double(token) { return d }
         if let b = Bool(token) { return b }
         return token
     }
     var lines = values.map { value -> String in
         switch value {
         case let i as Int: "int \\(i)"
         case let d as Double: "double \\(d)"
         case let b as Bool: "bool \\(b)"
         case let s as String: "string \\(s)"
         default: "unknown"
         }
     }
     lines.append("\\(values.filter { $0 is String }.count)")
     return lines
 }
 """,
 explain="""`Any` erases static type information, so you need casts to get it back: `is` tests, `as?` conditionally casts, and `case let x as T` does both inside a `switch`. Prefer real types or enums over `[Any]` in real code.""",
 tests=[({'items':['42','3.5','true','hi']},['int 42','double 3.5','bool true','string hi','1']), {'items':[]}, {'items':['1e3','x','false','-0']}]))
# ---------- Protocols (§23)
P.append(dict(id='protocol-shapes', title='Protocols: Area & Perimeter', topic='Protocols', notes='23', concepts=['protocols','existential-any'], docs=[('Protocols — Protocol Syntax', PT)],
 sig='func describeShapes(_ specs: [[Double]]) -> [String]',
 compare='exact',
 statement="""Define `protocol Shape { var name: String { get }; var area: Double { get }; func perimeter() -> Double }` and conform `Square(side)`, `Rect(w, h)` and `Circle(r)`.

 Specs: `[s]` → square, `[w, h]` → rect, `[r, 0]`… no — `[-r]` (a negative single value) → circle of radius `r`. Store them in `[any Shape]` and return `"<name> a=<area> p=<perimeter>"` with both numbers formatted to **2 decimal places** (use `String(format: "%.2f", x)` from Foundation).""",
 solution="""
 import Foundation

 protocol Shape {
     var name: String { get }
     var area: Double { get }
     func perimeter() -> Double
 }

 struct Square: Shape {
     let side: Double
     var name: String { "square" }
     var area: Double { side * side }
     func perimeter() -> Double { 4 * side }
 }

 struct Rect: Shape {
     let w: Double, h: Double
     var name: String { "rect" }
     var area: Double { w * h }
     func perimeter() -> Double { 2 * (w + h) }
 }

 struct Circle: Shape {
     let r: Double
     var name: String { "circle" }
     var area: Double { .pi * r * r }
     func perimeter() -> Double { 2 * .pi * r }
 }

 func describeShapes(_ specs: [[Double]]) -> [String] {
     let shapes: [any Shape] = specs.map { s in
         if s.count == 2 { return Rect(w: s[0], h: s[1]) }
         return s[0] < 0 ? Circle(r: -s[0]) : Square(side: s[0])
     }
     return shapes.map { "\\($0.name) a=\\(String(format: "%.2f", $0.area)) p=\\(String(format: "%.2f", $0.perimeter()))" }
 }
 """,
 explain="""A protocol lists requirements; `{ get }` means "readable" — satisfiable by a `let`, a `var` or a computed property. `[any Shape]` is an array of **existentials**: boxes that can hold different concrete conforming types.""",
 tests=[({'specs':[[2],[3,4],[-1]]},['square a=4.00 p=8.00','rect a=12.00 p=14.00','circle a=3.14 p=6.28']), {'specs':[]}, {'specs':[[0.5],[-2.5],[1,1]]}]))
P[-1]['statement'] = P[-1]['statement'].replace("`[r, 0]`… no — `[-r]`", "`[-r]`")
P.append(dict(id='protocol-extension-default', title='Protocol Extensions: Default Behaviour', topic='Protocols', notes='24', concepts=['protocol-extension','pop'], docs=[('Protocols — Protocol Extensions', PT)],
 sig='func greetings(_ kinds: [String]) -> [String]',
 statement="""`protocol Greeter { var name: String { get }; func greet() -> String }` with a **protocol extension** providing a default `greet()` returning `"Hello, I'm <name>"` and an extra method `func greetTwice() -> String` (the greeting twice, joined by `" "`).

 `English(name: "Ann")` uses the default; `Pirate(name: "Jack")` implements `greet()` as `"Ahoy! <name> here"`. Kinds are `"en"`/`"pirate"` — return `greetTwice()` for each.""",
 solution="""
 protocol Greeter {
     var name: String { get }
     func greet() -> String
 }

 extension Greeter {
     func greet() -> String { "Hello, I'm \\(name)" }
     func greetTwice() -> String { greet() + " " + greet() }
 }

 struct English: Greeter { let name: String }

 struct Pirate: Greeter {
     let name: String
     func greet() -> String { "Ahoy! \\(name) here" }
 }

 func greetings(_ kinds: [String]) -> [String] {
     kinds.map { kind -> String in
         let g: any Greeter = kind == "pirate" ? Pirate(name: "Jack") : English(name: "Ann")
         return g.greetTwice()
     }
 }
 """,
 explain="""Because `greet()` is a protocol **requirement**, `greetTwice()` calls it through the witness table and gets Pirate's own version. Default implementations let conforming types opt out of boilerplate.""",
 tests=[({'kinds':['en','pirate']},["Hello, I'm Ann Hello, I'm Ann",'Ahoy! Jack here Ahoy! Jack here']), {'kinds':[]}]))
P.append(dict(id='predict-static-dispatch-trap', title='Predict: Protocol Extension Dispatch Trap', topic='Protocols', mode='predict', notes='24', diff='hard', concepts=['method-dispatch','protocol-extension'], docs=[('Protocols — Protocol Extensions', PT)],
 statement="""A famous interview question. `describe()` is a requirement; `nickname()` is **not** — it only exists in the extension. Predict what each call prints.""",
 snippet="""
 protocol Animal {
     func describe() -> String
 }

 extension Animal {
     func describe() -> String { "some animal" }
     func nickname() -> String { "critter" }
 }

 struct Cat: Animal {
     func describe() -> String { "a cat" }
     func nickname() -> String { "kitty" }
 }

 let cat = Cat()
 let animal: any Animal = cat
 print(cat.describe(), "|", cat.nickname())
 print(animal.describe(), "|", animal.nickname())
 """,
 explain="""Requirements are dispatched **dynamically** via the witness table, so `animal.describe()` finds Cat's version. Methods that exist only in a protocol extension are dispatched **statically** by the variable's type — `animal.nickname()` calls the extension's `"critter"` even though Cat has its own."""))
P.append(dict(id='comparable-version', title='Comparable: Semantic Versions', topic='Protocols', notes='23', diff='medium', concepts=['comparable','equatable-hashable','failable-init'], docs=[('Protocols — Adopting a Protocol Using a Synthesized Implementation', PT)],
 sig='func sortVersions(_ versions: [String]) -> [String]',
 statement="""Make `struct Version: Comparable, CustomStringConvertible` from strings like `"1.10.2"` (missing parts default to 0, so `"2"` == `"2.0.0"`) via a failable init. Sort ascending (skip invalid strings), deduplicate equal versions keeping the first spelling, and return their `description`s as originally written.""",
 solution="""
 struct Version: Comparable, CustomStringConvertible {
     let parts: [Int]
     let description: String

     init?(_ text: String) {
         let pieces = text.split(separator: ".", omittingEmptySubsequences: false)
         guard (1...3).contains(pieces.count) else { return nil }
         var nums: [Int] = []
         for piece in pieces {
             guard let n = Int(piece), n >= 0 else { return nil }
             nums.append(n)
         }
         parts = nums + Array(repeating: 0, count: 3 - nums.count)
         description = text
     }

     static func == (a: Version, b: Version) -> Bool { a.parts == b.parts }
     static func < (a: Version, b: Version) -> Bool { a.parts.lexicographicallyPrecedes(b.parts) }
 }

 func sortVersions(_ versions: [String]) -> [String] {
     var result: [Version] = []
     for v in versions.compactMap(Version.init).sorted() where result.last != v {
         result.append(v)
     }
     return result.map(\\.description)
 }
 """,
 explain="""Implementing `<` (and `==` when the synthesised one would compare the wrong fields — here `description` must not count) gives `sorted()`, `max()`, `>`, `<=` and friends. String comparison would wrongly put `"1.10"` before `"1.9"`. `sorted()` is stable, so the first spelling of equal versions survives.""",
 tests=[({'versions':['1.10.0','1.9.3','2','1.9.3','x.1']},['1.9.3','1.10.0','2']), {'versions':[]}, {'versions':['0.0.1','0.1','1','1.0.0','01.0']}]))
P.append(dict(id='protocol-composition-delegate', title='Delegation with a Weak Delegate', topic='Protocols', notes='23', diff='medium', concepts=['delegation','protocol-composition','weak-unowned'], docs=[('Protocols — Delegation', PT)],
 sig='func downloadDemo(_ files: [String], keepDelegate: Bool) -> [String]',
 statement="""`protocol DownloaderDelegate: AnyObject { func didFinish(_ file: String) }`. `final class Downloader` has `weak var delegate: DownloaderDelegate?` and `func download(_ file: String)` that calls `delegate?.didFinish(file)`; if there's no delegate it records `"dropped <file>"` in its own log.

 A `final class Screen: DownloaderDelegate` logs `"shown <file>"`. In `downloadDemo`, create the downloader and a screen, set the delegate, and if `keepDelegate` is `false` **release the screen** (set your only strong reference to `nil`) before downloading. Return the combined log (a shared `Log` object).""",
 solution="""
 final class Log { var lines: [String] = [] }

 protocol DownloaderDelegate: AnyObject {
     func didFinish(_ file: String)
 }

 final class Downloader {
     weak var delegate: DownloaderDelegate?
     let log: Log
     init(log: Log) { self.log = log }

     func download(_ file: String) {
         if let delegate { delegate.didFinish(file) } else { log.lines.append("dropped \\(file)") }
     }
 }

 final class Screen: DownloaderDelegate {
     let log: Log
     init(log: Log) { self.log = log }
     func didFinish(_ file: String) { log.lines.append("shown \\(file)") }
 }

 func downloadDemo(_ files: [String], keepDelegate: Bool) -> [String] {
     let log = Log()
     let downloader = Downloader(log: log)
     var screen: Screen? = Screen(log: log)
     downloader.delegate = screen
     if !keepDelegate { screen = nil }
     files.forEach(downloader.download)
     withExtendedLifetime(screen) {}
     return log.lines
 }
 """,
 explain="""Delegates are `weak` so the worker doesn't keep its owner alive (owner → worker → owner would be a cycle). `weak` requires a class-constrained protocol (`: AnyObject`). When the last strong reference goes, the weak `delegate` becomes `nil` automatically. `withExtendedLifetime` keeps `screen` alive until after the downloads when we *do* keep it.""",
 tests=[({'files':['a','b'],'keepDelegate':True},['shown a','shown b']), ({'files':['a'],'keepDelegate':False},['dropped a']), {'files':[],'keepDelegate':True}]))
# ---------- Extensions (§24)
P.append(dict(id='extension-int-helpers', title='Extending Int', topic='Extensions', notes='24', concepts=['extensions','computed-properties'], docs=[('Extensions — Computed Properties', EX)],
 sig='func intFacts(_ nums: [Int]) -> [String]',
 statement="""Extend `Int` with:
 - `var isPrime: Bool`
 - `var digits: [Int]` (of the magnitude, most significant first; `0` → `[0]`)
 - `func times(_ action: () -> Void)`

 Return `"<n>: prime=<isPrime> digits=<digits> ticks=<count>"` where `ticks` counts calls made by `n.times { … }` (0 for negative `n`).""",
 solution="""
 extension Int {
     var isPrime: Bool {
         guard self >= 2 else { return false }
         var d = 2
         while d * d <= self {
             if self % d == 0 { return false }
             d += 1
         }
         return true
     }

     var digits: [Int] {
         String(magnitude).compactMap(\\.wholeNumberValue)
     }

     func times(_ action: () -> Void) {
         guard self > 0 else { return }
         for _ in 0..<self { action() }
     }
 }

 func intFacts(_ nums: [Int]) -> [String] {
     nums.map { n in
         var ticks = 0
         n.times { ticks += 1 }
         return "\\(n): prime=\\(n.isPrime) digits=\\(n.digits) ticks=\\(ticks)"
     }
 }
 """,
 explain="""Extensions add computed properties and methods to types you don't own. They **can't** add stored properties. `times` takes a non-escaping closure, so it can mutate `ticks` captured from the caller.""",
 tests=[({'nums':[7,10]},['7: prime=true digits=[7] ticks=7','10: prime=false digits=[1, 0] ticks=10']), {'nums':[]}, {'nums':[0,1,2,-13,97]}]))
P.append(dict(id='extension-protocol-conformance', title='Retroactive Conformance via Extension', topic='Extensions', notes='24', diff='medium', concepts=['extensions','protocols','protocol-extension'], docs=[('Extensions — Adding Protocol Conformance with an Extension', EX)],
 sig='func summaries(ints: [Int], words: [String], flags: [Bool]) -> [String]',
 statement="""Declare `protocol Summarizable { var summary: String { get } }`. **Retroactively** conform `Int` (`"int(<n>)"`), `String` (`"str(<count>)"`) and `Array where Element: Summarizable` (`"[<summaries joined by ,>]"`) in extensions.

 Return `[ints.summary, words.summary, flags-as-Int.summary]` where each Bool maps to `1`/`0` first.""",
 solution="""
 protocol Summarizable {
     var summary: String { get }
 }

 extension Int: Summarizable {
     var summary: String { "int(\\(self))" }
 }

 extension String: Summarizable {
     var summary: String { "str(\\(count))" }
 }

 extension Array: Summarizable where Element: Summarizable {
     var summary: String { "[" + map(\\.summary).joined(separator: ",") + "]" }
 }

 func summaries(ints: [Int], words: [String], flags: [Bool]) -> [String] {
     [ints.summary, words.summary, flags.map { $0 ? 1 : 0 }.summary]
 }
 """,
 explain="""You can add a protocol conformance to **any** type, even standard library ones, in an extension. `extension Array: Summarizable where Element: Summarizable` is a **conditional conformance** — `[Int]` gets it, `[Bool]` doesn't (hence the map).""",
 tests=[({'ints':[1,2],'words':['hi','🦅'],'flags':[True,False]},['[int(1),int(2)]','[str(2),str(1)]','[int(1),int(0)]']), {'ints':[],'words':[],'flags':[]}]))
# ---------- Access control
P.append(dict(id='diag-private-access', title='Diagnostic: private Is Private', topic='Access control', mode='diagnostic', notes='21', concepts=['access-control','fileprivate-vs-private','encapsulation'], docs=[('Access Control', AC)],
 statement="""Declare `struct Vault { private var secret = "1234" }`, create one, and try to **read** `vault.secret` from top-level code. You pass when access is denied.""",
 starter="struct Vault {\n    var secret = \"1234\"\n}\n\nlet vault = Vault()\nprint(vault.secret)\n",
 solution="struct Vault {\n    private var secret = \"1234\"\n}\n\nlet vault = Vault()\nprint(vault.secret)\n",
 explain="""*'secret' is inaccessible due to 'private' protection level*. `private` limits access to the enclosing declaration (and its extensions in the same file). `fileprivate` would allow the whole file; `internal` (the default) the whole module.""",
 tests=[{'name':'Access denied','pattern':"inaccessible due to 'private' protection level"}]))
P.append(dict(id='diag-existential-member', title='Diagnostic: Protocol Type Hides Members', topic='Protocols', mode='diagnostic', notes='23', concepts=['existential-any','protocols','type-casting'], docs=[('Protocols — Protocols as Types', PT)],
 statement="""From your notes: `protocol Vehicle { func travel() }` and `struct Car: Vehicle` with an extra `openSunroof()`. Write `func commute(_ vehicle: any Vehicle)` that calls `vehicle.openSunroof()`. You pass when the compiler says the protocol type has no such member.""",
 starter="protocol Vehicle { func travel() }\n\nstruct Car: Vehicle {\n    func travel() {}\n    func openSunroof() {}\n}\n\nfunc commute(_ vehicle: any Vehicle) {\n    vehicle.travel()\n    if let car = vehicle as? Car { car.openSunroof() }\n}\n",
 solution="protocol Vehicle { func travel() }\n\nstruct Car: Vehicle {\n    func travel() {}\n    func openSunroof() {}\n}\n\nfunc commute(_ vehicle: any Vehicle) {\n    vehicle.openSunroof()\n}\n",
 explain="""*value of type 'any Vehicle' has no member 'openSunroof'*. Through a protocol type you only see the protocol's members; to reach concrete API you must downcast (`as? Car`) — which is often a sign the protocol is missing a requirement.""",
 tests=[{'name':'Member hidden','pattern':"has no member 'openSunroof'"}]))
P.append(dict(id='abstract-class-emulation', title='Emulating an Abstract Class', topic='Protocols', notes='23', diff='medium', concepts=['abstract-class','pop','protocol-extension'], docs=[('Protocols', PT)],
 sig='func report(_ sizes: [[Int]]) -> [String]',
 statement="""Swift has no `abstract` keyword. Model a "template method": `protocol Report` requires `var title: String` and `func rows() -> [String]`, and a protocol extension provides `func render() -> [String]` returning `["== <title> ==", rows…, "(<n> rows)"]`.

 `SalesReport(amounts)` titles itself `"Sales"` with rows `"$<amount>"`; `TeamReport(headcounts)` titles `"Team"` with rows `"team <i>: <count>"` (1-based). `sizes[0]` feeds sales, `sizes[1]` team. Return both renders concatenated.""",
 solution="""
 protocol Report {
     var title: String { get }
     func rows() -> [String]
 }

 extension Report {
     func render() -> [String] {
         let body = rows()
         return ["== \\(title) =="] + body + ["(\\(body.count) rows)"]
     }
 }

 struct SalesReport: Report {
     let amounts: [Int]
     var title: String { "Sales" }
     func rows() -> [String] { amounts.map { "$\\($0)" } }
 }

 struct TeamReport: Report {
     let headcounts: [Int]
     var title: String { "Team" }
     func rows() -> [String] { headcounts.enumerated().map { "team \\($0.offset + 1): \\($0.element)" } }
 }

 func report(_ sizes: [[Int]]) -> [String] {
     SalesReport(amounts: sizes[0]).render() + TeamReport(headcounts: sizes[1]).render()
 }
 """,
 explain="""Protocol requirements are the "abstract" parts; the extension is the shared concrete algorithm. Unlike an abstract base class, forgetting a requirement is a **compile-time** error, and structs can participate.""",
 tests=[({'sizes':[[5,10],[3]]},['== Sales ==','$5','$10','(2 rows)','== Team ==','team 1: 3','(1 rows)']), {'sizes':[[],[]]}]))
# ---------- Design problems (custom harness)
P.append(dict(id='design-min-stack', title='Design: Min Stack (struct)', topic='Structs', notes='21', diff='medium', concepts=['mutating','generics','optionals'], docs=[('Generics — Generic Types','LanguageGuide/Generics')],
 statement="""Implement `struct MinStack` with `mutating func push(_ x: Int)`, `mutating func pop() -> Int?`, `func top() -> Int?` and `func min() -> Int?` — all **O(1)**.

 The judge drives it LeetCode-style from a list of operations and prints each result (`nil` shows as `null`):
 ```
 ops:  push push push min pop min top
 args: [-2] [0]  [-3]  []  []  []  []
 out:  null null null -3  -3  -2  0
 ```""",
 starter="""
 struct MinStack {
     mutating func push(_ x: Int) {}
     mutating func pop() -> Int? { nil }
     func top() -> Int? { nil }
     func min() -> Int? { nil }
 }
 """,
 solution="""
 struct MinStack {
     private var items: [(value: Int, min: Int)] = []

     mutating func push(_ x: Int) {
         items.append((x, Swift.min(x, items.last?.min ?? x)))
     }

     mutating func pop() -> Int? {
         items.popLast()?.value
     }

     func top() -> Int? { items.last?.value }
     func min() -> Int? { items.last?.min }
 }
 """,
 harness=OPS_HARNESS_HEADER + """
 func __run(_ __i: __Input) async throws -> [Int?] {
     var stack = MinStack()
     var out: [Int?] = []
     for (op, args) in zip(__i.ops, __i.args) {
         switch op {
         case "push": stack.push(args[0]); out.append(nil)
         case "pop": out.append(stack.pop())
         case "top": out.append(stack.top())
         default: out.append(stack.min())
         }
     }
     return out
 }
 """,
 explain="""Store the running minimum **alongside** each element, so popping restores the previous minimum for free. `popLast()` returns an optional (unlike `removeLast()`, which traps on empty). Inside the type, `Swift.min` refers to the global function rather than the `min()` method.""",
 tests=[({'ops':['push','push','push','min','pop','min','top'],'args':[[-2],[0],[-3],[],[],[],[]]},[None,None,None,-3,-3,-2,0]),
        {'ops':['pop','min','top'],'args':[[],[],[]]},
        {'ops':['push','push','push','pop','pop','min'],'args':[[5],[5],[1],[],[],[]]}]))
P.append(dict(id='design-parking-lot', title='Design: Parking Lot (classes)', topic='Classes & inheritance', notes='22', diff='medium', concepts=['class-definition','struct-vs-class','enums'], docs=[('Structures and Classes', CS)],
 statement="""Implement `final class ParkingLot` with `init(big: Int, medium: Int, small: Int)` and `func park(_ carType: Int) -> Bool` (1 = big, 2 = medium, 3 = small). A car only fits a slot of **its own** size.

 The judge sends `ops = ["init", "park", …]` with `args` like LeetCode's *Design Parking System*; `init` yields `null`.""",
 starter="""
 final class ParkingLot {
     init(big: Int, medium: Int, small: Int) {}
     func park(_ carType: Int) -> Bool { false }
 }
 """,
 solution="""
 final class ParkingLot {
     enum Size: Int { case big = 1, medium, small }
     private var free: [Size: Int]

     init(big: Int, medium: Int, small: Int) {
         free = [.big: big, .medium: medium, .small: small]
     }

     func park(_ carType: Int) -> Bool {
         guard let size = Size(rawValue: carType), let slots = free[size], slots > 0 else { return false }
         free[size] = slots - 1
         return true
     }
 }
 """,
 harness=OPS_HARNESS_HEADER + """
 func __run(_ __i: __Input) async throws -> [Bool?] {
     var lot: ParkingLot?
     var out: [Bool?] = []
     for (op, args) in zip(__i.ops, __i.args) {
         if op == "init" {
             lot = ParkingLot(big: args[0], medium: args[1], small: args[2])
             out.append(nil)
         } else {
             out.append(lot!.park(args[0]))
         }
     }
     return out
 }
 """,
 explain="""A class suits an object with identity and shared mutable state. A nested enum with raw values turns the magic numbers into a type, and the failable `Size(rawValue:)` rejects bad input.""",
 tests=[({'ops':['init','park','park','park','park'],'args':[[1,1,0],[1],[2],[3],[1]]},[None,True,True,False,False]),
        {'ops':['init','park','park','park'],'args':[[0,0,2],[3],[3],[3]]},
        {'ops':['init','park'],'args':[[1,1,1],[4]]}]))

write_all(P, 'intermediate', 300)
