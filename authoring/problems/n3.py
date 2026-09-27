import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CC='LanguageGuide/Concurrency'; GE='LanguageGuide/Generics'; OT='LanguageGuide/OpaqueTypes'; AT='ReferenceManual/Attributes'; DE='ReferenceManual/Declarations'; EXP='ReferenceManual/Expressions'
P=[]
P.append(dict(id='async-let', title='async let: Parallel Child Tasks', topic='Concurrency', diff='medium', concepts=['async-await','task-group'], docs=[('Concurrency — Calling Asynchronous Functions in Parallel', CC)], timeLimitMs=700,
 sig='func dashboard(userID: Int) async -> [String]',
 statement="""Three services each take ~300 ms (given). Load all three **in parallel** with `async let`, then return `[profile, feed, notifications]`. Sequential awaits take ~900 ms and exceed the 700 ms time limit.""",
 starter="""
 func loadProfile(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "profile \\(id)" }
 func loadFeed(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "feed \\(id)" }
 func loadNotifications(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "notifications \\(id)" }

 func dashboard(userID: Int) async -> [String] {
     let profile = await loadProfile(userID)
     let feed = await loadFeed(userID)
     let notifications = await loadNotifications(userID)
     return [profile, feed, notifications]
 }
 """,
 solution="""
 func loadProfile(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "profile \\(id)" }
 func loadFeed(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "feed \\(id)" }
 func loadNotifications(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "notifications \\(id)" }

 func dashboard(userID: Int) async -> [String] {
     async let profile = loadProfile(userID)
     async let feed = loadFeed(userID)
     async let notifications = loadNotifications(userID)
     return await [profile, feed, notifications]
 }
 """,
 explain="""`async let` starts a child task immediately; `await` collects its value later. Three bindings → three concurrent tasks, so the total is ~300 ms. They're **structured**: if the function exits early, unawaited children are cancelled automatically.""",
 hints=("Awaiting each call in turn runs them one after another.","`async let x = f()` starts `f` right away; you `await x` later.","`async let profile = loadProfile(userID)` ×3, then `return await [profile, feed, notifications]`."),
 tests=[({'userID':7},['profile 7','feed 7','notifications 7']), {'userID':0}, {'userID':42}], hidden=1))
P.append(dict(id='checked-continuation', title='Wrapping Callbacks with Continuations', topic='Concurrency', diff='medium', concepts=['async-await','escaping','error-handling'], docs=[('withCheckedThrowingContinuation', 'https://developer.apple.com/documentation/swift/withcheckedthrowingcontinuation(isolation:function:_:)')],
 sig='func fetchAll(_ keys: [String]) async -> [String]',
 statement="""A legacy API (given) reports through a completion handler: `legacyFetch(_:completion:)` calls back with `.success(value)` or `.failure(LegacyError.notFound)`. Wrap it as `func fetch(_ key: String) async throws -> String` using `withCheckedThrowingContinuation`, then fetch each key returning the value or `"missing <key>"`.""",
 starter="""
 enum LegacyError: Error { case notFound }

 func legacyFetch(_ key: String, completion: @escaping @Sendable (Result<String, Error>) -> Void) {
     Thread.detachNewThread {
         completion(key.hasPrefix("x") ? .failure(LegacyError.notFound) : .success(key.uppercased()))
     }
 }

 import Foundation

 func fetchAll(_ keys: [String]) async -> [String] {
     return []
 }
 """,
 solution="""
 enum LegacyError: Error { case notFound }

 func legacyFetch(_ key: String, completion: @escaping @Sendable (Result<String, Error>) -> Void) {
     Thread.detachNewThread {
         completion(key.hasPrefix("x") ? .failure(LegacyError.notFound) : .success(key.uppercased()))
     }
 }

 import Foundation

 func fetch(_ key: String) async throws -> String {
     try await withCheckedThrowingContinuation { continuation in
         legacyFetch(key) { result in
             continuation.resume(with: result)
         }
     }
 }

 func fetchAll(_ keys: [String]) async -> [String] {
     var out: [String] = []
     for key in keys {
         out.append((try? await fetch(key)) ?? "missing \\(key)")
     }
     return out
 }
 """,
 explain="""A continuation suspends the async function until the callback resumes it — **exactly once** (the *checked* variant traps if you resume twice or warns if you never do). `resume(with: result)` forwards a `Result` directly. This is how you modernise delegate/callback APIs.""",
 hints=("You need to suspend until a callback fires.","`withCheckedThrowingContinuation { continuation in legacyFetch(key) { … } }`.","Inside the callback: `continuation.resume(with: result)`."),
 tests=[({'keys':['a','xy','swift']},['A','missing xy','SWIFT']), {'keys':[]}, {'keys':['x']}]))
P.append(dict(id='actor-nonisolated', title='Actors & nonisolated Members', topic='Concurrency', diff='medium', concepts=['actors','sendable'], docs=[('Concurrency — Actors', CC)],
 sig='func libraryDemo(_ ops: [String]) async -> [String]',
 statement="""`actor Library` has a `let name` and a mutable `books: [String: Int]` (title → copies). Add:
 - `func checkout(_ title: String) -> Bool` (decrement if available)
 - `func add(_ title: String)`
 - `nonisolated var label: String { "Library \\(name)" }` — readable **without** `await` because it only touches a `let`

 Ops: `add <t>`, `out <t>`. Return the label first (no await), then `"ok"`/`"unavailable"` per op, then the sorted `"t=n"` inventory.""",
 solution="""
 actor Library {
     let name: String
     private var books: [String: Int] = [:]

     init(name: String) { self.name = name }

     nonisolated var label: String { "Library \\(name)" }

     func add(_ title: String) { books[title, default: 0] += 1 }

     func checkout(_ title: String) -> Bool {
         guard let n = books[title], n > 0 else { return false }
         books[title] = n - 1
         return true
     }

     func inventory() -> [String] { books.sorted { $0.key < $1.key }.map { "\\($0.key)=\\($0.value)" } }
 }

 func libraryDemo(_ ops: [String]) async -> [String] {
     let library = Library(name: "Central")
     var out = [library.label]
     for op in ops {
         let p = op.split(separator: " ", maxSplits: 1).map(String.init)
         if p[0] == "add" { await library.add(p[1]); out.append("ok") }
         else { out.append(await library.checkout(p[1]) ? "ok" : "unavailable") }
     }
     return out + (await library.inventory())
 }
 """,
 explain="""Everything inside an actor is isolated: callers must `await`. A `nonisolated` member opts out — legal only if it touches immutable (`let`, Sendable) state, so it can be called synchronously. Actor `let` properties of Sendable type are also readable without `await`.""",
 hints=("Actor methods are awaited from outside; a `nonisolated` member isn't.","`nonisolated var label` may only read the `let name`, never `books`.","`out.append(await library.checkout(title) ? \"ok\" : \"unavailable\")`."),
 tests=[({'ops':['add Dune','out Dune','out Dune','add Emma']},['Library Central','ok','ok','unavailable','ok','Dune=0','Emma=1']), {'ops':[]}]))
P.append(dict(id='global-actor', title='Custom Global Actors', topic='Concurrency', diff='hard', concepts=['actors','sendable'], docs=[('Attributes — globalActor', AT)],
 sig='func analyticsDemo(_ events: [String]) async -> [String]',
 statement="""Declare `@globalActor actor AnalyticsActor { static let shared = AnalyticsActor() }`. Mark a class `@AnalyticsActor final class Tracker` holding `var events: [String]`, and a free function `@AnalyticsActor func log(_ e: String, to t: Tracker)`. All of it is isolated to the **same** actor, so `log` can touch `t.events` synchronously.

 Log each event (skipping empty strings) and return the tracker's events plus `"count <n>"`.""",
 solution="""
 @globalActor
 actor AnalyticsActor {
     static let shared = AnalyticsActor()
 }

 @AnalyticsActor
 final class Tracker {
     var events: [String] = []
 }

 @AnalyticsActor
 func log(_ event: String, to tracker: Tracker) {
     guard !event.isEmpty else { return }
     tracker.events.append(event)
 }

 @AnalyticsActor
 func runAnalytics(_ events: [String]) -> [String] {
     let tracker = Tracker()
     for e in events { log(e, to: tracker) }
     return tracker.events + ["count \\(tracker.events.count)"]
 }

 func analyticsDemo(_ events: [String]) async -> [String] {
     await runAnalytics(events)
 }
 """,
 explain="""A global actor is a singleton actor you can apply as an attribute, isolating unrelated declarations to one serial executor — `@MainActor` is the built-in example. Code isolated to the same global actor calls each other synchronously; outsiders `await`.""",
 hints=("`@globalActor` turns an actor with a `static let shared` into an attribute.","Put `@AnalyticsActor` on the class, the logging function and a runner; call the runner with `await`.","Within `@AnalyticsActor` code, `log(e, to: tracker)` needs no `await`."),
 tests=[({'events':['open','','tap']},['open','tap','count 2']), {'events':[]}]))
P.append(dict(id='sendable-value-snapshot', title='Sendable Snapshots Across Tasks', topic='Concurrency', diff='medium', concepts=['sendable','value-vs-reference','task-group'], docs=[('Sendable', 'https://developer.apple.com/documentation/swift/sendable')],
 sig='func processOrders(_ totals: [Int]) async -> [String]',
 statement="""Model `struct OrderSnapshot: Sendable { let id: Int; let total: Int }` and process snapshots concurrently in a task group, each child returning `"#<id>: <tax>"` where tax = total × 8 / 100 (integer). Return results sorted by id.

 Try replacing the struct with a `final class` holding a `var total` — Swift 6 rejects sending it into child tasks.""",
 solution="""
 struct OrderSnapshot: Sendable {
     let id: Int
     let total: Int
 }

 func processOrders(_ totals: [Int]) async -> [String] {
     let snapshots = totals.enumerated().map { OrderSnapshot(id: $0.offset + 1, total: $0.element) }
     let results = await withTaskGroup(of: (Int, String).self) { group in
         for s in snapshots {
             group.addTask { (s.id, "#\\(s.id): \\(s.total * 8 / 100)") }
         }
         var collected: [(Int, String)] = []
         for await r in group { collected.append(r) }
         return collected
     }
     return results.sorted { $0.0 < $1.0 }.map(\\.1)
 }
 """,
 explain="""Immutable value types of `Sendable` members are automatically safe to share across concurrency domains — each task gets its own copy. That's why snapshotting mutable models into Sendable structs is the standard way to hand data to background work in Swift 6.""",
 hints=("What kind of type can be safely copied into many concurrent tasks?","A `struct` with only `let` Sendable properties is `Sendable`; spawn one child task per snapshot.","Collect `(id, text)` pairs from the group, then sort by id."),
 tests=[({'totals':[100,250,99]},['#1: 8','#2: 20','#3: 7']), {'totals':[]}]))
P.append(dict(id='predict-struct-class-actor', title='Predict: Struct vs Class vs Actor', topic='Concurrency', mode='predict', diff='medium', concepts=['value-vs-reference','actors','struct-vs-class'], docs=[('Concurrency — Actors', CC)],
 statement="""Swiftful Thinking's *Struct vs Class vs Actor* in one snippet. Predict the output (top-level `await` is allowed in `main.swift`).""",
 snippet="""
 struct S { var n = 0 }
 final class C { var n = 0 }
 actor A {
     var n = 0
     func bump() -> Int { n += 1; return n }
 }

 var s1 = S(); var s2 = s1; s2.n = 5
 let c1 = C(); let c2 = c1; c2.n = 5
 let a1 = A(); let a2 = a1
 _ = await a2.bump()
 print(s1.n, s2.n)
 print(c1.n, c2.n, c1 === c2)
 print(await a1.n, await a1.bump(), a1 === a2)
 """,
 explain="""Structs copy (value semantics); classes and actors are reference types, so `a1` and `a2` are the **same** actor. The actor differs from the class by **isolation**: every access from outside is `await`ed and serialised, which makes it safe to share across threads.""",
 hints=("Two of these three are reference types.","`a2.bump()` changes the same actor that `a1` refers to.","Last line: `1 2 true`.")))
P.append(dict(id='weak-self-task', title='Tasks, Cancellation & [weak self]', topic='Concurrency', diff='hard', concepts=['closures-memory','weak-unowned','async-await'], docs=[('Concurrency — Task Cancellation', CC)],
 sig='func screenLifecycle(cancelOnDisappear: Bool) async -> [String]',
 statement="""Swiftful's *strong & weak references with Async Await*. `@MainActor final class ImageLoader` starts `task = Task { [weak self] in … }` in `onAppear()`, which sleeps 50 ms then (if still alive and not cancelled) sets `self.image = "loaded"`. `onDisappear()` cancels the task if `cancelOnDisappear`. `deinit` logs `"deinit"`.

 The demo creates the loader, calls `onAppear()`, then `onDisappear()`, drops the loader, waits 150 ms, and returns the log. Every write goes through a shared `Log` actor.""",
 solution="""
 actor Log {
     private(set) var lines: [String] = []
     func add(_ s: String) { lines.append(s) }
 }

 @MainActor
 final class ImageLoader {
     private var task: Task<Void, Never>?
     private let log: Log
     var image: String?

     init(log: Log) { self.log = log }

     func onAppear() {
         task = Task { [weak self, log] in
             try? await Task.sleep(for: .milliseconds(50))
             guard !Task.isCancelled else { await log.add("cancelled"); return }
             guard let self else { return }
             self.image = "loaded"
             await self.log.add("loaded")
         }
     }

     func onDisappear(cancel: Bool) {
         if cancel { task?.cancel() }
     }

     isolated deinit {
         let log = self.log
         Task { await log.add("deinit") }
     }
 }

 func screenLifecycle(cancelOnDisappear: Bool) async -> [String] {
     let log = Log()
     await MainActor.run {
         var loader: ImageLoader? = ImageLoader(log: log)
         loader?.onAppear()
         loader?.onDisappear(cancel: cancelOnDisappear)
         loader = nil
     }
     try? await Task.sleep(for: .milliseconds(150))
     return await log.lines.sorted()
 }
 """,
 explain="""A `Task` closure strongly retains what it captures until it finishes. `[weak self]` lets the owner deallocate early, and cancelling the task on disappear stops wasted work. Cancellation is cooperative: `Task.sleep` throws on cancellation, and the task must check `Task.isCancelled` itself. The log is sorted because the order of `deinit` vs task completion depends on scheduling. Two subtleties: the logger is captured **separately** (`[weak self, log]`) because once `self` is gone, `self?.log` is `nil` too. And without cancellation the task still runs to completion — but `guard let self` finds the loader already deallocated, so nothing is \"loaded\": weak capture prevents the leak, cancellation prevents the wasted work.""",
 hints=("A `Task { }` captures `self` strongly unless you say otherwise.","Capture `[weak self, log]` (the logger separately!), check `Task.isCancelled` after the sleep, and `guard let self` before touching state.","Cancel in `onDisappear` with `task?.cancel()`."),
 tests=[({'cancelOnDisappear':True},['cancelled','deinit']), {'cancelOnDisappear':False}], hidden=0))
P.append(dict(id='mvvm-async-viewmodel', title='MVVM with async/await', topic='Architecture', diff='medium', concepts=['dependency-injection','async-await','actors'], docs=[('MainActor', 'https://developer.apple.com/documentation/swift/mainactor')],
 sig='func loadScreen(_ behaviours: [String]) async -> [String]',
 statement="""Swiftful's *MVVM with Async Await*. Define `protocol DataService: Sendable { func fetchTitles() async throws -> [String] }` and a `@MainActor final class TitlesViewModel` with `enum State { case idle, loading, loaded([String]), failed(String) }` and `func load() async`.

 For each behaviour (`ok`, `empty`, `fail`) build a mock service, run `load()`, and record every state the view model passes through, formatted `idle → loading → loaded(3)` / `failed(offline)` / `loaded(0)`.""",
 solution="""
 enum ServiceError: Error { case offline }

 protocol DataService: Sendable {
     func fetchTitles() async throws -> [String]
 }

 struct MockService: DataService {
     let behaviour: String
     func fetchTitles() async throws -> [String] {
         switch behaviour {
         case "fail": throw ServiceError.offline
         case "empty": return []
         default: return ["One", "Two", "Three"]
         }
     }
 }

 @MainActor
 final class TitlesViewModel {
     enum State {
         case idle, loading, loaded([String]), failed(String)
         var label: String {
             switch self {
             case .idle: "idle"
             case .loading: "loading"
             case .loaded(let t): "loaded(\\(t.count))"
             case .failed(let e): "failed(\\(e))"
             }
         }
     }

     private(set) var history: [String] = []
     private(set) var state: State = .idle { didSet { history.append(state.label) } }
     private let service: any DataService

     init(service: any DataService) {
         self.service = service
         history = [state.label]
     }

     func load() async {
         state = .loading
         do {
             state = .loaded(try await service.fetchTitles())
         } catch {
             state = .failed("\\(error)")
         }
     }
 }

 func loadScreen(_ behaviours: [String]) async -> [String] {
     var out: [String] = []
     for b in behaviours {
         let vm = await TitlesViewModel(service: MockService(behaviour: b))
         await vm.load()
         out.append(await vm.history.joined(separator: " → "))
     }
     return out
 }
 """,
 explain="""The view model owns UI state on the `@MainActor`, depends on a **protocol** (so tests inject a mock), and models loading as an enum — impossible states like "loading and failed" can't exist. The service call hops off the main actor while it waits.""",
 hints=("Model the screen's states as an enum and inject the service through a protocol.","Set `.loading`, then `.loaded(try await service.fetchTitles())` or `.failed` in the `catch`.","Record each state in `didSet` on the state property."),
 tests=[({'behaviours':['ok','fail','empty']},['idle → loading → loaded(3)','idle → loading → failed(offline)','idle → loading → loaded(0)']), {'behaviours':[]}], hidden=0))
P.append(dict(id='async-throwing-stream', title='AsyncThrowingStream: Progress Updates', topic='Concurrency', diff='medium', concepts=['async-await','error-handling'], docs=[('AsyncThrowingStream', 'https://developer.apple.com/documentation/swift/asyncthrowingstream')],
 sig='func downloadProgress(chunks: Int, failAt: Int) async -> [String]',
 statement="""Write `func download(chunks: Int, failAt: Int) -> AsyncThrowingStream<Int, Error>` that yields percentage progress (`100 * i / chunks` for i in 1…chunks) and **throws** `DownloadError.interrupted` when `i == failAt` (use 0 for "never fails"). Consume it with `for try await`, recording each value, then `"done"` or `"error interrupted"`.""",
 solution="""
 enum DownloadError: Error { case interrupted }

 func download(chunks: Int, failAt: Int) -> AsyncThrowingStream<Int, Error> {
     AsyncThrowingStream { continuation in
         for i in stride(from: 1, through: chunks, by: 1) {
             if i == failAt {
                 continuation.finish(throwing: DownloadError.interrupted)
                 return
             }
             continuation.yield(100 * i / chunks)
         }
         continuation.finish()
     }
 }

 func downloadProgress(chunks: Int, failAt: Int) async -> [String] {
     var log: [String] = []
     do {
         for try await percent in download(chunks: chunks, failAt: failAt) {
             log.append("\\(percent)%")
         }
         log.append("done")
     } catch {
         log.append("error \\(error)")
     }
     return log
 }
 """,
 explain="""`AsyncThrowingStream` bridges push-based producers into `for try await`. `finish(throwing:)` ends the stream with an error that surfaces at the loop; `finish()` ends it normally.""",
 hints=("A stream's continuation can `yield` values, `finish()`, or `finish(throwing:)`.","Loop over the chunks, yielding percentages; on the failing chunk, finish with the error and return.","Consume with `for try await percent in download(…)` inside `do`/`catch`."),
 tests=[({'chunks':4,'failAt':0},['25%','50%','75%','100%','done']), ({'chunks':4,'failAt':3},['25%','50%','error interrupted']), {'chunks':0,'failAt':0}, {'chunks':3,'failAt':1}]))
P.append(dict(id='task-timeout', title='Timeouts with a Throwing Task Group', topic='Concurrency', diff='hard', concepts=['task-group','async-await','error-handling'], docs=[('withThrowingTaskGroup', 'https://developer.apple.com/documentation/swift/withthrowingtaskgroup(of:returning:isolation:body:)')], timeLimitMs=3000,
 sig='func withDeadlines(_ jobs: [[Int]]) async -> [String]',
 statement="""Implement `func withTimeout<T: Sendable>(ms: Int, _ work: @escaping @Sendable () async throws -> T) async throws -> T`: race `work` against a sleeping task in a throwing task group; whichever finishes first wins and the other is cancelled. Throw `TimeoutError()` if the timer wins.

 Each job is `[workMs, timeoutMs]` where the work sleeps `workMs` then returns `"done in <workMs>"`. Return the result or `"timed out"` per job.""",
 solution="""
 struct TimeoutError: Error {}

 func withTimeout<T: Sendable>(ms: Int, _ work: @escaping @Sendable () async throws -> T) async throws -> T {
     try await withThrowingTaskGroup(of: T.self) { group in
         group.addTask { try await work() }
         group.addTask {
             try await Task.sleep(for: .milliseconds(ms))
             throw TimeoutError()
         }
         defer { group.cancelAll() }
         return try await group.next()!
     }
 }

 func withDeadlines(_ jobs: [[Int]]) async -> [String] {
     var out: [String] = []
     for job in jobs {
         let workMs = job[0]
         do {
             out.append(try await withTimeout(ms: job[1]) {
                 try await Task.sleep(for: .milliseconds(workMs))
                 return "done in \\(workMs)"
             })
         } catch {
             out.append("timed out")
         }
     }
     return out
 }
 """,
 explain="""`group.next()` returns the **first** child to finish (or rethrows its error); cancelling the group then stops the loser. This is the idiomatic structured-concurrency timeout — no timers, no leaked work.""",
 hints=("Race two child tasks in one group: the real work and a sleep that throws.","`try await group.next()!` gives whichever finishes first; then cancel the rest.","`defer { group.cancelAll() }` before `return try await group.next()!`."),
 tests=[({'jobs':[[10,200],[300,50]]},['done in 10','timed out']), {'jobs':[]}, {'jobs':[[0,100]]}], hidden=0))
P.append(dict(id='task-local', title='@TaskLocal: Request IDs', topic='Concurrency', diff='hard', concepts=['async-await','task-group'], docs=[('TaskLocal', 'https://developer.apple.com/documentation/swift/tasklocal')],
 sig='func tracedRequests(_ ids: [String]) async -> [String]',
 statement="""Declare `enum Trace { @TaskLocal static var requestID = "none" }`. For each id, run `Trace.$requestID.withValue(id) { … }` and inside it spawn **two child tasks** (a task group) that each log `"<requestID>:<step>"` for steps `db` and `cache` — child tasks inherit the task-local value. Also log once outside any `withValue`. Return logs sorted.""",
 solution="""
 enum Trace {
     @TaskLocal static var requestID = "none"
 }

 func handle() async -> [String] {
     await withTaskGroup(of: String.self) { group in
         for step in ["db", "cache"] {
             group.addTask { "\\(Trace.requestID):\\(step)" }
         }
         var lines: [String] = []
         for await line in group { lines.append(line) }
         return lines
     }
 }

 func tracedRequests(_ ids: [String]) async -> [String] {
     var logs = ["\\(Trace.requestID):outside"]
     for id in ids {
         logs += await Trace.$requestID.withValue(id) { await handle() }
     }
     return logs.sorted()
 }
 """,
 explain="""Task-local values flow down the task tree (to child tasks and `async let`) without threading a parameter through every call — perfect for request IDs and tracing. Outside `withValue` you see the default.""",
 hints=("A task-local value is bound for a scope and inherited by child tasks.","Wrap the work in `Trace.$requestID.withValue(id) { … }` and read `Trace.requestID` inside the children.","Children: `group.addTask { \"\\(Trace.requestID):\\(step)\" }`."),
 tests=[({'ids':['r1','r2']},['none:outside','r1:cache','r1:db','r2:cache','r2:db']), {'ids':[]}]))
P.append(dict(id='actor-request-coalescing', title='Actor Reentrancy: Coalesce Duplicate Requests', topic='Concurrency', diff='hard', concepts=['actors','async-await','caching'], docs=[('Concurrency — Actors', CC)],
 sig='func coalesced(_ keys: [String]) async -> [String]',
 statement="""A senior-level classic. An `actor ImageCache` must not download the same key twice, even when many callers ask **concurrently**. Because actors are **reentrant**, checking a cache dictionary before `await download()` isn't enough — two callers can both miss.

 Store in-flight work as `[String: Task<String, Never>]`: if a task exists, `await task.value`; otherwise create one. The fake `download` sleeps 30 ms and increments a download counter. Request all keys **concurrently** (task group) and return `[sorted distinct results…, "downloads <n>"]`.""",
 solution="""
 actor ImageCache {
     private var tasks: [String: Task<String, Never>] = [:]
     private(set) var downloads = 0

     func image(for key: String) async -> String {
         if let existing = tasks[key] { return await existing.value }
         let task = Task { await self.download(key) }
         tasks[key] = task
         return await task.value
     }

     private func download(_ key: String) async -> String {
         downloads += 1
         try? await Task.sleep(for: .milliseconds(30))
         return "img:\\(key)"
     }
 }

 func coalesced(_ keys: [String]) async -> [String] {
     let cache = ImageCache()
     let results = await withTaskGroup(of: String.self) { group in
         for key in keys { group.addTask { await cache.image(for: key) } }
         var all: Set<String> = []
         for await r in group { all.insert(r) }
         return all
     }
     return results.sorted() + ["downloads \\(await cache.downloads)"]
 }
 """,
 explain="""Between an actor's `await` points other calls can run (reentrancy), so state checked before an `await` may be stale after it. Registering the in-flight `Task` **synchronously** (before any `await`) closes the gap: later callers find it and await the same result. Downloads = number of distinct keys.""",
 hints=("Two concurrent callers can both see an empty cache if you `await` before recording anything.","Store the in-flight `Task` in a dictionary *before* awaiting it; later callers await the same task.","`if let existing = tasks[key] { return await existing.value }` then create, store and await a new `Task`."),
 tests=[({'keys':['a','b','a','a','c','b']},['img:a','img:b','img:c','downloads 3']), {'keys':[]}, {'keys':['x','x','x','x']}]))
P.append(dict(id='check-cancellation', title='Cooperative Cancellation with checkCancellation', topic='Concurrency', diff='medium', concepts=['async-await','error-handling'], docs=[('Task', 'https://developer.apple.com/documentation/swift/task')],
 sig='func batch(items: Int, cancelEarly: Bool) async -> [String]',
 statement="""Process `items` units of work in a `Task`, calling `try Task.checkCancellation()` before each unit and `await Task.yield()` after it. If `cancelEarly`, cancel the task **immediately** after creating it. Return `"processed <n>"` or `"cancelled after <n>"` using the task's result (`try await task.value`).""",
 solution="""
 final class Counter: @unchecked Sendable {
     var value = 0
 }

 func batch(items: Int, cancelEarly: Bool) async -> [String] {
     let counter = Counter()
     let task = Task {
         for _ in 0..<items {
             try Task.checkCancellation()
             counter.value += 1
             await Task.yield()
         }
         return counter.value
     }
     if cancelEarly { task.cancel() }
     do {
         return ["processed \\(try await task.value)"]
     } catch is CancellationError {
         return ["cancelled after \\(counter.value == 0 ? 0 : counter.value)"]
     } catch {
         return ["error"]
     }
 }
 """,
 explain="""`task.cancel()` only sets a flag; `Task.checkCancellation()` throws `CancellationError` when it's set, which ends the work at a safe point. Cancelling before the task starts means the very first check throws. (With `items == 0` there's no check, so the task completes normally.)""",
 hints=("Cancellation is a flag the task must check.","Call `try Task.checkCancellation()` at the top of each loop iteration.","`catch is CancellationError` distinguishes cancellation from other errors."),
 tests=[({'items':5,'cancelEarly':False},['processed 5']), ({'items':5,'cancelEarly':True},['cancelled after 0']), {'items':0,'cancelEarly':True}]))
P.append(dict(id='custom-async-sequence', title='Custom AsyncSequence: Countdown', topic='Concurrency', diff='hard', concepts=['async-await','custom-collection'], docs=[('AsyncSequence', 'https://developer.apple.com/documentation/swift/asyncsequence')],
 sig='func countdown(from start: Int, keepEvensOnly: Bool) async -> [Int]',
 statement="""Implement `struct Countdown: AsyncSequence` (with a nested `AsyncIterator` whose `mutating func next() async -> Int?` counts down to 0 and yields with `await Task.yield()` between values). Consume it, optionally using the async `filter` operator for even numbers, and return the values.""",
 solution="""
 struct Countdown: AsyncSequence {
     typealias Element = Int
     let start: Int

     struct AsyncIterator: AsyncIteratorProtocol {
         var current: Int
         mutating func next() async -> Int? {
             guard current >= 0 else { return nil }
             await Task.yield()
             defer { current -= 1 }
             return current
         }
     }

     func makeAsyncIterator() -> AsyncIterator { AsyncIterator(current: start) }
 }

 func countdown(from start: Int, keepEvensOnly: Bool) async -> [Int] {
     var out: [Int] = []
     if keepEvensOnly {
         for await n in Countdown(start: start).filter({ $0.isMultiple(of: 2) }) { out.append(n) }
     } else {
         for await n in Countdown(start: start) { out.append(n) }
     }
     return out
 }
 """,
 explain="""`AsyncSequence` mirrors `Sequence`: provide `makeAsyncIterator()`, whose `next()` is `async`. You get `map`, `filter`, `prefix`, `contains`… as async operators for free.""",
 hints=("It's `Sequence`, but `next()` is `async`.","The iterator holds `current`, returns it, and decrements until below 0.","Conform with `typealias Element = Int` and `func makeAsyncIterator() -> AsyncIterator`."),
 tests=[({'start':3,'keepEvensOnly':False},[3,2,1,0]), ({'start':5,'keepEvensOnly':True},[4,2,0]), {'start':-1,'keepEvensOnly':False}, {'start':0,'keepEvensOnly':True}]))
P.append(dict(id='duration-components', title='Duration & Clocks', topic='Concurrency', concepts=['async-await','fundamental-types'], docs=[('Duration', 'https://developer.apple.com/documentation/swift/duration')],
 sig='func formatDurations(_ millis: [Int]) -> [String]',
 statement="""Swift's `Duration` (used by `Task.sleep(for:)` and clocks) stores seconds + attoseconds. For each millisecond value build `Duration.milliseconds(n)`, add `.seconds(1)`, and format as `"<m>m <s>s <ms>ms"` using `components.seconds` / `components.attoseconds` (1 ms = 10¹⁵ attoseconds).""",
 solution="""
 func formatDurations(_ millis: [Int]) -> [String] {
     millis.map { ms in
         let d = Duration.milliseconds(ms) + .seconds(1)
         let (seconds, attoseconds) = d.components
         let totalMs = seconds * 1000 + attoseconds / 1_000_000_000_000_000
         return "\\(totalMs / 60_000)m \\(totalMs % 60_000 / 1000)s \\(totalMs % 1000)ms"
     }
 }
 """,
 explain="""`Duration` is a precise, overflow-resistant time span; arithmetic like `+` works directly. Clocks (`ContinuousClock`, `SuspendingClock`) measure elapsed `Duration`s via `clock.measure { … }`.""",
 hints=("`Duration` supports `+`; `.components` gives `(seconds, attoseconds)`.","Convert everything to milliseconds: seconds × 1000 + attoseconds ÷ 10¹⁵.","Then split into minutes, seconds and milliseconds with `/` and `%`."),
 tests=[({'millis':[0,61500]},['0m 1s 0ms','1m 2s 500ms']), {'millis':[]}, {'millis':[999,3600000]}]))
P.append(dict(id='parameter-packs', title='Parameter Packs (Variadic Generics)', topic='Swift evolution', diff='hard', concepts=['generics','variadic','tuples'], docs=[('Generics — Parameter Packs', GE)],
 sig='func packsDemo() -> [String]',
 statement="""Swift 5.9 added **parameter packs**: generics over a variable number of types. Write:
 - `func describeAll<each T>(_ value: repeat each T) -> [String]` returning `String(describing:)` for every argument
 - `func allNonNil<each T>(_ value: repeat (each T)?) -> Bool`

 Return `describeAll(1, "two", 3.0, true)` + `["\\(allNonNil(1, "a", 2.5))", "\\(allNonNil(1, nil as String?))"]`.""",
 solution="""
 func describeAll<each T>(_ value: repeat each T) -> [String] {
     var out: [String] = []
     for v in repeat each value {
         out.append(String(describing: v))
     }
     return out
 }

 func allNonNil<each T>(_ value: repeat (each T)?) -> Bool {
     for v in repeat each value {
         if v == nil { return false }
     }
     return true
 }

 func packsDemo() -> [String] {
     describeAll(1, "two", 3.0, true) + ["\\(allNonNil(1, "a", 2.5))", "\\(allNonNil(1, nil as String?))"]
 }
 """,
 explain="""`each T` declares a pack of types; `repeat each value` expands it. Swift 6 lets you iterate a pack with `for v in repeat each value`. This is how SwiftUI's `ViewBuilder` and `zip`-like APIs escape the old "overload for 1…10 arguments" pattern.""",
 hints=("A type parameter pack is written `each T`; a value pack parameter is `repeat each T`.","Iterate the pack with `for v in repeat each value { … }` (Swift 6).","For optionals: parameter `repeat (each T)?`, and return false on the first `nil`."),
 tests=[({},['1','two','3.0','true','true','false'])], hidden=0))
P.append(dict(id='noncopyable-generics', title='Noncopyable Generics', topic='Swift evolution', diff='hard', concepts=['ownership','generics','memory-safety'], docs=[('Swift Evolution SE-0427', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0427-noncopyable-generics.md')],
 sig='func vaultDemo(_ secrets: [String]) -> [String]',
 statement="""Swift 6 lets generics accept **noncopyable** types via `~Copyable`. Write `struct Ticket: ~Copyable { let id: String }` and a generic `struct Vault<Item: ~Copyable>: ~Copyable` that holds an optional item with `mutating func store(_ item: consuming Item)` and `mutating func take() -> Item?`.

 For each secret, store a ticket, take it back (logging `"took <id>"`), and try taking again (logging `"empty"`).""",
 solution="""
 struct Ticket: ~Copyable {
     let id: String
 }

 struct Vault<Item: ~Copyable>: ~Copyable {
     private var item: Item?

     init() { item = nil }

     mutating func store(_ newItem: consuming Item) {
         item = consume newItem
     }

     mutating func take() -> Item? {
         item.take()
     }
 }

 func vaultDemo(_ secrets: [String]) -> [String] {
     var log: [String] = []
     for s in secrets {
         var vault = Vault<Ticket>()
         vault.store(Ticket(id: s))
         if let t = vault.take() { log.append("took \\(t.id)") }
         log.append(vault.take() == nil ? "empty" : "still full")
     }
     return log
 }
 """,
 explain="""`<Item: ~Copyable>` means "Item might not be copyable", so the generic code may only move or borrow items. `Optional.take()` moves the value out and leaves `nil` — the only way to extract a noncopyable value from storage.""",
 hints=("`~Copyable` in a generic constraint removes the implicit `Copyable` requirement.","A vault containing a noncopyable item must itself be `~Copyable`; store with a `consuming` parameter.","Extract with `item.take()`, which moves the value out and leaves `nil`."),
 tests=[({'secrets':['a','b']},['took a','empty','took b','empty']), {'secrets':[]}]))
P.append(dict(id='diag-consume-operator', title='Diagnostic: The consume Operator', topic='Swift evolution', mode='diagnostic', diff='medium', concepts=['ownership'], docs=[('Swift Evolution SE-0366', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0366-move-function.md')],
 statement="""`consume x` ends a variable's lifetime early (even for copyable types), so using it afterwards is an error. Inside a function, write `let data = [1, 2, 3]`, then `let moved = consume data`, then `print(data.count)`. You pass when the compiler reports the use after consume.""",
 starter="func demo() {\n    let data = [1, 2, 3]\n    let moved = consume data\n    print(moved.count)\n}\ndemo()\n",
 solution="func demo() {\n    let data = [1, 2, 3]\n    let moved = consume data\n    print(data.count)\n    print(moved.count)\n}\ndemo()\n",
 explain="""`consume` gives you explicit control over lifetimes — useful to avoid an accidental copy of a large buffer, or to prove a value is no longer used. The compiler enforces it: *'data' used after consume*.""",
 hints=("`consume` ends a binding's lifetime at that point.","After `let moved = consume data`, any use of `data` is an error.","Add `print(data.count)` after the consume."),
 tests=[{'name':'Use after consume','pattern':'used after consume|consumed'}]))
P.append(dict(id='primary-associated-types', title='Primary Associated Types: some Collection<Int>', topic='Opaque & existential types', diff='medium', concepts=['opaque-types','associated-types','existential-any'], docs=[('Opaque and Boxed Protocol Types', OT)],
 sig='func primaryDemo(_ values: [Int]) -> [Int]',
 statement="""Since Swift 5.7, protocols like `Collection` declare a **primary associated type**, so you can write `some Collection<Int>` and `any Sequence<Int>`.
 - `func evens(in values: some Collection<Int>) -> [Int]`
 - `func squares(_ values: [Int]) -> some Sequence<Int>` — return a **lazy** map (the caller only knows it's a sequence of Int)
 - `let sources: [any Sequence<Int>] = [values, values.reversed(), squares(values)]`

 Return `evens(in: values) + Array(squares(values)) + sources.map { $0.reduce(0, +) }`.""",
 solution="""
 func evens(in values: some Collection<Int>) -> [Int] {
     values.filter { $0.isMultiple(of: 2) }
 }

 func squares(_ values: [Int]) -> some Sequence<Int> {
     values.lazy.map { $0 * $0 }
 }

 func primaryDemo(_ values: [Int]) -> [Int] {
     let sources: [any Sequence<Int>] = [values, values.reversed(), squares(values)]
     return evens(in: values) + Array(squares(values)) + sources.map { $0.reduce(0, +) }
 }
 """,
 explain="""`some Sequence<Int>` hides the concrete type (`LazyMapSequence<[Int], Int>`) while still promising the element type — no type erasure needed. `any Sequence<Int>` lets different concrete sequences share one array.""",
 hints=("`Collection<Int>` constrains the element type without naming a concrete collection.","Return `values.lazy.map { $0 * $0 }` as `some Sequence<Int>`.","`[any Sequence<Int>]` can hold an array, a reversed view and your lazy sequence together."),
 tests=[({'values':[1,2,3,4]},[2,4,1,4,9,16,10,10,30]), {'values':[]}, {'values':[-2,5]}]))
P.append(dict(id='call-as-function', title='callAsFunction & @dynamicCallable', topic='Advanced features', diff='medium', concepts=['dynamic-member-lookup','closures'], docs=[('Declarations — Methods with Special Names', DE)],
 sig='func callablesDemo(_ values: [Int]) -> [String]',
 statement="""Make values callable like functions:
 - `struct Polynomial { let coefficients: [Int]; func callAsFunction(_ x: Int) -> Int }` — `p(2)` evaluates it (Horner's method, coefficients from highest power)
 - `@dynamicCallable struct Joiner { let separator: String; func dynamicallyCall(withArguments args: [String]) -> String }` — `j("a", "b")`

 For `p = Polynomial(coefficients: [2, 0, 1])` (2x² + 1) return `p(v)` for each value, then `Joiner(separator: "-")("x", "y", "z")`.""",
 solution="""
 struct Polynomial {
     let coefficients: [Int]
     func callAsFunction(_ x: Int) -> Int {
         coefficients.reduce(0) { $0 * x + $1 }
     }
 }

 @dynamicCallable
 struct Joiner {
     let separator: String
     func dynamicallyCall(withArguments args: [String]) -> String {
         args.joined(separator: separator)
     }
 }

 func callablesDemo(_ values: [Int]) -> [String] {
     let p = Polynomial(coefficients: [2, 0, 1])
     let join = Joiner(separator: "-")
     return values.map { String(p($0)) } + [join("x", "y", "z")]
 }
 """,
 explain="""`callAsFunction` makes an instance callable with normal, type-checked parameters (used by SwiftUI's `DismissAction` and ML libraries). `@dynamicCallable` accepts any number of arguments of one type — mainly for interop with dynamic languages.""",
 hints=("A method named `callAsFunction` makes `value(...)` legal.","Horner's method: `coefficients.reduce(0) { $0 * x + $1 }`.","`@dynamicCallable` requires `dynamicallyCall(withArguments:)`."),
 tests=[({'values':[0,1,2,-3]},['1','3','9','19','x-y-z']), {'values':[]}]))
P.append(dict(id='predict-count-where', title='Predict: Newer Standard Library APIs', topic='Swift evolution', mode='predict', concepts=['higher-order-functions','compactmap-flatmap'], docs=[('Sequence', 'https://developer.apple.com/documentation/swift/sequence')],
 statement="Predict the output of these Swift 5.x–6 additions.",
 snippet="""
 import Foundation

 let words = ["apple", "Banana", "cherry", "date", "Elder"]
 print(words.count(where: { $0.first?.isUppercase == true }))
 print(words.firstIndex(where: { $0.count > 5 }) ?? -1)
 print(words.min(by: { $0.count < $1.count }) ?? "-")
 print(words.split(whereSeparator: { $0 == "cherry" }).map(\\.count))
 print(words.allSatisfy { $0.count >= 4 }, words.contains { $0.hasSuffix("y") })
 print(Array(words.prefix(while: { $0.first?.isLowercase == true })))
 print(words.sorted(using: KeyPathComparator(\\.count)).first!)
 """,
 explain="""`count(where:)` (Swift 6) replaces `filter(…).count` without allocating. `split(whereSeparator:)` on arrays returns `[ArraySlice]`. `sorted(using: KeyPathComparator)` (Foundation) sorts by a key path and is stable.""",
 hints=("`count(where:)` counts matches without building an array.","`split` around `\"cherry\"` gives two slices; `prefix(while:)` stops at \"Banana\".","The shortest word (first on ties) is `\"date\"`.")))
P.append(dict(id='diag-existential-equatable', title="Diagnostic: == on 'any Equatable'", topic='Opaque & existential types', mode='diagnostic', diff='medium', concepts=['existential-any','equatable-hashable','generics'], docs=[('Opaque and Boxed Protocol Types', OT)],
 statement="""`Equatable` has a `Self` requirement: `==` compares two values of the **same** type. With existentials the compiler can't know both boxes hold the same type. Write `let a: any Equatable = 1`, `let b: any Equatable = 2` and `print(a == b)`. You pass when it's rejected.""",
 starter="func same<T: Equatable>(_ a: T, _ b: T) -> Bool { a == b }\nprint(same(1, 2))\n",
 solution="let a: any Equatable = 1\nlet b: any Equatable = 2\nprint(a == b)\n",
 explain="""`any Equatable` erases the concrete type, so `==` (which needs `Self == Self`) can't be called on two of them. Generics (`<T: Equatable>`) keep the type known, which is why they're preferred for such APIs.""",
 hints=("`==` requires both sides to be the *same* concrete type.","Box two values as `any Equatable` and compare them.","`print(a == b)` with both declared `any Equatable`."),
 tests=[{'name':'Existential == rejected','pattern':"cannot be applied|any Equatable"}]))
P.append(dict(id='diag-actor-isolation', title='Diagnostic: Reading Actor State Synchronously', topic='Concurrency', mode='diagnostic', diff='medium', concepts=['actors'], docs=[('Concurrency — Actors', CC)],
 statement="""Declare `actor Counter { var value = 0 }` and, in a **non-async** function, read `Counter().value` directly. You pass when the compiler reports actor isolation.""",
 starter="actor Counter { var value = 0 }\n\nfunc read(_ c: Counter) async -> Int {\n    await c.value\n}\n",
 solution="actor Counter { var value = 0 }\n\nfunc read(_ c: Counter) -> Int {\n    c.value\n}\n",
 explain="""*actor-isolated property 'value' can not be referenced from a nonisolated context*. Outside the actor, access requires `await` (and therefore an async context) so the actor can serialise it.""",
 hints=("Actor state can only be touched from inside the actor, or with `await`.","Write a synchronous function that returns `c.value`.","`func read(_ c: Counter) -> Int { c.value }`."),
 tests=[{'name':'Isolation enforced','pattern':'actor-isolated'}]))
P.append(dict(id='diag-captured-var-mutation', title='Diagnostic: Mutating a Captured var Concurrently', topic='Concurrency', mode='diagnostic', diff='medium', concepts=['sendable','capturing-values'], docs=[('Sendable', 'https://developer.apple.com/documentation/swift/sendable')],
 statement="""In an `async` function declare `var count = 0`, then start `Task { count += 1 }` while also doing `count += 1` in the function. You pass when Swift 6 rejects the concurrent mutation of the captured variable.""",
 starter="func work() async {\n    var count = 0\n    count += 1\n    print(count)\n}\n",
 solution="func work() async {\n    var count = 0\n    Task { count += 1 }\n    count += 1\n    print(count)\n}\n",
 explain="""Closures capture variables **by reference**; a `Task` closure runs concurrently, so both sides could mutate `count` at once — a data race. Swift 6 rejects it at compile time. Use an actor, or capture an immutable copy (`[count]`).""",
 hints=("Task closures run concurrently with the code that created them.","Mutate the same captured `var` inside a `Task` and outside it.","`Task { count += 1 }` followed by `count += 1`."),
 tests=[{'name':'Race rejected','pattern':'concurrently-executing|data race|sending|Sendable|captured'}]))
P.append(dict(id='opening-existentials', title='Implicitly Opened Existentials', topic='Opaque & existential types', diff='hard', concepts=['existential-any','opaque-vs-generics','generics'], docs=[('Swift Evolution SE-0352', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0352-implicit-open-existentials.md')],
 sig='func describeShapes(_ sides: [Int]) -> [String]',
 statement="""`protocol Shape { associatedtype Measure: Numeric & CustomStringConvertible; var perimeter: Measure { get } }`. `Square` uses `Int`, `Circle` uses `Double`. Store shapes as `[any Shape]` and pass each to a **generic** `func report(_ s: some Shape) -> String` (`"<type>: <perimeter>"`) — Swift 5.7+ opens the existential automatically.

 Side `n > 0` → `Square(side: n)`, `n <= 0` → `Circle(radius: Double(-n))` with perimeter `2 × 3 × r` (use 3 for π to keep it exact).""",
 solution="""
 protocol Shape {
     associatedtype Measure: Numeric & CustomStringConvertible
     var perimeter: Measure { get }
 }

 struct Square: Shape {
     let side: Int
     var perimeter: Int { 4 * side }
 }

 struct Circle: Shape {
     let radius: Double
     var perimeter: Double { 2 * 3 * radius }
 }

 func report(_ s: some Shape) -> String {
     "\\(type(of: s)): \\(s.perimeter)"
 }

 func describeShapes(_ sides: [Int]) -> [String] {
     let shapes: [any Shape] = sides.map { $0 > 0 ? Square(side: $0) as any Shape : Circle(radius: Double(-$0)) }
     return shapes.map { report($0) }
 }
 """,
 explain="""(Note `as any Shape` in the ternary: both branches must have one type, and Swift won't pick the existential for you.) Passing an `any Shape` to a `some Shape` parameter "opens" the box: inside `report`, the concrete type and its `Measure` are known again. Before SE-0352 you needed type-erasing wrappers for this.""",
 hints=("A protocol with an associated type can still be stored as `any Shape`.","Pass each `any Shape` to a function taking `some Shape` — Swift opens it for you.","`report` can use `type(of: s)` and `s.perimeter`."),
 tests=[({'sides':[3,-2]},['Square: 12','Circle: 12.0']), {'sides':[]}, {'sides':[1,0]}]))
P.append(dict(id='keypath-member-lookup', title='Type-Safe @dynamicMemberLookup with Key Paths', topic='Advanced features', diff='hard', concepts=['dynamic-member-lookup','key-paths','generics'], docs=[('Attributes — dynamicMemberLookup', AT)],
 sig='func auditDemo(_ edits: [String]) -> [String]',
 statement="""Build `@dynamicMemberLookup struct Audited<Value>` that wraps a value and records reads/writes. Implement `subscript<T>(dynamicMember keyPath: WritableKeyPath<Value, T>) -> T { get set }` that appends `"get <name>"`/`"set <name>"` to a log — use `"\\(keyPath)"`? No — take names from a provided `[PartialKeyPath<Value>: String]`.

 Wrap `struct Settings { var volume = 5; var theme = "light" }`; apply edits `volume=<n>` / `theme=<t>` through `audited.volume = …` syntax, read both at the end, and return the log followed by the final values.""",
 solution="""
 @dynamicMemberLookup
 struct Audited<Value> {
     private(set) var value: Value
     let names: [PartialKeyPath<Value>: String]
     private(set) var log: [String] = []

     init(_ value: Value, names: [PartialKeyPath<Value>: String]) {
         self.value = value
         self.names = names
     }

     subscript<T>(dynamicMember keyPath: WritableKeyPath<Value, T>) -> T {
         get { value[keyPath: keyPath] }
         set {
             log.append("set \\(names[keyPath] ?? "?")")
             value[keyPath: keyPath] = newValue
         }
     }

     mutating func read<T>(_ keyPath: KeyPath<Value, T>) -> T {
         log.append("get \\(names[keyPath] ?? "?")")
         return value[keyPath: keyPath]
     }
 }

 struct Settings {
     var volume = 5
     var theme = "light"
 }

 func auditDemo(_ edits: [String]) -> [String] {
     var audited = Audited(Settings(), names: [\\Settings.volume: "volume", \\Settings.theme: "theme"])
     for edit in edits {
         let p = edit.split(separator: "=").map(String.init)
         if p[0] == "volume", let v = Int(p[1]) { audited.volume = v }
         if p[0] == "theme" { audited.theme = p[1] }
     }
     let volume = audited.read(\\.volume)
     let theme = audited.read(\\.theme)
     return audited.log + ["volume=\\(volume)", "theme=\\(theme)"]
 }
 """,
 explain="""With a **key-path** subscript, `audited.volume` is type-checked against `Settings` — autocomplete and typos are caught at compile time, unlike string-based dynamic members. This is how SwiftUI's `Binding` and `@Bindable` forward `$model.property`.""",
 hints=("A `@dynamicMemberLookup` subscript can take a `WritableKeyPath<Value, T>` instead of a `String`.","Getter reads `value[keyPath: keyPath]`; setter logs then writes it.","Key paths are `Hashable`, so `[PartialKeyPath<Value>: String]` can map them to names."),
 tests=[({'edits':['volume=9','theme=dark']},['set volume','set theme','get volume','get theme','volume=9','theme=dark']), {'edits':[]}]))
P[-1]['statement'] = P[-1]['statement'].replace(" — use `\"\\\\(keyPath)\"`? No — take names from a provided `[PartialKeyPath<Value>: String]`.", ". Take property names from a provided `[PartialKeyPath<Value>: String]` dictionary.")
P.append(dict(id='builtin-macros', title='Built-in Expression Macros', topic='Swift evolution', mode='predict', concepts=['compiler-directives','main-attribute'], docs=[('Expressions — Macro-Expansion Expression', EXP)],
 statement="""Swift has built-in "magic" expression macros used for logging and assertions. Predict the output (the judge compiles this file as `main.swift` in a module named `Solution`).""",
 snippet="""
 func logged(_ message: String, function: String = #function, line: Int = #line) -> String {
     "[\\(function):\\(line)] \\(message)"
 }

 struct Service {
     func start() -> String { logged("starting") }
 }

 print(#fileID)
 print(Service().start())
 print(logged("top level"))
 print(#column > 0, #function)
 """,
 explain="""`#fileID` is `Module/File.swift`, `#function` the enclosing declaration's name, `#line`/`#column` the source position. Used as **default arguments**, they capture the *caller's* location — which is how `assert`, `fatalError` and logging frameworks report where they were called. At top level, `#function` is the file-scope name.""",
 hints=("Default arguments like `#function` are evaluated at the **call site**.","`#fileID` is `Solution/main.swift` here.","Inside `start()`, `#function` is `start()`; the line is where `logged` is called.")))
write_all(P, 'advanced', 800)
