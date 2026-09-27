import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
OC='LanguageGuide/OptionalChaining'; TB='LanguageGuide/TheBasics'; EH='LanguageGuide/ErrorHandling'; CL='LanguageGuide/Closures'; BO='LanguageGuide/BasicOperators'
P=[]
# ---------- Optionals (§25)
P.append(dict(id='parse-sum-optionals', title='Sum the Parsable Numbers', topic='Optionals', notes='25', concepts=['optionals','compactmap-flatmap','failable-init'], docs=[('The Basics — Optionals', TB)],
 sig='func sumOfNumbers(_ tokens: [String]) -> Int',
 statement="""`Int("42")` returns an `Int?` — it's a **failable initialiser**. Sum only the tokens that parse as integers.

 ```swift
 sumOfNumbers(["3", "x", "-2", "4.5", " 7"])   // 1   (" 7" and "4.5" don't parse)
 ```""",
 solution="func sumOfNumbers(_ tokens: [String]) -> Int {\n    tokens.compactMap { Int($0) }.reduce(0, +)\n}\n",
 explain="""`compactMap` unwraps and drops `nil`s in one step. `Int(String)` is strict: no whitespace, no decimal point, optional leading `+`/`-`.""",
 tests=[({'tokens':['3','x','-2','4.5',' 7']},1), {'tokens':[]}, {'tokens':['+5','-0','007']}, {'tokens':['9223372036854775806','1']}, {'tokens':['a','b']}]))
P.append(dict(id='if-let-chain', title='Bind Several Optionals', topic='Optionals', notes='25', concepts=['optional-binding','multiple-optional-binding','if-let-vs-guard'], docs=[('The Basics — Optional Binding', TB)],
 sig='func rectangleArea(width: String?, height: String?) -> String',
 statement="""Both inputs may be missing or non-numeric. Using **one** `if let … , let …, condition` statement, return `"area <w*h>"` when both parse to positive integers; otherwise `"invalid"`.""",
 solution="""
 func rectangleArea(width: String?, height: String?) -> String {
     if let width, let w = Int(width), let height, let h = Int(height), w > 0, h > 0 {
         return "area \\(w * h)"
     }
     return "invalid"
 }
 """,
 explain="""Comma-separated clauses in an `if` all must succeed, evaluated left to right, and later ones can use earlier bindings. `if let width` is Swift 5.7 shorthand for `if let width = width`.""",
 tests=[({'width':'3','height':'4'},'area 12'), ({'width':None,'height':'4'},'invalid'), {'width':'3','height':'x'}, {'width':'0','height':'5'}, {'width':'-2','height':'-3'}, {'width':None,'height':None}]))
P.append(dict(id='guard-let-validate', title='guard let: Validate a Sign-up', topic='Optionals', notes='25', concepts=['guard','if-let-vs-guard'], docs=[('Control Flow — Early Exit','LanguageGuide/ControlFlow')],
 sig='func validateSignup(username: String?, age: String?, email: String?) -> String',
 statement="""Validate in this order, returning the **first** failure message:
 1. username present and 3–16 characters → else `"bad username"`
 2. age present, an integer, and ≥ 13 → else `"bad age"`
 3. email present and contains exactly one `@` with text on both sides → else `"bad email"`

 Otherwise return `"welcome <username>"`. Use a `guard` for each rule so the happy path stays unindented.""",
 solution="""
 func validateSignup(username: String?, age: String?, email: String?) -> String {
     guard let username, (3...16).contains(username.count) else { return "bad username" }
     guard let age, let years = Int(age), years >= 13 else { return "bad age" }
     guard let email else { return "bad email" }
     let parts = email.split(separator: "@", omittingEmptySubsequences: false)
     guard parts.count == 2, !parts[0].isEmpty, !parts[1].isEmpty else { return "bad email" }
     return "welcome \\(username)"
 }
 """,
 explain="""`guard` inverts the logic: state what must be true, exit otherwise. Bindings made by `guard let` remain in scope **after** the guard — unlike `if let`. `omittingEmptySubsequences: false` keeps empty pieces so `"@x"` is detected.""",
 tests=[({'username':'varun','age':'25','email':'v@x.io'},'welcome varun'), ({'username':'vi','age':'25','email':'v@x.io'},'bad username'), {'username':'varun','age':None,'email':'v@x.io'}, {'username':'varun','age':'12','email':'v@x.io'}, {'username':'varun','age':'20','email':'a@b@c'}, {'username':'varun','age':'20','email':'@x'}, {'username':None,'age':None,'email':None}, {'username':'varun','age':'2x','email':'a@b'}]))
P.append(dict(id='nil-coalescing-config', title='Config with ?? Fallbacks', topic='Optionals', notes='25', concepts=['nil-coalescing','dictionary-basics'], docs=[('Basic Operators — Nil-Coalescing Operator', BO)],
 sig='func resolvePort(env: [String: String], args: [String: String]) -> Int',
 statement="""Resolve a port number: use `args["port"]` if it parses as an `Int`, else `env["PORT"]` if it parses, else `8080`. Write it as a single chain of `??`.""",
 solution="func resolvePort(env: [String: String], args: [String: String]) -> Int {\n    args[\"port\"].flatMap { Int($0) } ?? env[\"PORT\"].flatMap { Int($0) } ?? 8080\n}\n",
 explain="""`??` chains right-to-left and the right side is only evaluated if needed (it's an autoclosure). `Optional.flatMap` runs a transform returning an optional without producing `Int??` — `args["port"].map { Int($0) }` would be doubly optional.""",
 tests=[({'env':{'PORT':'3000'},'args':{'port':'4000'}},4000), ({'env':{'PORT':'3000'},'args':{}},3000), {'env':{},'args':{}}, {'env':{'PORT':'x'},'args':{'port':'y'}}, {'env':{'PORT':'1'},'args':{'port':'nope'}}]))
P.append(dict(id='optional-chaining-company', title='Optional Chaining Through a Model', topic='Optionals', notes='25', concepts=['optional-chaining'], docs=[('Optional Chaining', OC)],
 sig='func ceoCityLengths(_ records: [[String]]) -> [Int?]',
 statement="""Model: `Company` has an optional `ceo: Person?`; `Person` has an optional `address: Address?`; `Address` has `city: String`. Each record is `[companyName, ceoName, city]` where `"-"` means *missing* (a missing CEO name means no CEO; a missing city means the CEO has no address).

 Build the models, then return `company.ceo?.address?.city.count` for each.""",
 solution="""
 struct Address { let city: String }
 struct Person { let name: String; let address: Address? }
 struct Company { let name: String; let ceo: Person? }

 func ceoCityLengths(_ records: [[String]]) -> [Int?] {
     records.map { r in
         let address = r[2] == "-" ? nil : Address(city: r[2])
         let ceo = r[1] == "-" ? nil : Person(name: r[1], address: address)
         let company = Company(name: r[0], ceo: ceo)
         return company.ceo?.address?.city.count
     }
 }
 """,
 explain="""`a?.b?.c.count` short-circuits to `nil` at the first missing link, and the result is **one level** of optional (`Int?`), however many `?`s are in the chain.""",
 tests=[({'records':[['Acme','Ana','Lisbon'],['Void','-','-'],['Solo','Bo','-']]},[6,None,None]), {'records':[]}, {'records':[['X','Y','São Paulo']]}]))
P.append(dict(id='optional-map-flatmap', title='Optional map vs flatMap', topic='Optionals', notes='25', diff='medium', concepts=['optionals','compactmap-flatmap'], docs=[('The Basics — Optionals', TB)],
 sig='func squaredFirstNumber(_ csv: String?) -> Int?',
 statement="""Given an optional CSV line, return the square of its **first** field if it parses as an integer. Use `Optional.flatMap` / `Optional.map` rather than `if let` — no `!` and no `if`.

 ```swift
 squaredFirstNumber("4,x,y")  // 16
 squaredFirstNumber("x,4")    // nil
 squaredFirstNumber(nil)      // nil
 ```""",
 solution="""
 func squaredFirstNumber(_ csv: String?) -> Int? {
     csv
         .flatMap { $0.split(separator: ",", omittingEmptySubsequences: false).first }
         .flatMap { Int($0) }
         .map { $0 * $0 }
 }
 """,
 explain="""On an `Optional`, `map` transforms the wrapped value if present; `flatMap` does the same for transforms that themselves return optionals (avoiding `T??`). This is the same shape as `Array.map`/`flatMap` — Optional is a container of zero or one element.""",
 tests=[({'csv':'4,x,y'},16), ({'csv':'x,4'},None), ({'csv':None},None), {'csv':''}, {'csv':'-3'}, {'csv':',5'}]))
P.append(dict(id='predict-optional-printing', title='Predict: Printing Optionals', topic='Optionals', mode='predict', notes='25', concepts=['optionals','implicitly-unwrapped','nil-coalescing'], docs=[('The Basics — Optionals', TB)],
 statement="Predict the output exactly. (The compiler emits a warning about implicitly converting an optional to `Any` — the output is what matters.)",
 snippet="""
 let a: Int? = 5
 let b: Int? = nil
 let c: Int! = 7
 print(a as Any)
 print(b as Any)
 print(a ?? 0, b ?? 0)
 print(c + 1)
 let d = c
 print(type(of: d))
 print(a.map { $0 * 2 } as Any, b.map { $0 * 2 } as Any)
 """,
 explain="""Printing an optional shows `Optional(5)` — a hint you forgot to unwrap. `Int!` is force-unwrapped only where a non-optional is **required** (`c + 1`); when the type can be inferred as an optional (`let d = c`), it stays `Optional<Int>`."""))
# ---------- Error handling (§19)
P.append(dict(id='check-password-throws', title='Throwing Password Check', topic='Error handling', notes='19', concepts=['error-handling','enums'], docs=[('Error Handling', EH)],
 sig='func checkPassword(_ password: String) throws -> String',
 statement="""From your notes. Declare `enum PasswordError: Error { case short, obvious }`. Throw `.short` if fewer than 5 characters, `.obvious` if the password is `"12345"` or `"password"`, return `"OK"` if under 10 characters, otherwise `"Good"`.

 The judge calls `try checkPassword(...)` — a thrown error shows up as `{"$error": "<case>"}`.""",
 starter="""
 enum PasswordError: Error {
     case short, obvious
 }

 func checkPassword(_ password: String) throws -> String {
     return ""
 }
 """,
 solution="""
 enum PasswordError: Error {
     case short, obvious
 }

 func checkPassword(_ password: String) throws -> String {
     if password.count < 5 { throw PasswordError.short }
     if ["12345", "password"].contains(password) { throw PasswordError.obvious }
     return password.count < 10 ? "OK" : "Good"
 }
 """,
 explain="""Errors are ordinary values of types conforming to `Error`; enums fit because failure modes are a closed set. `throws` marks the function, `throw` raises, and callers must `try`. Note `"12345"` is 5 characters, so it passes the length check and hits `.obvious`.""",
 tests=[({'password':'abc'},{'$error':'short'}), ({'password':'12345'},{'$error':'obvious'}), {'password':'swiftly'}, {'password':'correct horse battery'}, {'password':'password'}, {'password':''}]))
P.append(dict(id='do-catch-patterns', title='do/catch with Multi-Pattern Catches', topic='Error handling', notes='19', diff='medium', concepts=['multi-pattern-catch','error-handling','associated-values'], docs=[('Error Handling — Handling Errors Using Do-Catch', EH)],
 sig='func vend(_ requests: [String]) -> [String]',
 statement="""A vending machine (given in the starter) throws `VendingError`. Process each request and report:
 - success → `"got <item>"`
 - `.invalidSelection` **or** `.outOfStock` → `"unavailable"` (one multi-pattern `catch`)
 - `.insufficientFunds(let needed)` → `"insert <needed> more"`
 - anything else → `"error"`""",
 starter="""
 enum VendingError: Error {
     case invalidSelection
     case outOfStock
     case insufficientFunds(coinsNeeded: Int)
     case machineJammed
 }

 func buy(_ item: String) throws -> String {
     switch item {
     case "chips", "candy": return item
     case "soda": throw VendingError.outOfStock
     case "caviar": throw VendingError.insufficientFunds(coinsNeeded: 99)
     case "shake": throw VendingError.machineJammed
     default: throw VendingError.invalidSelection
     }
 }

 func vend(_ requests: [String]) -> [String] {
     // call buy(_:) for each request and handle every error
     return []
 }
 """,
 solution="""
 enum VendingError: Error {
     case invalidSelection
     case outOfStock
     case insufficientFunds(coinsNeeded: Int)
     case machineJammed
 }

 func buy(_ item: String) throws -> String {
     switch item {
     case "chips", "candy": return item
     case "soda": throw VendingError.outOfStock
     case "caviar": throw VendingError.insufficientFunds(coinsNeeded: 99)
     case "shake": throw VendingError.machineJammed
     default: throw VendingError.invalidSelection
     }
 }

 func vend(_ requests: [String]) -> [String] {
     requests.map { request in
         do {
             return "got \\(try buy(request))"
         } catch VendingError.invalidSelection, VendingError.outOfStock {
             return "unavailable"
         } catch VendingError.insufficientFunds(let needed) {
             return "insert \\(needed) more"
         } catch {
             return "error"
         }
     }
 }
 """,
 explain="""`catch` clauses pattern-match top to bottom like `switch` cases; a clause can list **several patterns** and bind associated values. A final bare `catch` (with implicit `error`) is needed because Swift can't prove untyped throws exhaustive.""",
 tests=[({'requests':['chips','soda','caviar','shake','gum']},['got chips','unavailable','insert 99 more','error','unavailable']), {'requests':[]}, {'requests':['candy','candy']}]))
P.append(dict(id='try-optional', title='try? to Optional', topic='Error handling', notes='19', concepts=['try-variants','error-handling'], docs=[('Error Handling — Converting Errors to Optional Values', EH)],
 sig='func safeDivisions(_ pairs: [[Int]]) -> [Int?]',
 statement="""Write `func divide(_ a: Int, by b: Int) throws -> Int` that throws a `DivisionError.byZero` when `b == 0` (and also throws `.overflow` for `Int.min / -1`, which would trap). `safeDivisions` returns `try? divide(...)` for each `[a, b]` pair.""",
 solution="""
 enum DivisionError: Error { case byZero, overflow }

 func divide(_ a: Int, by b: Int) throws -> Int {
     guard b != 0 else { throw DivisionError.byZero }
     let (q, overflow) = a.dividedReportingOverflow(by: b)
     guard !overflow else { throw DivisionError.overflow }
     return q
 }

 func safeDivisions(_ pairs: [[Int]]) -> [Int?] {
     pairs.map { try? divide($0[0], by: $0[1]) }
 }
 """,
 explain="""`try?` turns "throws or returns T" into `T?`, discarding the error — handy when you only care whether it worked. `Int.min / -1` is the one integer division that overflows.""",
 tests=[({'pairs':[[10,2],[1,0]]},[5,None]), {'pairs':[]}, {'pairs':[[-9223372036854775808,-1],[7,-2]]}]))
P.append(dict(id='defer-order', title='defer Runs in Reverse', topic='Error handling', notes='19', concepts=['defer'], docs=[('Error Handling — Specifying Cleanup Actions', EH)],
 sig='func runSteps(_ steps: [String]) -> [String]',
 statement="""Simulate opening resources. For each step name, log `"open <name>"` and register a `defer` that logs `"close <name>"`. If a step is named `"fail"`, log `"failing"` and stop (return early). Return the full log, including the `close` lines produced as the function exits.

 Hint: `defer` inside a `for` body runs at the end of **each iteration** — so recurse (or use a helper) to keep the resources nested.""",
 solution="""
 final class Log { var lines: [String] = [] }

 func open(_ steps: ArraySlice<String>, _ log: Log) {
     guard let name = steps.first else { return }
     if name == "fail" {
         log.lines.append("failing")
         return
     }
     log.lines.append("open \\(name)")
     defer { log.lines.append("close \\(name)") }
     open(steps.dropFirst(), log)
 }

 func runSteps(_ steps: [String]) -> [String] {
     let log = Log()
     open(steps[...], log)
     return log.lines
 }
 """,
 explain="""A `defer` runs when its **enclosing scope** exits — however it exits. Nested scopes unwind innermost first, so cleanup happens in reverse order of acquisition (just like multiple `defer`s in one scope run bottom-up).""",
 tests=[({'steps':['db','file']},['open db','open file','close file','close db']), {'steps':[]}, {'steps':['a','fail','b']}, {'steps':['x','y','z']}]))
P.append(dict(id='result-type', title='Result Instead of throws', topic='Error handling', notes='19', diff='medium', concepts=['result-type','error-handling'], docs=[('Error Handling', EH)],
 sig='func parseAges(_ raw: [String]) -> [String]',
 statement="""Write `func parseAge(_ s: String) -> Result<Int, AgeError>` where `enum AgeError: Error { case notANumber, negative, unrealistic }` (> 150 is unrealistic). For each input produce `"ok <age>"` or `"fail <error>"` by `switch`ing on the result.

 Then for fun: the **sum** of successful ages should be appended as a final line `"total <n>"`, computed with `compactMap { try? $0.get() }`.""",
 solution="""
 enum AgeError: Error { case notANumber, negative, unrealistic }

 func parseAge(_ s: String) -> Result<Int, AgeError> {
     guard let n = Int(s) else { return .failure(.notANumber) }
     if n < 0 { return .failure(.negative) }
     if n > 150 { return .failure(.unrealistic) }
     return .success(n)
 }

 func parseAges(_ raw: [String]) -> [String] {
     let results = raw.map(parseAge)
     var lines = results.map { result in
         switch result {
         case .success(let age): "ok \\(age)"
         case .failure(let error): "fail \\(error)"
         }
     }
     lines.append("total \\(results.compactMap { try? $0.get() }.reduce(0, +))")
     return lines
 }
 """,
 explain="""`Result<Success, Failure>` stores an outcome as a value — storable, passable, switchable. `get()` converts back to throwing style. With a concrete `Failure` type, the switch over errors is exhaustive.""",
 tests=[({'raw':['30','x','-1','200']},['ok 30','fail notANumber','fail negative','fail unrealistic','total 30']), {'raw':[]}, {'raw':['0','150','151']}]))
P.append(dict(id='typed-throws', title='Typed throws (Swift 6)', topic='Error handling', notes='19', diff='medium', concepts=['error-handling','generic-constraints'], docs=[('Error Handling — Specifying the Error Type', EH)],
 sig='func withdrawals(balance: Int, amounts: [Int]) -> [String]',
 statement="""Write `func withdraw(_ amount: Int, from balance: inout Int) throws(BankError)` using Swift 6 **typed throws**, with `enum BankError: Error { case invalidAmount, insufficientFunds(short: Int) }`.

 Apply each amount in order to a running balance and log `"ok -> <balance>"`, `"invalid"` or `"short by <n>"`. Because the error type is known, your `catch` needs no bare fallback — `error` is already a `BankError`. (Inside a closure, write `do throws(BankError) { … }`.)""",
 solution="""
 enum BankError: Error {
     case invalidAmount
     case insufficientFunds(short: Int)
 }

 func withdraw(_ amount: Int, from balance: inout Int) throws(BankError) {
     guard amount > 0 else { throw .invalidAmount }
     guard amount <= balance else { throw .insufficientFunds(short: amount - balance) }
     balance -= amount
 }

 func withdrawals(balance: Int, amounts: [Int]) -> [String] {
     var current = balance
     return amounts.map { amount in
         do throws(BankError) {
             try withdraw(amount, from: &current)
             return "ok -> \\(current)"
         } catch {
             switch error {
             case .invalidAmount: return "invalid"
             case .insufficientFunds(let short): return "short by \\(short)"
             }
         }
     }
 }
 """,
 explain="""`throws(BankError)` (SE-0413) tells callers exactly which error type can come out, so `catch` binds `error` as `BankError` and the switch is exhaustive. In a plain function body the `do` infers its error type; **inside a closure** you spell it out with `do throws(BankError) { … }` — otherwise `error` is `any Error`. Your notes' `withdraw` bug (refusing when `funds == amount`) is avoided with `<=`.""",
 tests=[({'balance':100,'amounts':[30,100,70,0]},['ok -> 70','short by 30','ok -> 0','invalid']), {'balance':0,'amounts':[]}, {'balance':50,'amounts':[-5,50,1]}]))
P.append(dict(id='rethrows-map', title='rethrows: Your Own map', topic='Error handling', notes='19', diff='medium', concepts=['rethrows','generics','closures'], docs=[('Declarations — Rethrowing Functions and Methods','ReferenceManual/Declarations')],
 sig='func demo(_ words: [String]) -> [String]',
 statement="""Add `func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T]` to `Array`. Because it `rethrows`, calling it with a **non-throwing** closure needs no `try`.

 In `demo`: (1) uppercase every word with `myMap` **without** `try`; (2) then `try? words.myMap(parse)` where `parse` throws for words containing digits — append `"parsed"` or `"rejected"`.""",
 starter="""
 extension Array {
     // func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T]
 }

 struct HasDigits: Error {}

 func parse(_ word: String) throws -> String {
     if word.contains(where: \\.isNumber) { throw HasDigits() }
     return word
 }

 func demo(_ words: [String]) -> [String] {
     return []
 }
 """,
 solution="""
 extension Array {
     func myMap<T>(_ transform: (Element) throws -> T) rethrows -> [T] {
         var out: [T] = []
         out.reserveCapacity(count)
         for element in self { out.append(try transform(element)) }
         return out
     }
 }

 struct HasDigits: Error {}

 func parse(_ word: String) throws -> String {
     if word.contains(where: \\.isNumber) { throw HasDigits() }
     return word
 }

 func demo(_ words: [String]) -> [String] {
     var result = words.myMap { $0.uppercased() }
     result.append((try? words.myMap(parse)) != nil ? "parsed" : "rejected")
     return result
 }
 """,
 explain="""`rethrows` means "I only throw if the closure you gave me throws". That's why the standard `map` needs `try` only with throwing closures. Inside, `try transform(element)` is allowed because the function rethrows.""",
 tests=[({'words':['a','b']},['A','B','parsed']), {'words':[]}, {'words':['r2d2','c3po']}]))
P.append(dict(id='predict-defer-throw', title='Predict: defer and Errors', topic='Error handling', mode='predict', notes='19', concepts=['defer','error-handling','try-variants'], docs=[('Error Handling', EH)],
 statement="Predict the output. Pay attention to **when** each `defer` runs relative to the `catch`.",
 snippet="""
 struct Boom: Error {}

 func work(_ fail: Bool) throws -> Int {
     print("start \\(fail)")
     defer { print("cleanup A") }
     defer { print("cleanup B") }
     if fail { throw Boom() }
     print("finish")
     return 1
 }

 do {
     _ = try work(false)
     _ = try work(true)
     print("unreachable")
 } catch {
     print("caught \\(error)")
 }
 print(try? work(true) as Any)
 """,
 explain="""`defer` blocks run in **reverse** order when the scope exits — including when it exits by throwing, *before* control reaches the `catch`. `try?` swallows the error into `nil`."""))
# ---------- Closures (§20)
P.append(dict(id='closure-shortening', title='The Shortening Ladder', topic='Closures', notes='20', concepts=['closures','trailing-closure'], docs=[('Closures — Closure Expressions', CL)],
 sig='func tNames(_ team: [String]) -> [String]',
 statement="""From your notes: keep names starting with "t" (case-insensitive), sorted **by length then alphabetically**. Write it with trailing closures and `$0`/`$1` shorthand — no `return`, no parameter types.""",
 solution="""
 func tNames(_ team: [String]) -> [String] {
     team
         .filter { $0.lowercased().hasPrefix("t") }
         .sorted { ($0.count, $0) < ($1.count, $1) }
 }
 """,
 explain="""The ladder: full `{ (name: String) -> Bool in return … }` → inferred types → implicit return → trailing closure → `$0`. Stop at whatever is clearest; `$0` shines in one-liners.""",
 tests=[({'team':['Gloria','Suzzanne','Tiffany','Tasha','trisha']},['Tasha','trisha','Tiffany']), {'team':[]}, {'team':['tom','Tim','ann','tea']}]))
P.append(dict(id='make-counter', title='Closures Capture State', topic='Closures', notes='20', concepts=['capturing-values','closures'], docs=[('Closures — Capturing Values', CL)],
 sig='func counterDemo(_ calls: [String]) -> [Int]',
 statement="""Write `func makeCounter(step: Int) -> () -> Int` returning a closure that adds `step` to a **captured** running total and returns it.

 `counterDemo` creates two counters — `a = makeCounter(step: 1)` and `b = makeCounter(step: 10)` — and calls them in the order given by `calls` (`"a"` or `"b"`), returning each result.""",
 solution="""
 func makeCounter(step: Int) -> () -> Int {
     var total = 0
     return {
         total += step
         return total
     }
 }

 func counterDemo(_ calls: [String]) -> [Int] {
     let a = makeCounter(step: 1)
     let b = makeCounter(step: 10)
     return calls.map { $0 == "a" ? a() : b() }
 }
 """,
 explain="""The returned closure captures `total` **by reference**, keeping it alive after `makeCounter` returns. Each call to `makeCounter` creates a fresh `total`, so `a` and `b` are independent.""",
 tests=[({'calls':['a','a','b','a','b']},[1,2,10,3,20]), {'calls':[]}, {'calls':['b','b','b']}]))
P.append(dict(id='capture-list-snapshot', title='Capture Lists Snapshot Values', topic='Closures', notes='20', diff='medium', concepts=['capture-list','capturing-values'], docs=[('Closures — Capturing Values', CL),('Automatic Reference Counting — Defining a Capture List','LanguageGuide/AutomaticReferenceCounting')],
 sig='func captureDemo(start: Int) -> [Int]',
 statement="""Set `var x = start`. Create `let byRef = { x }` and `let bySnapshot = { [x] in x }`. Then `x += 5` and return `[byRef(), bySnapshot()]`.""",
 solution="""
 func captureDemo(start: Int) -> [Int] {
     var x = start
     let byRef = { x }
     let bySnapshot = { [x] in x }
     x += 5
     return [byRef(), bySnapshot()]
 }
 """,
 explain="""Normally closures capture the **variable**, so they see later changes. A capture list `[x]` copies the **value** at the moment the closure is created. The same syntax (`[weak self]`) controls reference strength.""",
 tests=[({'start':1},[6,1]), {'start':0}, {'start':-5}]))
P.append(dict(id='escaping-handlers', title='@escaping: Store Callbacks', topic='Closures', notes='20', diff='medium', concepts=['escaping','closures'], docs=[('Closures — Escaping Closures', CL)],
 sig='func eventBus(_ events: [String]) -> [String]',
 statement="""Build a `final class EventBus` with `func subscribe(_ handler: @escaping (String) -> Void)` that **stores** handlers, and `func publish(_ event: String)` that calls every stored handler.

 `eventBus` subscribes two handlers that append `"A:<event>"` and `"B:<event>"` to a log (a class instance), publishes each event, and returns the log. Try removing `@escaping` and read the error.""",
 solution="""
 final class EventBus {
     private var handlers: [(String) -> Void] = []

     func subscribe(_ handler: @escaping (String) -> Void) {
         handlers.append(handler)
     }

     func publish(_ event: String) {
         for handler in handlers { handler(event) }
     }
 }

 final class Log { var lines: [String] = [] }

 func eventBus(_ events: [String]) -> [String] {
     let bus = EventBus()
     let log = Log()
     bus.subscribe { log.lines.append("A:\\($0)") }
     bus.subscribe { log.lines.append("B:\\($0)") }
     events.forEach(bus.publish)
     return log.lines
 }
 """,
 explain="""A closure that's **stored** outlives the call, so it must be `@escaping` — without it: *converting non-escaping parameter to generic parameter may allow it to escape*. Escaping closures are where retain cycles (`self` → handler → `self`) come from.""",
 tests=[({'events':['start','stop']},['A:start','B:start','A:stop','B:stop']), {'events':[]}]))
P.append(dict(id='autoclosure-log', title='@autoclosure: Lazy Logging', topic='Closures', notes='20', diff='medium', concepts=['autoclosure','nil-coalescing'], docs=[('Closures — Autoclosures', CL)],
 sig='func loggingDemo(level: Int) -> [String]',
 statement="""Write `func debugLog(_ message: @autoclosure () -> String, level: Int, into log: Log)` that only **evaluates** `message` when `level >= 2`.

 In `loggingDemo`, call `debugLog(expensive("A"), level: level, into: log)` and `debugLog(expensive("B"), level: 3, into: log)`, where `expensive(_:)` appends `"computed <x>"` to the log before returning `"msg <x>"`, and logged messages are appended as `"LOG msg <x>"`. Return the log.""",
 solution="""
 final class Log { var lines: [String] = [] }

 func debugLog(_ message: @autoclosure () -> String, level: Int, into log: Log) {
     guard level >= 2 else { return }
     log.lines.append("LOG \\(message())")
 }

 func loggingDemo(level: Int) -> [String] {
     let log = Log()
     func expensive(_ x: String) -> String {
         log.lines.append("computed \\(x)")
         return "msg \\(x)"
     }
     debugLog(expensive("A"), level: level, into: log)
     debugLog(expensive("B"), level: 3, into: log)
     return log.lines
 }
 """,
 explain="""`@autoclosure` wraps the argument expression in a closure, so it's evaluated **only if called**. That's how `assert`, `&&` and `??` avoid evaluating their right-hand side. At level 1 the log never contains `computed A`.""",
 tests=[({'level':1},['computed B','LOG msg B']), {'level':2}, {'level':0}]))
P.append(dict(id='sort-by-keypath', title='Sort by Any Key Path', topic='Closures', notes='20', diff='medium', concepts=['key-paths','sort-custom','generics'], docs=[('Expressions — Key-Path Expression','ReferenceManual/Expressions')],
 sig='func sortPeople(_ rows: [[String]], by key: String) -> [String]',
 statement="""Add `extension Sequence { func sorted<V: Comparable>(by keyPath: KeyPath<Element, V>) -> [Element] }`. Rows are `[name, age, city]`; build `Person` structs and sort by `\\.name`, `\\.age` or `\\.city` depending on `key`. Return the names in order (ties keep input order — the standard sort is stable).""",
 solution="""
 extension Sequence {
     func sorted<V: Comparable>(by keyPath: KeyPath<Element, V>) -> [Element] {
         sorted { $0[keyPath: keyPath] < $1[keyPath: keyPath] }
     }
 }

 struct Person {
     let name: String
     let age: Int
     let city: String
 }

 func sortPeople(_ rows: [[String]], by key: String) -> [String] {
     let people = rows.map { Person(name: $0[0], age: Int($0[1])!, city: $0[2]) }
     let sorted: [Person] = switch key {
     case "age": people.sorted(by: \\.age)
     case "city": people.sorted(by: \\.city)
     default: people.sorted(by: \\.name)
     }
     return sorted.map(\\.name)
 }
 """,
 explain="""`\\Person.age` is a `KeyPath<Person, Int>`; `value[keyPath: kp]` reads through it. Generic over `V: Comparable`, one method sorts by any property. Swift's `sort` is guaranteed stable since Swift 5.""",
 tests=[({'rows':[['cy','30','Rome'],['ana','25','Oslo'],['bo','25','Lima']],'key':'age'},['ana','bo','cy']), {'rows':[['cy','30','Rome'],['ana','25','Oslo'],['bo','25','Lima']],'key':'city'}, {'rows':[['cy','30','Rome'],['ana','25','Oslo']],'key':'name'}, {'rows':[],'key':'age'}]))
P.append(dict(id='compose-functions', title='Function Composition', topic='Closures', notes='20', diff='medium', concepts=['higher-order-functions','custom-operators','generics'], docs=[('Advanced Operators — Custom Operators','LanguageGuide/AdvancedOperators')],
 sig='func pipeline(_ values: [Int]) -> [String]',
 statement="""Declare `infix operator >>> : AdditionPrecedence` and implement it generically so `f >>> g` is a function that applies `f` then `g`.

 Build `let transform = double >>> increment >>> describe` where `double` ×2, `increment` +1 and `describe` turns an `Int` into `"#<n>"`, and map it over `values`.""",
 solution="""
 infix operator >>> : AdditionPrecedence

 func >>> <A, B, C>(f: @escaping (A) -> B, g: @escaping (B) -> C) -> (A) -> C {
     { g(f($0)) }
 }

 func double(_ x: Int) -> Int { x * 2 }
 func increment(_ x: Int) -> Int { x + 1 }
 func describe(_ x: Int) -> String { "#\\(x)" }

 func pipeline(_ values: [Int]) -> [String] {
     let transform = double >>> increment >>> describe
     return values.map(transform)
 }
 """,
 explain="""Custom operators are declared once (`infix operator`), given a precedence group, then implemented as functions. The closures escape (they're captured by the returned closure), hence `@escaping`. `AdditionPrecedence` is left-associative, so it composes left to right.""",
 tests=[({'values':[1,2,3]},['#3','#5','#7']), {'values':[]}, {'values':[-1,0]}]))
P.append(dict(id='curried-add', title='Currying & Partial Application', topic='Closures', notes='20', concepts=['currying','closures'], docs=[('Closures', CL)],
 sig='func curryDemo(_ base: Int, _ xs: [Int]) -> [Int]',
 statement="""Write `func add(_ a: Int) -> (Int) -> Int`. Using it, create `let addBase = add(base)` and return `xs.map(addBase)` followed by `add(1)(add(2)(3))`.""",
 solution="""
 func add(_ a: Int) -> (Int) -> Int {
     { b in a + b }
 }

 func curryDemo(_ base: Int, _ xs: [Int]) -> [Int] {
     let addBase = add(base)
     return xs.map(addBase) + [add(1)(add(2)(3))]
 }
 """,
 explain="""A curried function takes one argument and returns a function waiting for the next. `add(base)` is **partial application** — a reusable adder you can pass to `map`. Instance methods are curried too: `String.uppercased` has type `(String) -> () -> String`.""",
 tests=[({'base':10,'xs':[1,2]},[11,12,6]), {'base':0,'xs':[]}, {'base':-5,'xs':[5,10]}]))
P.append(dict(id='reduce-into', title='reduce(into:) to Build a Histogram', topic='Closures', notes='20', concepts=['map-filter-reduce','dictionary-basics'], docs=[('Closures', CL)],
 sig='func lengthHistogram(_ words: [String]) -> [String: [String]]',
 statement="""Group words by length (as a String key) using a single `reduce(into:)`, keeping first-seen order within each group.

 ```swift
 lengthHistogram(["hi", "yo", "hey"])   // ["2": ["hi", "yo"], "3": ["hey"]]
 ```""",
 solution="""
 func lengthHistogram(_ words: [String]) -> [String: [String]] {
     words.reduce(into: [:]) { groups, word in
         groups[String(word.count), default: []].append(word)
     }
 }
 """,
 explain="""`reduce(into:)` passes the accumulator as `inout`, so you mutate it in place instead of copying a new dictionary each step (which plain `reduce` would do — O(n²) for collections).""",
 tests=[({'words':['hi','yo','hey']},{'2':['hi','yo'],'3':['hey']}), {'words':[]}, {'words':['a','bb','c','dd','eee']}]))
P.append(dict(id='predict-closure-capture-loop', title='Predict: Closures Created in a Loop', topic='Closures', mode='predict', notes='20', concepts=['capturing-values','capture-list'], docs=[('Closures — Capturing Values', CL)],
 statement="Predict the output. Which values do the closures see when they finally run?",
 snippet="""
 var handlers: [() -> Void] = []
 for i in 1...3 {
     handlers.append { print("loop", i) }
 }
 var counter = 0
 for _ in 1...3 {
     handlers.append { print("shared", counter) }
     counter += 1
 }
 let snapshot = { [counter] in print("snapshot", counter) }
 counter = 100
 handlers.forEach { $0() }
 snapshot()
 """,
 explain="""Each `for-in` iteration gets a **fresh** `i` constant, so the first closures print 1, 2, 3. The second group all capture the **same** `counter` variable and print its value at call time (100). The capture list froze `counter` at 3 when `snapshot` was created."""))

write_all(P, 'intermediate', 100)
