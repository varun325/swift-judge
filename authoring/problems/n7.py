import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CB='https://developer.apple.com/documentation/combine/'
CD='https://developer.apple.com/documentation/coredata/'
SD='https://developer.apple.com/documentation/swiftdata/'
MAC=['darwin']
STACK = '''
 import CoreData

 /// Built once and shared by every container: building a model is relatively expensive.
 nonisolated(unsafe) let sharedNotesModel: NSManagedObjectModel = {
     func attribute(_ name: String, _ type: NSAttributeType, optional: Bool = false) -> NSAttributeDescription {
         let a = NSAttributeDescription()
         a.name = name
         a.attributeType = type
         a.isOptional = optional
         return a
     }
     let folder = NSEntityDescription()
     folder.name = "Folder"
     folder.managedObjectClassName = NSStringFromClass(NSManagedObject.self)
     let note = NSEntityDescription()
     note.name = "Note"
     note.managedObjectClassName = NSStringFromClass(NSManagedObject.self)

     let notes = NSRelationshipDescription()
     notes.name = "notes"
     notes.destinationEntity = note
     notes.minCount = 0
     notes.maxCount = 0            // to-many
     notes.isOptional = true
     notes.deleteRule = .cascadeDeleteRule
     let folderRel = NSRelationshipDescription()
     folderRel.name = "folder"
     folderRel.destinationEntity = folder
     folderRel.maxCount = 1
     folderRel.isOptional = true
     folderRel.deleteRule = .nullifyDeleteRule
     notes.inverseRelationship = folderRel
     folderRel.inverseRelationship = notes

     folder.properties = [attribute("name", .stringAttributeType), notes]
     note.properties = [
         attribute("title", .stringAttributeType),
         attribute("body", .stringAttributeType),
         attribute("priority", .integer64AttributeType),
         attribute("created", .dateAttributeType),
         folderRel,
     ]
     let model = NSManagedObjectModel()
     model.entities = [folder, note]
     return model
 }()

 /// A fresh in-memory Core Data stack (no .xcdatamodeld needed) that shares the one model.
 func makeContainer() -> NSPersistentContainer {
     let container = NSPersistentContainer(name: "Notes", managedObjectModel: sharedNotesModel)
     let description = NSPersistentStoreDescription()
     description.type = NSInMemoryStoreType
     container.persistentStoreDescriptions = [description]
     container.loadPersistentStores { _, error in precondition(error == nil) }
     return container
 }
'''
P=[]
# ---------------- Combine
P.append(dict(id='combine-pipeline', title='Combine: map, filter, scan & removeDuplicates', topic='Combine', platforms=MAC, concepts=['map-filter-reduce','higher-order-functions'], docs=[('Publisher', CB+'publisher'), ('Processing Published Elements with Subscribers', CB+'processing-published-elements-with-subscribers')],
 sig='func runningTotals(_ readings: [Int]) -> [Int]',
 statement="""Swiftful's *Publishers and Subscribers in Combine*. Turn `readings` into a publisher (`readings.publisher`) and build a pipeline: drop negatives (`filter`), drop **consecutive** duplicates (`removeDuplicates`), keep a running total (`scan(0, +)`), then `sink` the values into an array.""",
 solution="""
 import Combine

 func runningTotals(_ readings: [Int]) -> [Int] {
     var out: [Int] = []
     let cancellable = readings.publisher
         .filter { $0 >= 0 }
         .removeDuplicates()
         .scan(0, +)
         .sink { out.append($0) }
     _ = cancellable
     return out
 }
 """,
 explain="""A Combine pipeline is a chain of operators between a publisher and a subscriber; values flow through as they're emitted. `scan` is `reduce` that emits every intermediate result. `removeDuplicates` only drops **adjacent** repeats. Sequence publishers emit synchronously, so the array is filled before `sink` returns.""",
 hints=("Any sequence has a `.publisher`.","Chain `filter`, `removeDuplicates()`, `scan(0, +)`, then `sink`.","Keep the returned `AnyCancellable` alive until you're done."),
 tests=[({'readings':[3,3,-1,4,4,4,2]},[3,7,9]), {'readings':[]}, {'readings':[-5,-6]}, {'readings':[1,2,1,2]}]))
P.append(dict(id='combine-subjects', title='Subjects: Passthrough vs CurrentValue', topic='Combine', diff='medium', platforms=MAC, concepts=['closures','capturing-values'], docs=[('PassthroughSubject', CB+'passthroughsubject'), ('CurrentValueSubject', CB+'currentvaluesubject')],
 sig='func subjectsDemo(_ events: [String]) -> [String]',
 statement="""Create a `PassthroughSubject<String, Never>` (events) and a `CurrentValueSubject<Int, Never>(0)` (score). Events: `emit <text>`, `score <n>`, `subscribe` (attach a **late** subscriber to both, logging `"late:<value>"`), `finish` (complete both). The first subscriber, attached at the start, logs `"early:<value>"`. Return the early subscriber's log, then `"--"`, then the late subscriber's log (Combine doesn't promise which subscriber hears a value first, so keep them separate).""",
 solution="""
 import Combine

 func subjectsDemo(_ events: [String]) -> [String] {
     let messages = PassthroughSubject<String, Never>()
     let score = CurrentValueSubject<Int, Never>(0)
     var early: [String] = []
     var late: [String] = []
     var bag = Set<AnyCancellable>()
     messages.sink { early.append("early:\\($0)") }.store(in: &bag)
     score.sink { early.append("early:\\($0)") }.store(in: &bag)
     for e in events {
         let p = e.split(separator: " ", maxSplits: 1).map(String.init)
         switch p[0] {
         case "emit": messages.send(p.count > 1 ? p[1] : "")
         case "score": score.send(Int(p.count > 1 ? p[1] : "") ?? 0)
         case "subscribe":
             messages.sink { late.append("late:\\($0)") }.store(in: &bag)
             score.sink { late.append("late:\\($0)") }.store(in: &bag)
         default:
             messages.send(completion: .finished)
             score.send(completion: .finished)
         }
     }
     return early + ["--"] + late
 }
 """,
 explain="""A `PassthroughSubject` forwards values only to current subscribers — late subscribers miss the past. A `CurrentValueSubject` stores the latest value and **replays it immediately** to new subscribers (like `@Published`). After completion, nothing more is delivered. Gotcha: when a subject has several subscribers, the **order** in which they receive a value is not specified — never depend on it.""",
 hints=("One subject has no memory; the other remembers its latest value.","A late subscriber to a `CurrentValueSubject` receives the current value right away.","Store cancellables in a `Set<AnyCancellable>` so subscriptions stay alive."),
 tests=[({'events':['emit hi','score 5','subscribe','emit yo','finish','emit lost']},['early:0','early:hi','early:5','early:yo','--','late:5','late:yo']), {'events':[]}, {'events':['subscribe','score 1']}]))
P.append(dict(id='combine-published-sink', title='@Published + $property Pipelines', topic='Combine', diff='medium', platforms=MAC, concepts=['property-wrappers','closures'], docs=[('Published', CB+'published')],
 sig='func searchPipeline(_ typed: [String]) -> [String]',
 statement="""Swiftful's *Filtering data based on search bar text using Combine*. A view model has `@Published var query = ""` and `@Published private(set) var results: [String] = []`. In `init`, subscribe to `$query`: trim, lowercase, `removeDuplicates()`, `dropFirst()` (skip the initial value), and map to the matching items from a fixed list (`["apple", "apricot", "banana", "blueberry", "cherry"]`, prefix match; empty query → all). Assign into `results` with `assign(to: &$results)`.

 Set each typed string and log `results` joined by `,` after each.""",
 solution="""
 import Combine

 final class SearchViewModel: ObservableObject {
     @Published var query = ""
     @Published private(set) var results: [String] = []
     private let all = ["apple", "apricot", "banana", "blueberry", "cherry"]

     init() {
         $query
             .map { $0.trimmingCharacters(in: .whitespaces).lowercased() }
             .removeDuplicates()
             .dropFirst()
             .map { [all] q in q.isEmpty ? all : all.filter { $0.hasPrefix(q) } }
             .assign(to: &$results)
     }
 }

 import Foundation

 func searchPipeline(_ typed: [String]) -> [String] {
     let vm = SearchViewModel()
     return typed.map { text in
         vm.query = text
         return vm.results.joined(separator: ",")
     }
 }
 """,
 explain="""`$query` is the `@Published` property's publisher. `assign(to: &$results)` republishes into another `@Published` property and ties the subscription's lifetime to the object — no `AnyCancellable` or `[weak self]` needed. `removeDuplicates` means typing the same normalised text twice does no work.""",
 hints=("`$query` is a publisher of every value `query` takes.","Normalise, `removeDuplicates()`, `dropFirst()`, map to results.","Finish with `.assign(to: &$results)` — it manages its own lifetime."),
 tests=[({'typed':['a','ap','AP ','b','']},['apple,apricot','apple,apricot','apple,apricot','banana,blueberry','apple,apricot,banana,blueberry,cherry']), {'typed':[]}, {'typed':['z']}]))
P.append(dict(id='combine-future', title='Future & Promise: One-Shot Async Values', topic='Combine', diff='medium', platforms=MAC, concepts=['closures','escaping','result-type'], docs=[('Future', CB+'future')],
 sig='func futures(_ inputs: [Int]) -> [String]',
 statement="""Swiftful's *Futures and Promises in Combine*. Write `func validate(_ n: Int) -> Future<Int, ValidationError>` that fulfils its promise **synchronously** with `.success(n * 2)` for positive numbers, else `.failure(.notPositive)`. Subscribe with `sink(receiveCompletion:receiveValue:)` and log `"value <v>"`, then `"finished"` or `"failed notPositive"`.""",
 solution="""
 import Combine

 enum ValidationError: Error { case notPositive }

 func validate(_ n: Int) -> Future<Int, ValidationError> {
     Future { promise in
         promise(n > 0 ? .success(n * 2) : .failure(.notPositive))
     }
 }

 func futures(_ inputs: [Int]) -> [String] {
     var log: [String] = []
     var bag = Set<AnyCancellable>()
     for n in inputs {
         validate(n)
             .sink(receiveCompletion: { completion in
                 switch completion {
                 case .finished: log.append("finished")
                 case .failure(let e): log.append("failed \\(e)")
                 }
             }, receiveValue: { log.append("value \\($0)") })
             .store(in: &bag)
     }
     return log
 }
 """,
 explain="""A `Future` runs its closure **once, immediately** when created (eagerly — like a JS `Promise`), then delivers one value and completes, or fails. Wrap it in `Deferred` to make it lazy. In async/await code, a plain `async throws` function replaces most Futures.""",
 hints=("A `Future` is created with a closure that receives a `promise` callback.","Call `promise(.success(…))` or `promise(.failure(…))` exactly once.","`sink(receiveCompletion:receiveValue:)` sees both the value and the completion."),
 tests=[({'inputs':[3,-1]},['value 6','finished','failed notPositive']), {'inputs':[]}]))
P.append(dict(id='combine-error-handling', title='Combine Errors: tryMap, catch & replaceError', topic='Combine', diff='medium', platforms=MAC, concepts=['error-handling','result-type'], docs=[('Publisher.tryMap(_:)', CB+'publisher/trymap(_:)'), ('Publisher.catch(_:)', CB+'publisher/catch(_:)')],
 sig='func parseStream(_ tokens: [String], recovery: String) -> [String]',
 statement="""Parse tokens as integers with `tryMap` (throw on a bad token). With `recovery`:
 - `"replace"` → `.replaceError(with: -1)` (the stream **ends** after the error)
 - `"catch"` → `.catch { _ in Just(0) }`
 - `"perItem"` → use `flatMap` so each token is parsed in its own inner publisher and errors are replaced per item, letting the outer stream continue

 Log values and a final `"done"`.""",
 solution="""
 import Combine

 struct BadToken: Error {}

 func parseStream(_ tokens: [String], recovery: String) -> [String] {
     var log: [String] = []
     let source = tokens.publisher
     let pipeline: AnyPublisher<Int, Never>
     switch recovery {
     case "replace":
         pipeline = source.tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
             .replaceError(with: -1).eraseToAnyPublisher()
     case "catch":
         pipeline = source.tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
             .catch { _ in Just(0) }.eraseToAnyPublisher()
     default:
         pipeline = source.flatMap { t in
             Just(t).tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
                 .replaceError(with: -1)
         }.eraseToAnyPublisher()
     }
     let c = pipeline.sink(receiveCompletion: { _ in log.append("done") }, receiveValue: { log.append(String($0)) })
     _ = c
     return log
 }
 """,
 explain="""In Combine an error **terminates** the stream — `replaceError`/`catch` substitute a final value, but no more upstream values arrive. To survive per-item failures, handle errors **inside** a `flatMap` so each item gets its own short-lived publisher. `eraseToAnyPublisher()` hides the long operator type.""",
 hints=("`tryMap` turns a thrown error into a failed stream.","Errors end a stream; recovering outside means the rest of the input is lost.","Handle the error inside `flatMap { Just($0).tryMap(…).replaceError(with: -1) }` to continue."),
 tests=[({'tokens':['1','x','3'],'recovery':'replace'},['1','-1','done']), ({'tokens':['1','x','3'],'recovery':'catch'},['1','0','done']), ({'tokens':['1','x','3'],'recovery':'perItem'},['1','-1','3','done']), {'tokens':[],'recovery':'replace'}]))
P.append(dict(id='combine-combinelatest-zip', title='combineLatest vs zip vs merge', topic='Combine', diff='medium', platforms=MAC, concepts=['tuples','higher-order-functions'], docs=[('Publisher.combineLatest(_:)', CB+'publisher/combinelatest(_:)'), ('Publisher.zip(_:)', CB+'publisher/zip(_:)')],
 sig='func combine(_ events: [String], mode: String) -> [String]',
 statement="""Two `PassthroughSubject`s: `a` (Int) and `b` (String). Events are `a <n>` or `b <s>`. Depending on `mode`, subscribe with:
 - `combineLatest` → `"<a>-<b>"` whenever either changes (after both have emitted)
 - `zip` → pairs `"<a>-<b>"` in order, one from each
 - `merge` → map both to strings and merge: `"a<n>"` / `"b<s>"`""",
 solution="""
 import Combine

 func combine(_ events: [String], mode: String) -> [String] {
     let a = PassthroughSubject<Int, Never>()
     let b = PassthroughSubject<String, Never>()
     var log: [String] = []
     let cancellable: AnyCancellable
     switch mode {
     case "combineLatest": cancellable = a.combineLatest(b).sink { log.append("\\($0)-\\($1)") }
     case "zip": cancellable = a.zip(b).sink { log.append("\\($0)-\\($1)") }
     default: cancellable = a.map { "a\\($0)" }.merge(with: b.map { "b\\($0)" }).sink { log.append($0) }
     }
     for e in events {
         let p = e.split(separator: " ", maxSplits: 1).map(String.init)
         if p[0] == "a" { a.send(Int(p.count > 1 ? p[1] : "") ?? 0) } else { b.send(p.count > 1 ? p[1] : "") }
     }
     _ = cancellable
     return log
 }
 """,
 explain="""`combineLatest` is for **state** (form validation: re-evaluate when any field changes). `zip` pairs values **one-to-one** in order (request/response). `merge` interleaves same-typed streams (events from several sources). Choosing the wrong one is a common Combine bug.""",
 hints=("Each operator combines two streams differently: latest values, strict pairs, or interleaving.","`a.combineLatest(b)`, `a.zip(b)`, and `a.map(…).merge(with: b.map(…))`.","`combineLatest` only starts emitting once both have a value."),
 tests=[({'events':['a 1','a 2','b x','a 3','b y'],'mode':'combineLatest'},['2-x','3-x','3-y']), ({'events':['a 1','a 2','b x','a 3','b y'],'mode':'zip'},['1-x','2-y']), ({'events':['a 1','b x','a 2'],'mode':'merge'},['a1','bx','a2']), {'events':[],'mode':'zip'}]))
P.append(dict(id='combine-cancellation', title='AnyCancellable Lifetimes', topic='Combine', diff='medium', platforms=MAC, concepts=['arc','closures-memory'], docs=[('AnyCancellable', CB+'anycancellable')],
 sig='func lifetimes(_ steps: [String]) -> [String]',
 statement="""A subscription lives only as long as its `AnyCancellable`. With one `PassthroughSubject<Int, Never>`, steps: `sub` (subscribe, **keeping** the cancellable in a set), `temp` (subscribe but **discard** the cancellable immediately), `send <n>`, `cancel` (cancel and remove all kept subscriptions). Each subscriber logs `"s<k>:<value>"` (k = subscription number). Return the log **sorted** (the order in which several subscribers receive one value isn't guaranteed).""",
 solution="""
 import Combine

 func lifetimes(_ steps: [String]) -> [String] {
     let subject = PassthroughSubject<Int, Never>()
     var log: [String] = []
     var kept = Set<AnyCancellable>()
     var counter = 0
     for step in steps {
         let p = step.split(separator: " ").map(String.init)
         switch p[0] {
         case "sub":
             counter += 1
             let k = counter
             subject.sink { log.append("s\\(k):\\($0)") }.store(in: &kept)
         case "temp":
             counter += 1
             let k = counter
             _ = subject.sink { log.append("s\\(k):\\($0)") }
         case "send": subject.send(Int(p.count > 1 ? p[1] : "") ?? 0)
         default:
             kept.forEach { $0.cancel() }
             kept.removeAll()
         }
     }
     return log.sorted()   // delivery order between subscribers isn't guaranteed
 }
 """,
 explain="""`AnyCancellable` cancels its subscription in `deinit`, so discarding it (`_ = …sink`) ends the subscription immediately — the classic "my sink never fires" bug. Storing it in a `Set<AnyCancellable>` owned by the view model ties it to the owner's lifetime.""",
 hints=("A subscription dies when its `AnyCancellable` is deallocated.","`_ = subject.sink { … }` is cancelled right away; `.store(in: &kept)` keeps it alive.","`cancel` should cancel everything in the set and empty it."),
 tests=[({'steps':['sub','temp','send 1','sub','send 2','cancel','send 3']},['s1:1','s1:2','s3:2']), {'steps':[]}]))
P.append(dict(id='combine-async-bridge', title='Bridging Combine to async/await with .values', topic='Combine', diff='hard', platforms=MAC, concepts=['async-await','property-wrappers'], docs=[('Publisher.values', CB+'publisher/values-1dm9r'), ('AsyncPublisher', CB+'asyncpublisher')],
 sig='func bridge(_ values: [Int], take: Int) async -> [Int]',
 statement="""Swiftful's *AsyncPublisher*: every publisher exposes `.values`, an `AsyncSequence`. Build the Combine pipeline `values.publisher.filter { $0 > 0 }.map { $0 * 10 }` and consume it with `for await v in pipeline.values`, collecting until you have `take` values (then `break`).""",
 solution="""
 import Combine

 func bridge(_ values: [Int], take: Int) async -> [Int] {
     let pipeline = values.publisher
         .filter { $0 > 0 }
         .map { $0 * 10 }
     var out: [Int] = []
     guard take > 0 else { return out }
     for await v in pipeline.values {
         out.append(v)
         if out.count >= take { break }
     }
     return out
 }
 """,
 explain="""`.values` turns any publisher into an `AsyncSequence`, so Combine can be consumed with `for await` — including `@Published` via `$property.values`. Breaking out of the loop cancels the subscription. **Timing trap:** with a *live* subject, the subscription starts only when the loop begins iterating, so values sent before that are missed (and a `CurrentValueSubject` replays whatever is current at that moment). This problem uses a finite publisher so the result is deterministic — an early version of it, built on a live subject, was flaky for exactly that reason.""",
 hints=("Any publisher has a `.values` async sequence.","Build the pipeline with `filter` and `map`, then `for await v in pipeline.values`.","`break` once you've collected `take` values."),
 tests=[({'values':[1,-2,3,4],'take':2},[10,30]), {'values':[5,6],'take':10}, {'values':[],'take':1}, {'values':[1],'take':0}]))
# ---------------- Core Data
P.append(dict(id='coredata-crud', title='Core Data: Create, Fetch & Sort', topic='Core Data', diff='medium', platforms=MAC, concepts=['class-definition','sort-custom'], docs=[('NSPersistentContainer', CD+'nspersistentcontainer'), ('NSFetchRequest', CD+'nsfetchrequest')],
 sig='func notesCRUD(_ ops: [String]) async -> [String]',
 statement="""Swiftful's *Core Data with MVVM*. The starter builds an **in-memory** Core Data stack in code (entities `Note` and `Folder`). Implement ops against `container.viewContext`:
 - `add <title> <priority>` → insert a `Note` (use `NSEntityDescription.insertNewObject` / `setValue`)
 - `rename <old> <new>`, `delete <title>` (first match)
 - `list` → fetch all notes sorted by priority **descending** then title, logging `"title(p)"` joined by `,`

 Save after every change.""",
 starter=STACK+"""
 func notesCRUD(_ ops: [String]) async -> [String] {
     let container = makeContainer()   // keep the container alive: the context doesn't own it
     // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
     // private-queue context and do ALL work inside `await context.perform`, which runs on the
     // context's own queue (performAndWait would run inline on the caller's thread — here, main).
     let context = container.newBackgroundContext()
     return await context.perform {
         var log: [String] = []
         // implement the ops (inside perform: the context's own queue)
         withExtendedLifetime(container) {}
         return log
     }
 }
 """,
 solution=STACK+"""
 func fetchNotes(_ context: NSManagedObjectContext, title: String? = nil) -> [NSManagedObject] {
     let request = NSFetchRequest<NSManagedObject>(entityName: "Note")
     if let title { request.predicate = NSPredicate(format: "title == %@", title) }
     request.sortDescriptors = [NSSortDescriptor(key: "priority", ascending: false), NSSortDescriptor(key: "title", ascending: true)]
     return (try? context.fetch(request)) ?? []
 }

 func notesCRUD(_ ops: [String]) async -> [String] {
     let container = makeContainer()   // keep the container alive: the context doesn't own it
     // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
     // private-queue context and do ALL work inside `await context.perform`, which runs on the
     // context's own queue (performAndWait would run inline on the caller's thread — here, main).
     let context = container.newBackgroundContext()
     return await context.perform {
     var log: [String] = []
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("add", 3):
             let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
             note.setValue(p[1], forKey: "title")
             note.setValue("", forKey: "body")
             note.setValue(Int64(p[2]) ?? 0, forKey: "priority")
             note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
         case ("rename", 3): fetchNotes(context, title: p[1]).first?.setValue(p[2], forKey: "title")
         case ("delete", 2): fetchNotes(context, title: p[1]).first.map(context.delete)
         case ("list", 1):
             log.append(fetchNotes(context).map { "\\($0.value(forKey: "title") as! String)(\\($0.value(forKey: "priority") as! Int64))" }.joined(separator: ","))
         default: break
         }
         if context.hasChanges { try? context.save() }
     }
     withExtendedLifetime(container) {}
     return log
     }
 }
 """,
 explain="""Core Data is an **object graph manager** on top of a store (SQLite, or in-memory for tests). Keep the `NSPersistentContainer` alive for as long as you use its contexts — `makeContainer().viewContext` releases the container immediately and later fetches can crash (an early version of this problem did exactly that). And **contexts are thread-confined**: `viewContext` belongs to the main queue, so touching it from a background thread (as async code often is) causes random crashes. Do work inside `await context.perform { }` (it runs on the context's own queue). Beware `performAndWait`: on the calling thread it runs *inline*, and when that's the main thread Core Data schedules follow-up work on the main run loop — an early version of these problems crashed intermittently for exactly that reason once the container was gone. You mutate managed objects in a context and `save()` to persist; fetch requests use `NSPredicate` and `NSSortDescriptor`. In real apps you'd generate `NSManagedObject` subclasses instead of `setValue(_:forKey:)`.""",
 hints=("Everything happens in a context: insert, mutate, delete, then `save()`.","`NSFetchRequest<NSManagedObject>(entityName: \"Note\")` with a predicate and sort descriptors.","Sort with two `NSSortDescriptor`s: priority descending, title ascending."),
 tests=[({'ops':['add milk 1','add taxes 3','add bike 3','list','rename milk oat-milk','delete bike','list']},['bike(3),taxes(3),milk(1)','taxes(3),oat-milk(1)']), {'ops':[]}, {'ops':['delete ghost','list']}]))
P.append(dict(id='coredata-predicates', title='NSPredicate Formats', topic='Core Data', diff='medium', platforms=MAC, concepts=['fundamental-types','string-equality'], docs=[('NSPredicate', 'https://developer.apple.com/documentation/foundation/nspredicate'), ('Predicate Programming Guide', 'https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Predicates/AdditionalChapters/Introduction.html')],
 sig='func queryNotes(_ notes: [[String]], queries: [String]) async -> [String]',
 statement="""Insert notes `[title, body, priority]`, then run each query and return matching titles (sorted) joined by `,`:
 - `search <text>` → `title CONTAINS[cd] %@ OR body CONTAINS[cd] %@`
 - `between <lo> <hi>` → `priority BETWEEN {lo, hi}` (use `%@` with an array)
 - `in <a,b,c>` → `title IN %@`
 - `urgent` → `priority >= 3 AND NOT (title BEGINSWITH[c] 'draft')`

 Always pass values with `%@` — never interpolate them into the format string.""",
 starter=STACK+"""
 func queryNotes(_ notes: [[String]], queries: [String]) async -> [String] {
     return []
 }
 """,
 solution=STACK+"""
 func queryNotes(_ notes: [[String]], queries: [String]) async -> [String] {
     let container = makeContainer()   // keep the container alive: the context doesn't own it
     // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
     // private-queue context and do ALL work inside `await context.perform`, which runs on the
     // context's own queue (performAndWait would run inline on the caller's thread — here, main).
     let context = container.newBackgroundContext()
     return await context.perform {
     for n in notes {
         let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
         note.setValue(n[0], forKey: "title")
         note.setValue(n[1], forKey: "body")
         note.setValue(Int64(n[2]) ?? 0, forKey: "priority")
         note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
     }
     try? context.save()
     return queries.map { q in
         let p = q.split(separator: " ", maxSplits: 1).map(String.init)
         let arg = p.count > 1 ? p[1] : ""
         let predicate: NSPredicate
         switch p[0] {
         case "search": predicate = NSPredicate(format: "title CONTAINS[cd] %@ OR body CONTAINS[cd] %@", arg, arg)
         case "between":
             let bounds = arg.split(separator: " ").compactMap { Int($0) }
             predicate = NSPredicate(format: "priority BETWEEN %@", bounds.count == 2 ? bounds : [0, 0])
         case "in": predicate = NSPredicate(format: "title IN %@", arg.split(separator: ",").map(String.init))
         default: predicate = NSPredicate(format: "priority >= 3 AND NOT (title BEGINSWITH[c] %@)", "draft")
         }
         let request = NSFetchRequest<NSManagedObject>(entityName: "Note")
         request.predicate = predicate
         let titles = ((try? context.fetch(request)) ?? []).compactMap { $0.value(forKey: "title") as? String }
         return withExtendedLifetime(container) { titles.sorted().joined(separator: ",") }
     }
     }
 }
 """,
 explain="""`[c]` = case-insensitive, `[d]` = diacritic-insensitive. `%@` substitutes values safely (quoting and escaping) — string-building predicates is both a correctness and an injection bug, just like SQL. SwiftData's `#Predicate` replaces these strings with type-checked Swift.""",
 hints=("Predicates use a mini-language: `CONTAINS[cd]`, `BETWEEN`, `IN`, `BEGINSWITH`.","Always substitute values with `%@`, passing arrays for `BETWEEN` and `IN`.","`NSPredicate(format: \"title CONTAINS[cd] %@ OR body CONTAINS[cd] %@\", text, text)`."),
 tests=[({'notes':[['Café plan','menu',2],['Draft essay','intro',5],['Taxes','cafe receipts',4],['Bike','fix tyre',1]],'queries':['search CAFE','between 2 4','in Bike,Taxes,Nope','urgent']},['Café plan,Taxes','Café plan,Taxes','Bike,Taxes','Taxes']), {'notes':[],'queries':['urgent']}]))
P[-1]['tests'] = [({'notes':[['Café plan','menu','2'],['Draft essay','intro','5'],['Taxes','cafe receipts','4'],['Bike','fix tyre','1']],'queries':['search CAFE','between 2 4','in Bike,Taxes,Nope','urgent']},['Café plan,Taxes','Café plan,Taxes','Bike,Taxes','Taxes']), {'notes':[],'queries':['urgent']}]
P.append(dict(id='coredata-relationships', title='Relationships & Delete Rules', topic='Core Data', diff='hard', platforms=MAC, concepts=['retain-cycle','class-definition'], docs=[('NSRelationshipDescription', CD+'nsrelationshipdescription'), ('NSDeleteRule', CD+'nsdeleterule')],
 sig='func folders(_ ops: [String]) async -> [String]',
 statement="""Swiftful's *Core Data relationships, predicates, and delete rules*. The model has `Folder.notes` (to-many, **cascade**) and `Note.folder` (to-one, **nullify**). Ops:
 - `folder <name>`, `note <title> <folderName>` (set `note.folder`; the inverse updates automatically)
 - `delete-folder <name>` (notes cascade), `delete-note <title>` (folder keeps existing)
 - `report` → `"<folder>:<note count>"` per folder (sorted) + `"notes <total>"`, via a fetch count""",
 starter=STACK+"""
 func folders(_ ops: [String]) async -> [String] {
     return []
 }
 """,
 solution=STACK+"""
 func first(_ entity: String, named key: String, _ value: String, in context: NSManagedObjectContext) -> NSManagedObject? {
     let r = NSFetchRequest<NSManagedObject>(entityName: entity)
     r.predicate = NSPredicate(format: "%K == %@", key, value)
     r.fetchLimit = 1
     return try? context.fetch(r).first
 }

 func folders(_ ops: [String]) async -> [String] {
     let container = makeContainer()   // keep the container alive: the context doesn't own it
     // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
     // private-queue context and do ALL work inside `await context.perform`, which runs on the
     // context's own queue (performAndWait would run inline on the caller's thread — here, main).
     let context = container.newBackgroundContext()
     return await context.perform {
     var log: [String] = []
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("folder", 2):
             NSEntityDescription.insertNewObject(forEntityName: "Folder", into: context).setValue(p[1], forKey: "name")
         case ("note", 3):
             guard let folder = first("Folder", named: "name", p[2], in: context) else { continue }
             let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
             note.setValue(p[1], forKey: "title")
             note.setValue("", forKey: "body")
             note.setValue(Int64(0), forKey: "priority")
             note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
             note.setValue(folder, forKey: "folder")
         case ("delete-folder", 2): first("Folder", named: "name", p[1], in: context).map(context.delete)
         case ("delete-note", 2): first("Note", named: "title", p[1], in: context).map(context.delete)
         case ("report", 1):
             let r = NSFetchRequest<NSManagedObject>(entityName: "Folder")
             r.sortDescriptors = [NSSortDescriptor(key: "name", ascending: true)]
             for f in (try? context.fetch(r)) ?? [] {
                 let count = (f.value(forKey: "notes") as? Set<NSManagedObject>)?.count ?? 0
                 log.append("\\(f.value(forKey: "name") as! String):\\(count)")
             }
             log.append("notes \\((try? context.count(for: NSFetchRequest<NSManagedObject>(entityName: "Note"))) ?? 0)")
         default: break
         }
         if context.hasChanges { try? context.save() }
     }
     withExtendedLifetime(container) {}
     return log
     }
 }
 """,
 explain="""Declaring an **inverse** keeps both sides in sync (setting `note.folder` adds the note to `folder.notes`). Delete rules decide what happens to related objects: **cascade** deletes the notes with their folder; **nullify** just clears the reference. `%K` substitutes a key path name, `%@` a value; `count(for:)` counts without loading objects. All of it runs inside `await context.perform { }` because a context may only be used on its own queue.""",
 hints=("Set the to-one side (`note.folder`); the inverse to-many updates itself.","Deleting a folder cascades to its notes; deleting a note nullifies its folder link.","Report with `notes` set counts and `context.count(for:)`."),
 tests=[({'ops':['folder home','folder work','note milk home','note taxes home','note deck work','delete-note milk','report','delete-folder home','report']},['home:1','work:1','notes 2','work:1','notes 1']), {'ops':['report']}]))
P.append(dict(id='coredata-pagination', title='Fetch Limits, Offsets & Counts', topic='Core Data', diff='medium', platforms=MAC, concepts=['fundamental-types'], docs=[('NSFetchRequest.fetchOffset', CD+'nsfetchrequest/fetchoffset'), ('NSFetchRequest.fetchLimit', CD+'nsfetchrequest/fetchlimit')],
 sig='func pages(total: Int, pageSize: Int) async -> [String]',
 statement="""Insert `total` notes titled `n001`, `n002`, …, then page through them sorted by title using `fetchLimit` = pageSize and `fetchOffset` = page × pageSize. Return one line per page `"page <k>: <first>..<last>"`, starting with `"count <total>"` from `count(for:)`. Stop at the first empty page.""",
 starter=STACK+"""
 func pages(total: Int, pageSize: Int) async -> [String] {
     return []
 }
 """,
 solution=STACK+"""
 import Foundation

 func pages(total: Int, pageSize: Int) async -> [String] {
     let container = makeContainer()   // keep the container alive: the context doesn't own it
     // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
     // private-queue context and do ALL work inside `await context.perform`, which runs on the
     // context's own queue (performAndWait would run inline on the caller's thread — here, main).
     let context = container.newBackgroundContext()
     return await context.perform {
     for i in stride(from: 1, through: total, by: 1) {
         let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
         note.setValue(String(format: "n%03d", i), forKey: "title")
         note.setValue("", forKey: "body")
         note.setValue(Int64(0), forKey: "priority")
         note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
     }
     try? context.save()
     let countRequest = NSFetchRequest<NSManagedObject>(entityName: "Note")
     var log = ["count \\((try? context.count(for: countRequest)) ?? 0)"]
     guard pageSize > 0 else { return log }
     var page = 0
     while true {
         let r = NSFetchRequest<NSManagedObject>(entityName: "Note")
         r.sortDescriptors = [NSSortDescriptor(key: "title", ascending: true)]
         r.fetchLimit = pageSize
         r.fetchOffset = page * pageSize
         let items = ((try? context.fetch(r)) ?? []).compactMap { $0.value(forKey: "title") as? String }
         guard let firstTitle = items.first, let lastTitle = items.last else { break }
         log.append("page \\(page): \\(firstTitle)..\\(lastTitle)")
         page += 1
     }
     withExtendedLifetime(container) {}
     return log
     }
 }
 """,
 explain="""`fetchLimit`/`fetchOffset` push paging into the store (SQL `LIMIT`/`OFFSET`), so you never load the whole table; `count(for:)` asks for a count without materialising objects. Firestore pagination (Swiftful's Firebase series) solves the same problem with cursors.""",
 hints=("Let the store page for you with `fetchLimit` and `fetchOffset`.","Sort by title so pages are stable; loop until a page comes back empty.","`context.count(for:)` gives the total cheaply."),
 tests=[({'total':7,'pageSize':3},['count 7','page 0: n001..n003','page 1: n004..n006','page 2: n007..n007']), {'total':0,'pageSize':5}, {'total':4,'pageSize':4}]))
P.append(dict(id='coredata-background-context', title='Background Contexts & Merging Changes', topic='Core Data', diff='hard', platforms=MAC, concepts=['async-await','sendable'], docs=[('NSManagedObjectContext.perform(_:)', CD+'nsmanagedobjectcontext/perform(_:)'), ('Using Core Data in the background', CD+'using-core-data-in-the-background')],
 sig='func importInBackground(_ titles: [String]) async -> [String]',
 statement="""Swiftful's *Multi-threading* + Core Data. Import notes on a **background context** (`container.newBackgroundContext()` + `await context.perform { … }`), save it, and verify the **view context** sees them because `viewContext.automaticallyMergesChangesFromParent = true`. Pass only `NSManagedObjectID`s (Sendable) between contexts — never managed objects.

 Return `["background saved <n>", "main sees <n>", first imported title fetched on main via its objectID]`.""",
 starter=STACK+"""
 func importInBackground(_ titles: [String]) async -> [String] {
     return []
 }
 """,
 solution=STACK+"""
 func importInBackground(_ titles: [String]) async -> [String] {
     let container = makeContainer()
     container.viewContext.automaticallyMergesChangesFromParent = true
     let background = container.newBackgroundContext()
     let ids: [NSManagedObjectID] = await background.perform {
         let notes = titles.map { title -> NSManagedObject in
             let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: background)
             note.setValue(title, forKey: "title")
             note.setValue("", forKey: "body")
             note.setValue(Int64(0), forKey: "priority")
             note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
             return note
         }
         try? background.save()
         return notes.map(\\.objectID)
     }
     let main = container.viewContext
     return await main.perform {
         let count = (try? main.count(for: NSFetchRequest<NSManagedObject>(entityName: "Note"))) ?? 0
         let first = ids.first.flatMap { try? main.existingObject(with: $0).value(forKey: "title") as? String } ?? "-"
         return ["background saved \\(ids.count)", "main sees \\(count)", first]
     }
 }
 """,
 explain="""Managed objects are **not** thread-safe: each belongs to its context's queue, and you access it only inside `perform`. `NSManagedObjectID` is the Sendable handle you pass across, then re-fetch with `existingObject(with:)`. Heavy imports on a background context keep the UI responsive; automatic merging updates the main context.""",
 hints=("Do the work inside `await background.perform { … }` and return object IDs.","Save the background context; the view context merges automatically when configured.","On the main context, re-fetch with `existingObject(with: id)`."),
 tests=[({'titles':['a','b','c']},['background saved 3','main sees 3','a']), {'titles':[]}]))
# ---------------- SwiftData
P.append(dict(id='swiftdata-crud', title='SwiftData: @Model CRUD', topic='SwiftData', diff='medium', platforms=MAC, concepts=['class-definition','sort-custom'], docs=[('SwiftData', SD), ('Model()', SD+'model()'), ('ModelContext', SD+'modelcontext')],
 sig='func booksCRUD(_ ops: [String]) async -> [String]',
 statement="""Paul's *Storing our data with SwiftData*. Define `@Model final class Book { var title: String; var author: String; var rating: Int }`. Using an in-memory `ModelContainer` and its `mainContext` (on the `@MainActor`), apply ops `add <title>|<author>|<rating>`, `rate <title> <n>`, `delete <title>`, `list` (sorted by rating desc then title via `FetchDescriptor(sortBy:)`, logging `"title(r)"` joined by `,`).""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class Book {
     var title: String
     var author: String
     var rating: Int
     init(title: String, author: String, rating: Int) {
         self.title = title
         self.author = author
         self.rating = rating
     }
 }

 @MainActor func run(_ ops: [String]) throws -> [String] {
     let container = try ModelContainer(for: Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     var log: [String] = []
     func find(_ title: String) throws -> Book? {
         var d = FetchDescriptor<Book>(predicate: #Predicate { $0.title == title })
         d.fetchLimit = 1
         return try context.fetch(d).first
     }
     for op in ops {
         let p = op.split(separator: " ", maxSplits: 1).map(String.init)
         let arg = p.count > 1 ? p[1] : ""
         switch p[0] {
         case "add":
             let f = arg.split(separator: "|").map(String.init)
             if f.count == 3 { context.insert(Book(title: f[0], author: f[1], rating: Int(f[2]) ?? 0)) }
         case "rate":
             let f = arg.split(separator: " ").map(String.init)
             if f.count == 2, let book = try find(f[0]) { book.rating = Int(f[1]) ?? book.rating }
         case "delete":
             if let book = try find(arg) { context.delete(book) }
         default:
             let d = FetchDescriptor<Book>(sortBy: [SortDescriptor(\\.rating, order: .reverse), SortDescriptor(\\.title)])
             log.append(try context.fetch(d).map { "\\($0.title)(\\($0.rating))" }.joined(separator: ","))
         }
     }
     return log
 }

 func booksCRUD(_ ops: [String]) async -> [String] {
     (try? await run(ops)) ?? ["error"]
 }
 """,
 explain="""`@Model` turns a plain class into a persistent, observable model — no model file, no `NSManagedObject`. `ModelContext` inserts, deletes and autosaves; `FetchDescriptor` pairs a type-checked `#Predicate` with `SortDescriptor`s. It's Core Data underneath, with a Swift-native API.""",
 hints=("Mark the class `@Model`; create a `ModelContainer` with `isStoredInMemoryOnly: true`.","Insert with `context.insert`, delete with `context.delete`, mutate properties directly.","Fetch with `FetchDescriptor<Book>(sortBy: [SortDescriptor(\\.rating, order: .reverse), SortDescriptor(\\.title)])`."),
 tests=[({'ops':['add Dune|Herbert|5','add Emma|Austen|4','add Ulysses|Joyce|4','list','rate Emma 5','delete Ulysses','list']},['Dune(5),Emma(4),Ulysses(4)','Dune(5),Emma(5)']), {'ops':['list']}]))
P.append(dict(id='swiftdata-predicates', title='SwiftData #Predicate Queries', topic='SwiftData', diff='medium', platforms=MAC, concepts=['closures','key-paths'], docs=[('Predicate', 'https://developer.apple.com/documentation/foundation/predicate'), ('FetchDescriptor', SD+'fetchdescriptor')],
 sig='func findBooks(_ books: [[String]], queries: [String]) async -> [String]',
 statement="""Paul's *Filtering the results from a SwiftData query*. Insert books `[title, author, rating]` and run each query with `#Predicate` (type-checked Swift, not strings):
 - `author <text>` → `$0.author.localizedStandardContains(text)`
 - `min <n>` → rating ≥ n
 - `range <lo> <hi>` → lo ≤ rating ≤ hi **and** title not empty

 Return titles sorted, joined by `,`, and `fetchCount` for the query as `"(<n>)"`.""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class Book {
     var title: String
     var author: String
     var rating: Int
     init(title: String, author: String, rating: Int) {
         self.title = title
         self.author = author
         self.rating = rating
     }
 }

 @MainActor func run(_ books: [[String]], _ queries: [String]) throws -> [String] {
     let container = try ModelContainer(for: Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     for b in books { context.insert(Book(title: b[0], author: b[1], rating: Int(b[2]) ?? 0)) }
     return try queries.map { q in
         let p = q.split(separator: " ").map(String.init)
         let predicate: Predicate<Book>
         switch p[0] {
         case "author":
             let text = p.count > 1 ? p[1] : ""
             predicate = #Predicate { $0.author.localizedStandardContains(text) }
         case "min":
             let n = Int(p.count > 1 ? p[1] : "") ?? 0
             predicate = #Predicate { $0.rating >= n }
         default:
             let lo = Int(p.count > 1 ? p[1] : "") ?? 0
             let hi = Int(p.count > 2 ? p[2] : "") ?? 0
             predicate = #Predicate { $0.rating >= lo && $0.rating <= hi && !$0.title.isEmpty }
         }
         let descriptor = FetchDescriptor<Book>(predicate: predicate, sortBy: [SortDescriptor(\\.title)])
         let titles = try context.fetch(descriptor).map(\\.title)
         return "\\(titles.joined(separator: ",")) (\\(try context.fetchCount(descriptor)))"
     }
 }

 func findBooks(_ books: [[String]], queries: [String]) async -> [String] {
     (try? await run(books, queries)) ?? ["error"]
 }
 """,
 explain="""`#Predicate` is a macro: it looks like a Swift closure but is translated into a query the store can execute. It's type-checked (typos and type mismatches are compile errors) but supports only a subset of Swift — capture plain values into local constants first, as here.""",
 hints=("`#Predicate { $0.rating >= n }` builds a type-checked query.","Capture query values into local `let`s before using them in the macro.","`context.fetchCount(descriptor)` counts without loading models."),
 tests=[({'books':[['Dune','Frank Herbert','5'],['Emma','Jane Austen','4'],['Persuasion','Jane Austen','3']],'queries':['author jane','min 4','range 3 4']},['Emma,Persuasion (2)','Dune,Emma (2)','Emma,Persuasion (2)']), {'books':[],'queries':['min 1']}]))
P.append(dict(id='swiftdata-relationships', title='SwiftData Relationships & Cascade Delete', topic='SwiftData', diff='hard', platforms=MAC, concepts=['class-definition','retain-cycle'], docs=[('Relationship(_:deleteRule:minimumModelCount:maximumModelCount:originalName:inverse:hashModifier:)', SD+'relationship(_:deleterule:minimummodelcount:maximummodelcount:originalname:inverse:hashmodifier:)')],
 sig='func libraryGraph(_ ops: [String]) async -> [String]',
 statement="""Paul's *Working with relationships*. `@Model final class Author { var name: String; @Relationship(deleteRule: .cascade, inverse: \\Book.author) var books: [Book] = [] }` and `@Model final class Book { var title: String; var author: Author? }`. Ops: `author <name>`, `book <title> <authorName>` (append to the author's `books`), `delete-author <name>`, `delete-book <title>`, `report` (`"<author>:<n>"` sorted + `"books <total>"`). Save after each op.""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class Author {
     var name: String
     @Relationship(deleteRule: .cascade, inverse: \\Book.author) var books: [Book] = []
     init(name: String) { self.name = name }
 }

 @Model
 final class Book {
     var title: String
     var author: Author?
     init(title: String) { self.title = title }
 }

 @MainActor func run(_ ops: [String]) throws -> [String] {
     let container = try ModelContainer(for: Author.self, Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     var log: [String] = []
     func author(_ name: String) throws -> Author? { try context.fetch(FetchDescriptor<Author>(predicate: #Predicate { $0.name == name })).first }
     func book(_ title: String) throws -> Book? { try context.fetch(FetchDescriptor<Book>(predicate: #Predicate { $0.title == title })).first }
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("author", 2): context.insert(Author(name: p[1]))
         case ("book", 3):
             guard let a = try author(p[2]) else { break }
             let b = Book(title: p[1])
             context.insert(b)
             a.books.append(b)
         case ("delete-author", 2): if let a = try author(p[1]) { context.delete(a) }
         case ("delete-book", 2): if let b = try book(p[1]) { context.delete(b) }
         case ("report", 1):
             for a in try context.fetch(FetchDescriptor<Author>(sortBy: [SortDescriptor(\\.name)])) { log.append("\\(a.name):\\(a.books.count)") }
             log.append("books \\(try context.fetchCount(FetchDescriptor<Book>()))")
         default: break
         }
         try context.save()
     }
     return log
 }

 func libraryGraph(_ ops: [String]) async -> [String] {
     (try? await run(ops)) ?? ["error"]
 }
 """,
 explain="""`@Relationship(deleteRule: .cascade, inverse:)` gives the same guarantees as Core Data: appending to `author.books` also sets `book.author`, and deleting an author deletes their books. Without the inverse/cascade you'd leave orphaned rows behind.""",
 hints=("Declare the to-many side with `@Relationship(deleteRule: .cascade, inverse: \\Book.author)`.","Insert the book, then append it to the author's `books` — the inverse is set for you.","Count books with `fetchCount(FetchDescriptor<Book>())` after saving."),
 tests=[({'ops':['author Austen','author Herbert','book Emma Austen','book Persuasion Austen','book Dune Herbert','delete-book Emma','report','delete-author Austen','report']},['Austen:1','Herbert:1','books 2','Herbert:1','books 1']), {'ops':['report']}]))
P.append(dict(id='swiftdata-pagination-unique', title='SwiftData: Unique Attributes & Pagination', topic='SwiftData', diff='hard', platforms=MAC, concepts=['equatable-hashable','fundamental-types'], docs=[('Attribute(_:originalName:hashModifier:)', SD+'attribute(_:originalname:hashmodifier:)'), ('FetchDescriptor', SD+'fetchdescriptor')],
 sig='func syncTags(_ incoming: [String], pageSize: Int) async -> [String]',
 statement="""Syncing from a server often means **upserting**. `@Model final class Tag { @Attribute(.unique) var slug: String; var uses: Int }` — inserting a model whose unique `slug` already exists **updates** the existing row instead of duplicating it. Insert a `Tag(slug:, uses: 1)` for each incoming slug but first read the current `uses` so the count increments. Then page through tags sorted by slug with `fetchLimit`/`fetchOffset`, logging `"<slug>=<uses>"` per page (joined by `,`).""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class Tag {
     @Attribute(.unique) var slug: String
     var uses: Int
     init(slug: String, uses: Int) {
         self.slug = slug
         self.uses = uses
     }
 }

 @MainActor func run(_ incoming: [String], _ pageSize: Int) throws -> [String] {
     let container = try ModelContainer(for: Tag.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     for slug in incoming {
         let existing = try context.fetch(FetchDescriptor<Tag>(predicate: #Predicate { $0.slug == slug })).first
         context.insert(Tag(slug: slug, uses: (existing?.uses ?? 0) + 1))
         try context.save()
     }
     guard pageSize > 0 else { return [] }
     var pages: [String] = []
     var offset = 0
     while true {
         var d = FetchDescriptor<Tag>(sortBy: [SortDescriptor(\\.slug)])
         d.fetchLimit = pageSize
         d.fetchOffset = offset
         let page = try context.fetch(d)
         if page.isEmpty { break }
         pages.append(page.map { "\\($0.slug)=\\($0.uses)" }.joined(separator: ","))
         offset += pageSize
     }
     return pages
 }

 func syncTags(_ incoming: [String], pageSize: Int) async -> [String] {
     (try? await run(incoming, pageSize)) ?? ["error"]
 }
 """,
 explain="""`@Attribute(.unique)` makes inserts **upserts** keyed on that property — ideal for syncing server data idempotently. Paging with `fetchLimit`/`fetchOffset` keeps memory flat for large tables (SwiftUI's `@Query` does similar batching for you).""",
 hints=("A `.unique` attribute turns a second insert with the same key into an update.","Read the existing `uses` first so the new insert carries the incremented count.","Page with `fetchLimit` and increasing `fetchOffset` until a page is empty."),
 tests=[({'incoming':['swift','ios','swift','ui','swift'],'pageSize':2},['ios=1,swift=3','ui=1']), {'incoming':[],'pageSize':3}, {'incoming':['a'],'pageSize':5}]))
write_all(P, 'frameworks', 300)
