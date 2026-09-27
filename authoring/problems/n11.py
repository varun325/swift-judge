import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
AD='https://developer.apple.com/documentation/'
DOC=AD+'swiftui/'
MAC=['darwin']
S=[]  # swiftui track
F=[]  # frameworks track
S.append(dict(id='task-modifier-lifecycle', title='.task(id:): Automatic Restart & Cancellation', topic='State & data flow', diff='medium', platforms=MAC, concepts=['async-await','task-group'], docs=[('task(id:priority:_:)', DOC+'view')],
 sig='func taskLifecycle(_ events: [String]) async -> [String]',
 statement="""Swiftful's *Task and .task*. `.task(id: query)` starts a task when the view appears, **cancels and restarts** it whenever `query` changes, and cancels it when the view disappears. Simulate that runtime with a small `TaskRunner` that owns the current `Task`: events `appear <q>`, `change <q>` (only restarts if the id actually changed), `disappear`. Each task sleeps 20 ms then logs `"loaded <q>"` unless cancelled (then `"cancelled <q>"`). Wait 60 ms after the last event and return the sorted log.""",
 solution="""
 actor Log {
     private(set) var lines: [String] = []
     func add(_ s: String) { lines.append(s) }
 }

 @MainActor
 final class TaskRunner {
     private var task: Task<Void, Never>?
     private var currentID: String?
     let log: Log
     init(log: Log) { self.log = log }

     func start(_ id: String) {
         task?.cancel()
         currentID = id
         let log = self.log
         task = Task {
             try? await Task.sleep(for: .milliseconds(20))
             if Task.isCancelled { await log.add("cancelled \\(id)") } else { await log.add("loaded \\(id)") }
         }
     }

     func appear(_ id: String) { start(id) }
     func change(_ id: String) { if id != currentID { start(id) } }
     func disappear() { task?.cancel(); task = nil; currentID = nil }
 }

 func taskLifecycle(_ events: [String]) async -> [String] {
     let log = Log()
     let runner = await TaskRunner(log: log)
     for e in events {
         let p = e.split(separator: " ", maxSplits: 1).map(String.init)
         switch p[0] {
         case "appear": await runner.appear(p.count > 1 ? p[1] : "")
         case "change": await runner.change(p.count > 1 ? p[1] : "")
         default: await runner.disappear()
         }
     }
     try? await Task.sleep(for: .milliseconds(80))
     return await log.lines.sorted()
 }
 """,
 explain="""`.task` ties async work to a view's lifetime — no manual cancellation, no leaks. With `id:`, a changed value cancels the in-flight work and starts fresh (perfect for search), and unchanged values do nothing. Your async code must honour cancellation (`Task.sleep` throws; check `Task.isCancelled`).""",
 hints=("Keep a reference to the current `Task` so you can cancel it.","Restart only when the id actually changes; `disappear` cancels.","The task checks `Task.isCancelled` after its sleep."),
 tests=[({'events':['appear a','change a','change b','disappear']},['cancelled a','cancelled b']), {'events':['appear x']}, {'events':['appear a','change b']}], hidden=0))
S.append(dict(id='scroll-reader-target', title='ScrollViewReader: Choosing a Scroll Target', topic='Lists', platforms=MAC, concepts=['optionals','higher-order-functions'], docs=[('ScrollViewReader', DOC+'scrollviewreader'), ('ScrollViewProxy.scrollTo(_:anchor:)', DOC+'scrollviewproxy/scrollto(_:anchor:)')],
 sig='func scrollTargets(ids: [String], commands: [String]) -> [String]',
 statement="""Swiftful's *ScrollViewReader to auto scroll*. A chat screen calls `proxy.scrollTo(id, anchor:)`. Given message ids (in order) and commands, compute the id to scroll to: `bottom` (last message), `top` (first), `unread <id>` (the first message **after** `<id>`, or the last one if `<id>` is last/unknown), `search <text>` (first id containing the text, case-insensitive). Return `"<id> @<anchor>"` (`bottom` → `.bottom`, others → `.top`) or `"none"`.""",
 solution="""
 func scrollTargets(ids: [String], commands: [String]) -> [String] {
     commands.map { c in
         let p = c.split(separator: " ", maxSplits: 1).map(String.init)
         let arg = p.count > 1 ? p[1] : ""
         let target: String?
         var anchor = "top"
         switch p[0] {
         case "bottom": target = ids.last; anchor = "bottom"
         case "top": target = ids.first
         case "unread":
             if let i = ids.firstIndex(of: arg), i + 1 < ids.count { target = ids[i + 1] } else { target = ids.last }
         default: target = ids.first { $0.localizedCaseInsensitiveContains(arg) }
         }
         return target.map { "\\($0) @\\(anchor)" } ?? "none"
     }
 }

 import Foundation
 """,
 explain="""`ScrollViewReader` scrolls by **identity**, not offset, so the target id must match the `id` used in `ForEach`. Computing the target in the model keeps the view simple: `withAnimation { proxy.scrollTo(target, anchor: .bottom) }`. (iOS 17's `scrollPosition(id:)` binds the same idea two-way.)""",
 hints=("Scroll targets are ids, so compute which id you want.","`unread x` means the message right after `x`, falling back to the last.","Search with `localizedCaseInsensitiveContains` and take the first match."),
 tests=[({'ids':['m1','m2','hello-3','m4'],'commands':['bottom','top','unread m2','unread m4','search HELLO','search zzz']},['m4 @bottom','m1 @top','hello-3 @top','m4 @top','hello-3 @top','none']), {'ids':[],'commands':['bottom']}]))
S.append(dict(id='phase-animator-sequence', title='PhaseAnimator: Stepping Through Phases', topic='Animation', diff='medium', platforms=MAC, concepts=['enums','case-iterable'], docs=[('PhaseAnimator', DOC+'phaseanimator'), ('phaseAnimator(_:trigger:content:animation:)', DOC+'view/phaseanimator(_:trigger:content:animation:)')],
 sig='func phaseTimeline(triggers: Int, durations: [Double]) -> [String]',
 statement="""`PhaseAnimator` walks through a sequence of phases each time its `trigger` changes, then returns to the first. Model `enum Phase: CaseIterable { case idle, lift, spin, drop }` with a computed `scale` (`1, 1.2, 1.2, 1`) and `rotation` (`0, 0, 180, 360`). Each phase transition takes `durations[i]` seconds (i = target phase index − 1, looping). For `triggers` trigger changes, produce the timeline `"<t>s <phase> scale <s> rot <r>"` for every phase entered (t cumulative, 1 decimal), starting with `"0.0s idle …"`.""",
 solution="""
 enum Phase: CaseIterable {
     case idle, lift, spin, drop
     var scale: Double { self == .lift || self == .spin ? 1.2 : 1 }
     var rotation: Int {
         switch self {
         case .idle, .lift: 0
         case .spin: 180
         case .drop: 360
         }
     }
 }

 func phaseTimeline(triggers: Int, durations: [Double]) -> [String] {
     var t = 0.0
     func line(_ p: Phase) -> String { "\\((t * 10).rounded() / 10)s \\(p) scale \\(p.scale) rot \\(p.rotation)" }
     var out = [line(.idle)]
     guard !durations.isEmpty else { return out }
     for _ in 0..<max(triggers, 0) {
         let sequence = Array(Phase.allCases.dropFirst()) + [.idle]
         for (i, phase) in sequence.enumerated() {
             t += durations[i % durations.count]
             out.append(line(phase))
         }
     }
     return out
 }
 """,
 explain="""A phase enum with computed visual properties is exactly what you pass to `PhaseAnimator(Phase.allCases, trigger: tapCount) { content, phase in content.scaleEffect(phase.scale) … } animation: { phase in … }` — multi-step animations become data. Returning to the first phase makes the sequence repeatable.""",
 hints=("Put visual values (scale, rotation) on the phase enum as computed properties.","Each trigger walks lift → spin → drop → idle.","Accumulate time from the per-transition durations."),
 tests=[({'triggers':1,'durations':[0.2,0.5,0.3,0.4]},['0.0s idle scale 1.0 rot 0','0.2s lift scale 1.2 rot 0','0.7s spin scale 1.2 rot 180','1.0s drop scale 1.0 rot 360','1.4s idle scale 1.0 rot 0']), {'triggers':0,'durations':[1]}, {'triggers':2,'durations':[0.5]}]))
S.append(dict(id='scene-phase-autosave', title='scenePhase: Save When Backgrounded', topic='State & data flow', platforms=MAC, concepts=['enums','switch-statement'], docs=[('ScenePhase', DOC+'scenephase')],
 sig='func lifecycleSaves(_ phases: [String], edits: [Int]) -> [String]',
 statement="""Apps should persist work when the scene leaves the foreground. `@Environment(\\.scenePhase)` moves between `active`, `inactive` and `background`. Given the phase sequence and, for each step, how many unsaved edits were made just before it, log `"save <n>"` when transitioning **to `background`** with pending edits (then reset), `"refresh"` when returning to `active` **from `background`**, and `"-"` otherwise. Ignore repeated identical phases.""",
 solution="""
 enum AppPhase: String { case active, inactive, background }

 func lifecycleSaves(_ phases: [String], edits: [Int]) -> [String] {
     var current = AppPhase.active
     var pending = 0
     return zip(phases, edits).map { raw, newEdits in
         pending += newEdits
         guard let next = AppPhase(rawValue: raw), next != current else { return "-" }
         defer { current = next }
         switch (current, next) {
         case (_, .background) where pending > 0:
             defer { pending = 0 }
             return "save \\(pending)"
         case (.background, .active): return "refresh"
         default: return "-"
         }
     }
 }
 """,
 explain="""`.onChange(of: scenePhase) { old, new in … }` is where you save; `inactive` also happens for things like Control Center, so saving only on `background` avoids needless writes. Returning from background is a good moment to refresh stale data.""",
 hints=("React to *transitions*, not to the phase value alone.","Save pending edits on the way into `background`; refresh when coming back from it.","Skip unknown or unchanged phases."),
 tests=[({'phases':['inactive','background','background','active','inactive','active'],'edits':[2,1,0,0,3,0]},['-','save 3','-','refresh','-','-']), {'phases':[],'edits':[]}]))
S.append(dict(id='contrast-ratio', title='Accessibility: Contrast Ratios for Dynamic Colors', topic='Accessibility', diff='medium', platforms=MAC, concepts=['fundamental-types','extensions'], docs=[('Color', DOC+'color'), ('Accessibility — Color and effects', 'https://developer.apple.com/design/human-interface-guidelines/accessibility#Color-and-effects')],
 sig='func contrastChecks(_ pairs: [[String]]) -> [String]',
 statement="""Swiftful's *Accessibility: Dynamic Colors*. Text must have enough contrast against its background — WCAG requires **4.5:1** (AA) for body text, 3:1 for large text. For each `[foregroundHex, backgroundHex]`, compute relative luminance (sRGB channels linearised: `c ≤ 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4`, then `0.2126R + 0.7152G + 0.0722B`) and the ratio `(L1 + 0.05) / (L2 + 0.05)` (lighter over darker). Return `"<ratio 2dp> AA|AA-large|fail"`.""",
 solution="""
 import Foundation

 func luminance(_ hex: String) -> Double? {
     let digits = hex.hasPrefix("#") ? String(hex.dropFirst()) : hex
     guard digits.count == 6, let v = UInt32(digits, radix: 16) else { return nil }
     let channels = [(v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF].map { Double($0) / 255 }
     let linear = channels.map { $0 <= 0.03928 ? $0 / 12.92 : pow(($0 + 0.055) / 1.055, 2.4) }
     return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
 }

 func contrastChecks(_ pairs: [[String]]) -> [String] {
     pairs.map { p in
         guard let a = luminance(p[0]), let b = luminance(p[1]) else { return "invalid" }
         let ratio = (max(a, b) + 0.05) / (min(a, b) + 0.05)
         let grade = ratio >= 4.5 ? "AA" : ratio >= 3 ? "AA-large" : "fail"
         return "\\((ratio * 100).rounded() / 100) \\(grade)"
     }
 }
 """,
 explain="""Contrast is computed on **perceived luminance**, not raw RGB — green contributes far more than blue. Check both light and dark appearances of every dynamic color pair (asset-catalog colors switch per `colorScheme`), and respect `accessibilityShowButtonShapes`/increased-contrast settings where relevant.""",
 hints=("Linearise each sRGB channel before weighting.","Luminance = 0.2126 R + 0.7152 G + 0.0722 B.","Ratio = (lighter + 0.05) / (darker + 0.05); compare with 4.5 and 3."),
 tests=[({'pairs':[['#000000','#FFFFFF'],['#767676','#FFFFFF'],['#999999','#FFFFFF'],['#FF0000','#00FF00'],['#zzz','#fff']]},['21.0 AA','4.54 AA','2.85 fail','2.91 fail','invalid']), {'pairs':[]}]))
S.append(dict(id='inflection-pluralization', title='Localization: Automatic Grammar Agreement', topic='Accessibility', platforms=MAC, concepts=['string-interpolation','compiler-directives'], docs=[('AttributedString init(localized:)', AD+'foundation/attributedstring'), ('Localization', AD+'xcode/localization')],
 sig='func cartBadges(_ counts: [Int]) -> [String]',
 statement="""Hand-written `count == 1 ? "item" : "items"` breaks in other languages. Foundation's **automatic grammar agreement** inflects for you: `AttributedString(localized: "^[\\(n) item](inflect: true)")`. For each count return `"<inflected items> in cart"`, and also the same with a `.formatted()` count for thousands separators (`en_US`): e.g. `"1,200 items"` — use `Text`-style markdown inflection on a pre-formatted string.""",
 solution="""
 import Foundation

 func cartBadges(_ counts: [Int]) -> [String] {
     counts.map { n in
         let phrase = AttributedString(localized: "^[\\(n) item](inflect: true) in cart")
         return String(phrase.characters)
     }
 }
 """,
 explain="""The `^[…](inflect: true)` markdown attribute tells Foundation to make the noun agree with the number — for English, Spanish, French, German and more — and SwiftUI's `Text` supports it directly. For full control (Arabic has six plural forms), use String Catalogs' plural variations.""",
 hints=("Let Foundation inflect: `^[\\(n) item](inflect: true)`.","Create it with `AttributedString(localized:)`.","Convert to a plain string with `String(attributed.characters)`."),
 tests=[({'counts':[0,1,2]},['0 items in cart','1 item in cart','2 items in cart']), {'counts':[1000]}]))
S[-1]['statement'] = """Hand-written `count == 1 ? "item" : "items"` breaks in other languages. Foundation's **automatic grammar agreement** inflects for you: `AttributedString(localized: "^[\\(n) item](inflect: true) in cart")`. Return the inflected phrase for each count."""
F.append(dict(id='dispatch-group', title='GCD: DispatchGroup & Concurrent Queues', topic='Concurrency (GCD)', diff='medium', platforms=MAC, concepts=['dispatch-sync-async','closures'], docs=[('DispatchGroup', AD+'dispatch/dispatchgroup'), ('DispatchQueue', AD+'dispatch/dispatchqueue')],
 sig='func gcdBatch(_ items: [Int]) -> [String]',
 statement="""Swiftful's *Multi-threading with background threads and queues*. Before async/await, fan-out/fan-in used `DispatchGroup`: dispatch each item to a **concurrent** queue (`DispatchQueue(label:attributes: .concurrent)`) inside `group.enter()`/`leave()`, square it, and store results through a **serial** "lock" queue. Block with `group.wait()`, then return the results sorted plus `"items <n>"`.""",
 solution="""
 import Dispatch

 final class Results: @unchecked Sendable {
     private var values: [Int] = []
     private let lock = DispatchQueue(label: "results.lock")
     func add(_ v: Int) { lock.sync { values.append(v) } }
     var all: [Int] { lock.sync { values } }
 }

 func gcdBatch(_ items: [Int]) -> [String] {
     let worker = DispatchQueue(label: "worker", attributes: .concurrent)
     let group = DispatchGroup()
     let results = Results()
     for item in items {
         group.enter()
         worker.async {
             results.add(item * item)
             group.leave()
         }
     }
     group.wait()
     return results.all.sorted().map(String.init) + ["items \\(items.count)"]
 }
 """,
 explain="""`enter`/`leave` count outstanding work; `wait()` blocks until the count hits zero (`notify(queue:)` is the non-blocking version). Results from concurrent work must be collected through synchronisation — here a serial queue used as a lock. Structured concurrency (`withTaskGroup`) replaces all of this with less ceremony.""",
 hints=("`group.enter()` before dispatching, `group.leave()` when the work finishes.","Append results through a serial queue so concurrent writes don't race.","`group.wait()` then sort — completion order isn't deterministic."),
 tests=[({'items':[3,1,2]},['1','4','9','items 3']), {'items':[]}, {'items':list(range(1,21))}]))
F.append(dict(id='predict-serial-queue-order', title='Predict: Serial Queue Ordering', topic='Concurrency (GCD)', mode='predict', diff='medium', platforms=MAC, concepts=['dispatch-sync-async'], docs=[('DispatchQueue', AD+'dispatch/dispatchqueue')],
 statement="""FullStack.Cafe asks about `sync` vs `async`. A **serial** queue runs one block at a time, in order. `async` returns immediately; `sync` waits. Predict the output.""",
 snippet="""
 import Dispatch

 let queue = DispatchQueue(label: "serial")
 var log: [String] = []
 queue.async { log.append("A") }
 queue.async { log.append("B") }
 queue.sync { log.append("C") }
 log.append("D")
 queue.async { log.append("E") }
 queue.sync { }
 print(log.joined(separator: ","))
 """,
 explain="""On a serial queue, `sync` enqueues behind everything already queued and waits for it — so by the time `C` runs, `A` and `B` are done, and `D` only appends after `sync` returns. The empty `sync {}` at the end is a common way to wait for queued `async` work (`E`). Calling `sync` on the queue you're already on would deadlock.""",
 hints=("A serial queue runs blocks one at a time in the order they were enqueued.","`sync` doesn't return until its block — and everything queued before it — has run.","The empty `sync {}` waits for `E`.")))
F.append(dict(id='unidirectional-store', title='Unidirectional Data Flow (TCA/Redux-Style Store)', topic='Architecture', diff='hard', platforms=MAC, concepts=['enums','associated-values','mutating','async-await'], docs=[('The Composable Architecture (GitHub)', 'https://github.com/pointfreeco/swift-composable-architecture')],
 sig='func storeRun(_ actions: [String]) async -> [String]',
 statement="""Swiftful's *SwiftUI Advanced Architecture* compares MVVM with unidirectional architectures like TCA. Build one: `struct AppState: Equatable { var count = 0; var fact: String?; var isLoading = false }`, `enum Action { case increment, decrement, factButtonTapped, factResponse(String) }`, and a **pure** `reduce(_ state: inout AppState, _ action: Action) -> Effect?`, where an effect is async work that produces another action. A `@MainActor final class Store` sends actions, runs effects, and feeds their results back in.

 The fact effect returns `"fact about <count>"`. Actions: `+`, `-`, `fact`. Log the state after every action the store processes (including effect results) as `"<count> <loading|-> <fact|->"`.""",
 solution="""
 struct AppState: Equatable {
     var count = 0
     var fact: String?
     var isLoading = false
 }

 enum Action {
     case increment, decrement, factButtonTapped
     case factResponse(String)
 }

 typealias Effect = @Sendable () async -> Action

 func reduce(_ state: inout AppState, _ action: Action) -> Effect? {
     switch action {
     case .increment: state.count += 1; state.fact = nil; return nil
     case .decrement: state.count -= 1; state.fact = nil; return nil
     case .factButtonTapped:
         state.isLoading = true
         let n = state.count
         return { .factResponse("fact about \\(n)") }
     case .factResponse(let fact):
         state.isLoading = false
         state.fact = fact
         return nil
     }
 }

 @MainActor
 final class Store {
     private(set) var state = AppState()
     private(set) var history: [String] = []

     func send(_ action: Action) async {
         let effect = reduce(&state, action)
         history.append("\\(state.count) \\(state.isLoading ? "loading" : "-") \\(state.fact ?? "-")")
         if let effect { await send(await effect()) }
     }
 }

 func storeRun(_ actions: [String]) async -> [String] {
     let store = await Store()
     for a in actions {
         switch a {
         case "+": await store.send(.increment)
         case "-": await store.send(.decrement)
         case "fact": await store.send(.factButtonTapped)
         default: break
         }
     }
     return await store.history
 }
 """,
 explain="""All state changes go through one pure reducer (`(inout State, Action) -> Effect?`), and side effects come back as **actions** — a single, testable path for every change. This is Redux's model with Swift value types: `inout` state instead of returning a new object, and enums with payloads as actions.""",
 hints=("State is a struct; actions are an enum; the reducer mutates `inout` state.","Side effects are returned as async closures that produce the next action.","The store runs the reducer, records state, then awaits the effect and sends its action."),
 tests=[({'actions':['+','+','fact','-']},['1 - -','2 - -','2 loading -','2 - fact about 2','1 - -']), {'actions':[]}]))
F.append(dict(id='diffable-snapshot', title='Diffable Data Sources: Snapshots', topic='UIKit & AppKit', diff='medium', platforms=MAC, concepts=['equatable-hashable','collection-types'], docs=[('NSDiffableDataSourceSnapshot', AD+'uikit/nsdiffabledatasourcesnapshot'), ('Updating collection views using diffable data sources', AD+'uikit/updating-collection-views-using-diffable-data-sources')],
 sig='func snapshotOps(_ ops: [String]) -> [String]',
 statement="""UIKit's modern table and collection views are driven by **diffable data source snapshots** — the same identity-based diffing idea as SwiftUI's `ForEach`. `NSDiffableDataSourceSnapshot` exists in AppKit too, so the judge can run it. Build a snapshot with sections and item identifiers: ops `section <name>`, `add <section> <items,…>`, `delete <item>`, `move <item> after <item>`, `reload <item>` (marks it for reload). Return each section as `"<section>: <items>"`, then `"items <n>"` and `"reloaded <ids>"`.""",
 solution="""
 import AppKit

 func snapshotOps(_ ops: [String]) -> [String] {
     var snapshot = NSDiffableDataSourceSnapshot<String, String>()
     var reloaded: Set<String> = []
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("section", 2): snapshot.appendSections([p[1]])
         case ("add", 3):
             if snapshot.sectionIdentifiers.contains(p[1]) {
                 snapshot.appendItems(p[2].split(separator: ",").map(String.init).filter { snapshot.indexOfItem($0) == nil }, toSection: p[1])
             }
         case ("delete", 2): if snapshot.indexOfItem(p[1]) != nil { snapshot.deleteItems([p[1]]); reloaded.remove(p[1]) }
         case ("move", 4) where p[2] == "after":
             if snapshot.indexOfItem(p[1]) != nil, snapshot.indexOfItem(p[3]) != nil, p[1] != p[3] {
                 snapshot.moveItem(p[1], afterItem: p[3])
             }
         case ("reload", 2): if snapshot.indexOfItem(p[1]) != nil { snapshot.reloadItems([p[1]]); reloaded.insert(p[1]) }
         default: break
         }
     }
     let sections = snapshot.sectionIdentifiers.map { "\\($0): \\(snapshot.itemIdentifiers(inSection: $0).joined(separator: ","))" }
     return sections + ["items \\(snapshot.numberOfItems)", "reloaded \\(reloaded.sorted().joined(separator: ","))"]
 }
 """,
 explain="""A snapshot describes the **whole** desired state by identifiers; `dataSource.apply(snapshot)` computes and animates the difference — no more `performBatchUpdates` index bookkeeping crashes. Identifiers must be unique `Hashable` values (duplicates crash), which is why the solution filters them.""",
 hints=("Build the full desired state with `appendSections` and `appendItems(_:toSection:)`.","Item identifiers must be unique — skip ones already present.","`moveItem(_:afterItem:)`, `deleteItems`, `reloadItems`, then read `itemIdentifiers(inSection:)`."),
 tests=[({'ops':['section fruit','section veg','add fruit apple,pear,fig','add veg kale','move apple after fig','delete pear','reload kale','add fruit fig']},['fruit: fig,apple','veg: kale','items 3','reloaded kale']), {'ops':[]}]))
F.append(dict(id='sort-descriptors-swift', title='SortDescriptor & KeyPathComparator on Swift Types', topic='Foundation essentials', platforms=MAC, concepts=['key-paths','sort-custom'], docs=[('SortDescriptor', AD+'foundation/sortdescriptor'), ('KeyPathComparator', AD+'foundation/keypathcomparator')],
 sig='func sortPlayers(_ rows: [[String]], by keys: [String]) -> [String]',
 statement="""SwiftUI's `Table` and SwiftData use `SortDescriptor`s — they work on plain Swift types too (`array.sorted(using:)`). Players are `[name, score, country]`. Build `[SortDescriptor<Player>]` from keys like `score-` (descending) and `name` / `country` (ascending, `.localizedStandard` comparator for strings), apply them in order, and return the names.""",
 solution="""
 import Foundation

 struct Player {
     let name: String
     let score: Int
     let country: String
 }

 func sortPlayers(_ rows: [[String]], by keys: [String]) -> [String] {
     let players = rows.map { Player(name: $0[0], score: Int($0[1]) ?? 0, country: $0[2]) }
     let descriptors: [SortDescriptor<Player>] = keys.compactMap { key in
         let descending = key.hasSuffix("-")
         let order: SortOrder = descending ? .reverse : .forward
         switch key.trimmingCharacters(in: CharacterSet(charactersIn: "-")) {
         case "score": return SortDescriptor(\\.score, order: order)
         case "name": return SortDescriptor(\\.name, comparator: .localizedStandard, order: order)
         case "country": return SortDescriptor(\\.country, comparator: .localizedStandard, order: order)
         default: return nil
         }
     }
     return players.sorted(using: descriptors).map(\\.name)
 }
 """,
 explain="""A list of sort descriptors is a data description of "sort by A, then B" — you can store it, bind it to a table's column headers, or pass it to a SwiftData `@Query`. `.localizedStandard` sorts strings the way Finder does (`"file2" < "file10"`, case/diacritic-insensitive).""",
 hints=("Create one `SortDescriptor` per key, in priority order.","`order: .reverse` for descending; `comparator: .localizedStandard` for strings.","Apply them all with `sorted(using: descriptors)`."),
 tests=[({'rows':[['bo','90','SE'],['Ana','90','BR'],['cy','70','BR'],['Émile','90','FR']],'keys':['score-','name']},['Ana','bo','Émile','cy']), {'rows':[['a','1','X'],['b','2','A']],'keys':['country']}, {'rows':[],'keys':['score']}]))
F.append(dict(id='ab-test-bucketing', title='Deterministic A/B Test Bucketing', topic='Product engineering', platforms=MAC, concepts=['hashing','fundamental-types','integer-overflow'], docs=[('Hasher', AD+'swift/hasher')],
 sig='func assignVariants(userIDs: [String], experiment: String, splits: [Int]) -> [String]',
 statement="""Swiftful's *What to A/B test in your app*. Assign each user to a variant **deterministically** — the same user must get the same variant on every launch and device. Swift's `Hasher` is randomly seeded per process, so it's unusable; implement 32-bit **FNV-1a** over the UTF-8 of `"<experiment>:<userID>"` (offset 2166136261, prime 16777619, wrapping multiplication), take `hash % 100` as the bucket, and map it to variants `A`, `B`, `C`… using cumulative `splits` (percentages). Return `"<user>: <variant> (bucket <b>)"`.""",
 solution="""
 func fnv1a(_ s: String) -> UInt32 {
     var hash: UInt32 = 2_166_136_261
     for byte in s.utf8 {
         hash ^= UInt32(byte)
         hash = hash &* 16_777_619
     }
     return hash
 }

 func assignVariants(userIDs: [String], experiment: String, splits: [Int]) -> [String] {
     userIDs.map { user in
         let bucket = Int(fnv1a("\\(experiment):\\(user)") % 100)
         var cumulative = 0
         var variant = "control"
         for (i, pct) in splits.enumerated() {
             cumulative += pct
             if bucket < cumulative {
                 variant = String(UnicodeScalar(UInt8(65 + i)))
                 break
             }
         }
         return "\\(user): \\(variant) (bucket \\(bucket))"
     }
 }
 """,
 explain="""`hashValue`/`Hasher` change between launches (to defeat hash-flooding), so persisted or cross-device decisions need a stable hash like FNV-1a. Salting with the experiment name makes different experiments independent. Unassigned leftover percentage falls into `control`.""",
 hints=("Don't use `hashValue` — it changes every launch.","FNV-1a: `hash ^= byte; hash = hash &* prime` over the UTF-8 bytes.","Bucket = `hash % 100`; walk cumulative split percentages to pick A, B, C…"),
 tests=[{'userIDs':['u1','u2','u3','alice','bob'],'experiment':'paywall-v2','splits':[50,50]}, {'userIDs':['u1'],'experiment':'x','splits':[10]}, {'userIDs':[],'experiment':'x','splits':[100]}]))
F.append(dict(id='review-prompt-rules', title='When to Ask for an App Store Review', topic='Product engineering', platforms=MAC, concepts=['guard','dates' if False else 'control-flow'], docs=[('RequestReviewAction', AD+'storekit/requestreviewaction')],
 sig='func reviewPrompts(_ events: [[String]]) -> [String]',
 statement="""Swiftful's *How to improve App Store rating*: ask at a moment of success, not at random. `requestReview()` is rate-limited by the system anyway, so your own rules decide *when to try*. Events are `[day, kind]` with kinds `success`, `crash`, `launch`. Prompt on a `success` only if: at least 3 successes so far (including this one), no crash in the last 7 days, the last prompt was ≥ 60 days ago (or never), and at most 3 prompts per 365 days. Return the days on which you'd prompt, as `"prompt day <d>"`.""",
 solution="""
 func reviewPrompts(_ events: [[String]]) -> [String] {
     var successes = 0
     var lastCrash: Int?
     var prompts: [Int] = []
     var out: [String] = []
     for e in events {
         guard e.count == 2, let day = Int(e[0]) else { continue }
         switch e[1] {
         case "crash": lastCrash = day
         case "success":
             successes += 1
             let noRecentCrash = lastCrash.map { day - $0 > 7 } ?? true
             let spaced = prompts.last.map { day - $0 >= 60 } ?? true
             let yearly = prompts.count(where: { day - $0 < 365 }) < 3
             if successes >= 3 && noRecentCrash && spaced && yearly {
                 prompts.append(day)
                 out.append("prompt day \\(day)")
             }
         default: break
         }
     }
     return out
 }
 """,
 explain="""Apple limits prompts to three per 365 days and may show none; asking after a user **succeeded** (finished a task) and not after a crash produces better ratings. Keeping these rules in a pure function makes them testable and easy to tune.""",
 hints=("Track success count, last crash day and previous prompt days.","All four conditions must hold on a `success` event.","Count prompts within the last 365 days with `count(where:)`."),
 tests=[({'events':[['1','success'],['2','success'],['3','crash'],['5','success'],['12','success'],['40','success'],['75','success'],['140','success'],['200','success'],['300','success']]},['prompt day 12','prompt day 75','prompt day 140']), {'events':[]}]))
F.append(dict(id='infinite-scroll', title='Infinite Scroll: When to Load the Next Page', topic='Product engineering', diff='medium', platforms=MAC, concepts=['optionals','guard'], docs=[('onAppear(perform:)', DOC+'view/onappear(perform:)'), ('LazyVStack', DOC+'lazyvstack')],
 sig='func feedPaging(pageSize: Int, totalAvailable: Int, visibleIndices: [Int]) -> [String]',
 statement="""A `LazyVStack` calls `.onAppear` as rows become visible; load the next page when a row within the last `threshold = 3` items appears. Guard against duplicate loads (`isLoading`) and stop at the end (`hasMore`). Loads complete instantly here. For each visible index (in order) log `"load page <n>"` when a load starts, else `"-"`. Start with page 0 already loaded (`pageSize` items).""",
 solution="""
 struct FeedModel {
     let pageSize: Int
     let totalAvailable: Int
     private(set) var loadedCount: Int
     private(set) var page = 0
     private(set) var isLoading = false
     var hasMore: Bool { loadedCount < totalAvailable }

     init(pageSize: Int, totalAvailable: Int) {
         self.pageSize = pageSize
         self.totalAvailable = totalAvailable
         loadedCount = min(pageSize, totalAvailable)
     }

     mutating func rowAppeared(_ index: Int) -> Int? {
         guard hasMore, !isLoading, index >= loadedCount - 3 else { return nil }
         isLoading = true
         page += 1
         loadedCount = min(loadedCount + pageSize, totalAvailable)
         isLoading = false
         return page
     }
 }

 func feedPaging(pageSize: Int, totalAvailable: Int, visibleIndices: [Int]) -> [String] {
     var model = FeedModel(pageSize: pageSize, totalAvailable: totalAvailable)
     return visibleIndices.map { i in model.rowAppeared(i).map { "load page \\($0)" } ?? "-" }
 }
 """,
 explain="""Prefetching a few rows before the end hides loading latency; the `isLoading` guard stops the same trigger from firing several loads, and `hasMore` stops requests once the server is exhausted. In real code the load is async and `isLoading` stays true until it finishes.""",
 hints=("Trigger when the appearing index is within the last 3 loaded rows.","Guard on `hasMore` and `!isLoading`.","Each load adds up to `pageSize` rows, capped at the total."),
 tests=[{'pageSize':10,'totalAvailable':25,'visibleIndices':[0,5,6,7,8,15,16,17,22,24]}, {'pageSize':5,'totalAvailable':3,'visibleIndices':[0,1,2]}, {'pageSize':2,'totalAvailable':10,'visibleIndices':[]}]))
F.append(dict(id='offline-sync-queue', title='Offline-First Sync Queue', topic='Product engineering', diff='hard', platforms=MAC, concepts=['enums','associated-values','error-handling'], docs=[('NWPathMonitor', AD+'network/nwpathmonitor')],
 sig='func syncQueue(_ events: [String]) -> [String]',
 statement="""Apps should keep working offline and sync later. Model a FIFO queue of pending mutations: `enum Mutation { case create(String), rename(from: String, to: String), delete(String) }`. Events: `create x`, `rename x y`, `delete x` (enqueue), `offline`, `online` (flush the queue in order while online; a mutation targeting a name the server doesn't have fails and is **dropped** with a log), and `status`. **Coalesce** before sending: a `create` followed by `delete` of the same item cancels both. Log each sent mutation as `"sent <mutation>"`, failures as `"dropped <mutation>"`, and `status` as `"server: <names sorted>"`.""",
 solution="""
 enum Mutation: CustomStringConvertible {
     case create(String)
     case rename(from: String, to: String)
     case delete(String)
     var description: String {
         switch self {
         case .create(let n): "create \\(n)"
         case let .rename(a, b): "rename \\(a)->\\(b)"
         case .delete(let n): "delete \\(n)"
         }
     }
 }

 func coalesce(_ queue: [Mutation]) -> [Mutation] {
     var result: [Mutation] = []
     for m in queue {
         if case .delete(let name) = m, let i = result.lastIndex(where: { if case .create(name) = $0 { return true }; return false }) {
             result.remove(at: i)
             continue
         }
         result.append(m)
     }
     return result
 }

 func syncQueue(_ events: [String]) -> [String] {
     var online = true
     var pending: [Mutation] = []
     var server: Set<String> = []
     var log: [String] = []

     func flush() {
         for m in coalesce(pending) {
             switch m {
             case .create(let n): server.insert(n); log.append("sent \\(m)")
             case let .rename(a, b):
                 if server.remove(a) != nil { server.insert(b); log.append("sent \\(m)") } else { log.append("dropped \\(m)") }
             case .delete(let n):
                 if server.remove(n) != nil { log.append("sent \\(m)") } else { log.append("dropped \\(m)") }
             }
         }
         pending = []
     }

     for e in events {
         let p = e.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("create", 2): pending.append(.create(p[1]))
         case ("rename", 3): pending.append(.rename(from: p[1], to: p[2]))
         case ("delete", 2): pending.append(.delete(p[1]))
         case ("offline", 1): online = false
         case ("online", 1): online = true
         case ("status", 1): log.append("server: \\(server.sorted().joined(separator: ","))")
         default: break
         }
         if online { flush() }
     }
     return log
 }
 """,
 explain="""Offline-first means the **local** state updates immediately and a durable queue replays changes later, in order. Coalescing (create + delete = nothing) saves requests and avoids errors; conflicts (renaming something that no longer exists) need an explicit policy — here, drop and log. `NWPathMonitor` tells you when connectivity returns.""",
 hints=("Queue mutations as enum values; flush them in order whenever you're online.","Before flushing, remove create/delete pairs for the same item.","Rename/delete of a missing server item is dropped and logged."),
 tests=[({'events':['offline','create a','create b','delete b','rename a c','status','online','status','delete zzz']},['server: ','sent create a','sent rename a->c','server: c','dropped delete zzz']), {'events':[]}]))
F.append(dict(id='universal-link-matching', title='Universal Links: AASA Path Matching', topic='Product engineering', diff='medium', platforms=MAC, concepts=['codable','regex','optionals'], docs=[('Supporting universal links in your app', AD+'xcode/supporting-universal-links-in-your-app'), ('Supporting associated domains', AD+'xcode/supporting-associated-domains')],
 sig='func matchLinks(aasa: String, urls: [String]) -> [String]',
 statement="""iOS decides whether an `https://` link opens your app using the `apple-app-site-association` file's `components`. Decode a simplified AASA: `{"applinks": {"details": [{"appIDs": [...], "components": [{"/": "/orders/*"}, {"/": "/admin/*", "exclude": true}, {"/": "/p/?"}]}]}}`. Patterns: `*` matches any run of characters, `?` exactly one; components are checked **in order** and the first match wins (an `exclude` match means "open in Safari"). Return `"app"` or `"web"` per URL path.""",
 solution="""
 import Foundation

 struct AASA: Decodable {
     struct Applinks: Decodable { let details: [Detail] }
     struct Detail: Decodable { let components: [Component] }
     struct Component: Decodable {
         let path: String
         let exclude: Bool?
         enum CodingKeys: String, CodingKey { case path = "/", exclude }
     }
     let applinks: Applinks
 }

 func wildcardMatches(_ pattern: String, _ text: String) -> Bool {
     let p = Array(pattern), t = Array(text)
     var memo: [[Bool?]] = Array(repeating: Array(repeating: nil, count: t.count + 1), count: p.count + 1)
     func match(_ i: Int, _ j: Int) -> Bool {
         if let cached = memo[i][j] { return cached }
         let result: Bool
         if i == p.count { result = j == t.count }
         else if p[i] == "*" { result = match(i + 1, j) || (j < t.count && match(i, j + 1)) }
         else { result = j < t.count && (p[i] == "?" || p[i] == t[j]) && match(i + 1, j + 1) }
         memo[i][j] = result
         return result
     }
     return match(0, 0)
 }

 func matchLinks(aasa: String, urls: [String]) -> [String] {
     guard let file = try? JSONDecoder().decode(AASA.self, from: Data(aasa.utf8)) else { return urls.map { _ in "web" } }
     let components = file.applinks.details.flatMap(\\.components)
     return urls.map { url in
         guard let path = URLComponents(string: url)?.path else { return "web" }
         guard let hit = components.first(where: { wildcardMatches($0.path, path) }) else { return "web" }
         return hit.exclude == true ? "web" : "app"
     }
 }
 """,
 explain="""Universal links are verified by the AASA file your server hosts; ordering matters because the first matching component wins, so put `exclude` rules **before** broad patterns. Wildcard matching with memoised recursion is the same algorithm as glob matching.""",
 hints=("Decode the AASA; the path key is literally `\"/\"` — map it with `CodingKeys`.","Glob-match `*` and `?` against the URL path (memoised recursion or DP).","First matching component decides; `exclude: true` means web."),
 tests=[({'aasa':'{"applinks":{"details":[{"appIDs":["T.x"],"components":[{"/":"/admin/*","exclude":true},{"/":"/orders/*"},{"/":"/p/?"}]}]}}','urls':['https://shop.example/orders/42','https://shop.example/admin/users','https://shop.example/p/7','https://shop.example/p/77','https://shop.example/']},['app','web','app','web','web']), {'aasa':'bad','urls':['https://x.y/orders/1']}]))
F.append(dict(id='image-downsampling', title='Image Downsampling Math', topic='Performance', platforms=MAC, concepts=['fundamental-types','memory-layout'], docs=[('Image I/O: CGImageSourceCreateThumbnailAtIndex', AD+'imageio/cgimagesourcecreatethumbnailatindex(_:_:_:)')],
 sig='func downsample(_ images: [[Double]]) -> [String]',
 statement="""Displaying a 4000×3000 photo in a 100×100 pt thumbnail wastes ~46 MB of decoded memory. Given `[pixelWidth, pixelHeight, displayWidthPt, displayHeightPt, screenScale]`, compute the thumbnail's **max pixel size** for `CGImageSourceCreateThumbnailAtIndex` so the image *fills* the display area (aspect-fill: scale factor = max(displayW×scale/pixelW, displayH×scale/pixelH), never upscale), then report `"<w>x<h>px, <decodedKB> KB vs <originalKB> KB"` (4 bytes per pixel, integer division by 1024).""",
 solution="""
 func downsample(_ images: [[Double]]) -> [String] {
     images.map { i in
         let (pw, ph, dw, dh, scale) = (i[0], i[1], i[2], i[3], i[4])
         let factor = min(1, max(dw * scale / pw, dh * scale / ph))
         let w = Int((pw * factor).rounded(.up)), h = Int((ph * factor).rounded(.up))
         let decoded = w * h * 4 / 1024
         let original = Int(pw) * Int(ph) * 4 / 1024
         return "\\(w)x\\(h)px, \\(decoded) KB vs \\(original) KB"
     }
 }
 """,
 explain="""Decoded image memory depends on **pixels**, not file size: width × height × 4 bytes. Downsampling with ImageIO (`kCGImageSourceThumbnailMaxPixelSize`) before display is the biggest memory win in image-heavy feeds — what Kingfisher's `DownsamplingImageProcessor` does.""",
 hints=("Memory = pixels × 4 bytes, regardless of the JPEG's file size.","Aspect-fill: the scale factor is the larger of the two ratios, capped at 1.","Round the thumbnail dimensions up to whole pixels."),
 tests=[({'images':[[4000,3000,100,100,3],[800,600,400,300,2],[300,300,100,100,3]]},['400x300px, 468 KB vs 46875 KB','800x600px, 1875 KB vs 1875 KB','300x300px, 351 KB vs 351 KB']), {'images':[]}]))
write_all(S, 'swiftui', 500)
write_all(F, 'frameworks', 700)
