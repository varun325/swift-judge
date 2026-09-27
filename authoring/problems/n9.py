import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
DOC='https://developer.apple.com/documentation/swiftui/'
SD='https://developer.apple.com/documentation/swiftdata/'
MAC=['darwin']
L = {
 1:('kCjDulwChRQ','L1: Intro to Xcode and SwiftUI'), 2:('63UHypFKRRM','L2: Code Breaker App'), 3:('B42CuI0RO7Y','L3: Model and UI & Swift Type System'),
 4:('IvOF3Bmk-94',"L4: CodeBreaker's Model"), 5:('u6cgk1W6EXE','L5: Layout & Data Flow'), 6:('tvVj6MSBhBA','L6: Demonstrating Data Flow'),
 7:('RYemrq0e7KM','L7: Animation (Generics & custom View modifiers)'), 8:('OZK7_p1G8Pw','L8: Animation Demonstration'), 9:('o3D3rqh-IVA','L9: Protocols (elapsed time)'),
 10:('NnJ91M9PRYo','L10: Building Complex UIs'), 11:('PXcl5cjVNT0','L11: iPad and Mac'), 12:('gNok5P7HLCw','L12: Even More Complex UIs'),
 13:('k9wjAdgUY0A','L13: SwiftData'), 14:('1PDZl0LPryw','L14: SwiftData Demonstration'), 15:('F0nefFT2Uik','L15: Multithreading'), 16:('skECWIKpBVY','L16: Shapes, Gestures, Persistence'),
}
def lec(*ns): return [(f'CS193p 2025 · {L[n][1]}', f'https://www.youtube.com/watch?v={L[n][0]}', 'Stanford Online') for n in ns]
P=[]
P.append(dict(id='cs193p-some-view-body', title='L1: What Is `some View`?', topic='L1–L2 · Views & modifiers', mode='predict', platforms=MAC, concepts=['opaque-types','computed-properties'], docs=[('View', DOC+'view')], videos=lec(1,2),
 statement="""CS193p L1 introduces views as Lego: `body` is a **computed property** of type `some View`. Predict the output — the concrete type behind `some View`, and how many times `body` runs.""",
 snippet="""
 import SwiftUI

 final class Counter { nonisolated(unsafe) static var calls = 0 }

 struct ContentView: View {
     var body: some View {
         Counter.calls += 1
         return VStack {
             Image(systemName: "globe")
             Text("Hello, world!")
         }
         .padding()
     }
 }

 @MainActor func show() {
     let view = ContentView()
     print(type(of: view.body))
     _ = view.body
     print(Counter.calls)
 }
 show()
 """,
 explain="""`body` is just a computed property — it runs **every time it's read**, and SwiftUI reads it whenever state changes, so keep it cheap and side-effect free. `some View` hides a precise type (here a padded VStack of a TupleView) that SwiftUI uses to diff efficiently.""",
 hints=("`body` is a computed property, not stored.","The type is built from nested generics: the modifier wraps the VStack, which wraps a TupleView.","Reading `body` twice runs it twice."),
))
P.append(dict(id='cs193p-match-count-where', title="L2: Match Markers with count(where:)", topic='L1–L2 · Views & modifiers', platforms=MAC, concepts=['enums','higher-order-functions'], docs=[('Array', 'https://developer.apple.com/documentation/swift/array')], videos=lec(2),
 sig='func markerSummary(_ matches: [String]) -> [Int]',
 statement="""CodeBreaker's markers show how good a guess was: `enum Match { case nomatch, exact, inexact }`. L2 counts them with Swift 6's `count(where:)`. Parse the strings into `Match` values (ignore unknown strings) and return `[exact count, inexact count, nomatch count]`.""",
 solution="""
 enum Match: String {
     case nomatch, exact, inexact
 }

 func markerSummary(_ matches: [String]) -> [Int] {
     let parsed = matches.compactMap(Match.init(rawValue:))
     return [
         parsed.count(where: { $0 == .exact }),
         parsed.count(where: { $0 == .inexact }),
         parsed.count(where: { $0 == .nomatch }),
     ]
 }
 """,
 explain="""`count(where:)` counts matches without building an intermediate array (unlike `filter { }.count`). Enums make the three marker states explicit — no stringly-typed checks in the view.""",
 hints=("Model the three states as an enum with `String` raw values.","`compactMap(Match.init(rawValue:))` parses and drops unknown strings.","`parsed.count(where: { $0 == .exact })`, and likewise for the others."),
 tests=[({'matches':['exact','inexact','exact','nomatch','bogus']},[2,1,1]), {'matches':[]}]))
P.append(dict(id='cs193p-mastermind-match', title='L4–L5: Scoring a Guess (Exact & Inexact)', topic='L3–L5 · Model & type system', diff='medium', platforms=MAC, concepts=['dictionary-basics','higher-order-functions','enums'], docs=[('Collection Types', 'https://docs.swift.org/swift-book/documentation/the-swift-programming-language/collectiontypes/')], videos=lec(4,5),
 sig='func score(master: [String], guesses: [[String]]) -> [String]',
 statement="""The heart of CodeBreaker's model: `func match(against master: Code) -> [Match]`. For a guess:
 - **exact** = right peg in the right position
 - **inexact** = right peg in the wrong position — but each master peg can only be matched **once** (duplicates make this tricky!)

 Implement it first with loops, then refactor with `map`/`zip` as L5 does. Return `"<exact>E <inexact>I"` for each guess. Empty strings are "missing" pegs and never match.""",
 solution="""
 func match(_ guess: [String], against master: [String]) -> (exact: Int, inexact: Int) {
     let pairs = zip(guess, master)
     let exact = pairs.count(where: { $0 == $1 && !$0.isEmpty })
     // Count remaining (non-exact) pegs of each colour on both sides; inexact = overlap.
     var masterLeft: [String: Int] = [:], guessLeft: [String: Int] = [:]
     for (g, m) in pairs where g != m || g.isEmpty {
         if !m.isEmpty { masterLeft[m, default: 0] += 1 }
         if !g.isEmpty { guessLeft[g, default: 0] += 1 }
     }
     let inexact = guessLeft.reduce(0) { $0 + min($1.value, masterLeft[$1.key] ?? 0) }
     return (exact, inexact)
 }

 func score(master: [String], guesses: [[String]]) -> [String] {
     guesses.map { guess in
         let r = match(guess, against: master)
         return "\\(r.exact)E \\(r.inexact)I"
     }
 }
 """,
 explain="""The naive "for each guess peg, is it anywhere in the master?" over-counts duplicates (guess `RRRR` against `RGBY` isn't 1 exact + 3 inexact). Removing exact pairs first and then taking `min(count in guess, count in master)` per colour is the correct rule. `zip` + `count(where:)` expresses the exact matches in one line.""",
 hints=("Count exact matches first, position by position.","For the remaining (non-exact) positions, count each colour on both sides.","Inexact = Σ over colours of `min(guessCount, masterCount)`."),
 tests=[({'master':['R','G','B','Y'],'guesses':[['R','G','B','Y'],['Y','B','G','R'],['R','R','R','R'],['G','R','','Y']]},['4E 0I','0E 4I','1E 0I','1E 2I']), {'master':['R','R','G','G'],'guesses':[['G','G','R','R'],['R','G','R','G']]}, {'master':[],'guesses':[[]]}]))
P.append(dict(id='cs193p-code-kinds', title='L3–L4: Code Kinds with Associated Data', topic='L3–L5 · Model & type system', diff='medium', platforms=MAC, concepts=['associated-values','mutating','typealias'], docs=[('Enumerations', 'https://docs.swift.org/swift-book/documentation/the-swift-programming-language/enumerations/')], videos=lec(3,4),
 sig='func codeBoard(master: [String], attempts: [[String]]) -> [String]',
 statement="""L4's model: `typealias Peg = String` (Color in the course) and `struct Code { var kind: Kind; var pegs: [Peg] }` with `enum Kind { case master(isHidden: Bool), guess, attempt([Match]), unknown }`. Build the board: the master (hidden until an attempt is fully exact), then each attempt with its matches (reuse your scoring from the previous problem: exact first, then inexact).

 Return one line per code: `"master:<pegs or ????>"` then `"attempt:<pegs> <e>E<i>I"`, and finally `"won"`/`"playing"`.""",
 solution="""
 typealias Peg = String

 enum Match { case nomatch, exact, inexact }

 struct Code {
     enum Kind {
         case master(isHidden: Bool)
         case guess
         case attempt([Match])
         case unknown
     }
     var kind: Kind
     var pegs: [Peg]

     var isHidden: Bool {
         if case .master(let hidden) = kind { return hidden }
         return false
     }

     func match(against other: Code) -> [Match] {
         let exact = zip(pegs, other.pegs).map { $0 == $1 }
         var remaining = other.pegs.enumerated().filter { !exact[$0.offset] }.map(\\.element)
         return pegs.indices.map { i in
             if exact[i] { return .exact }
             if let j = remaining.firstIndex(of: pegs[i]) { remaining.remove(at: j); return .inexact }
             return .nomatch
         }
     }
 }

 func codeBoard(master: [String], attempts: [[String]]) -> [String] {
     var masterCode = Code(kind: .master(isHidden: true), pegs: master)
     var lines: [String] = []
     var won = false
     for pegs in attempts {
         let matches = Code(kind: .guess, pegs: pegs).match(against: masterCode)
         lines.append("attempt:\\(pegs.joined()) \\(matches.count(where: { $0 == .exact }))E\\(matches.count(where: { $0 == .inexact }))I")
         if !matches.isEmpty && matches.allSatisfy({ $0 == .exact }) { won = true }
     }
     if won { masterCode.kind = .master(isHidden: false) }
     return ["master:\\(masterCode.isHidden ? String(repeating: "?", count: master.count) : master.joined())"] + lines + [won ? "won" : "playing"]
 }
 """,
 explain="""An enum with associated data models "what kind of code is this, and what extra data does each kind carry" — the master knows if it's hidden, an attempt carries its matches. `if case .master(let hidden) = kind` extracts the payload. `var kind` inside a struct can be reassigned because the model is a mutable value.""",
 hints=("Give each `Kind` case exactly the data it needs as associated values.","`if case .master(let hidden) = kind` reads the payload.","Reveal the master by assigning `masterCode.kind = .master(isHidden: false)` once an attempt is all-exact."),
 tests=[({'master':['R','G','B','Y'],'attempts':[['R','R','G','G'],['R','G','B','Y']]},['master:RGBY','attempt:RRGG 1E1I','attempt:RGBY 4E0I','won']), {'master':['R','G'],'attempts':[['G','R']]}, {'master':['A'],'attempts':[]}]))
P.append(dict(id='cs193p-tap-to-cycle', title='L4: Tap-to-Cycle Peg Selection', topic='L3–L5 · Model & type system', platforms=MAC, concepts=['mutating','optionals','nil-coalescing'], docs=[('onTapGesture(count:perform:)', DOC+'view/ontapgesture(count:perform:)')], videos=lec(4),
 sig='func cyclePegs(choices: [String], slots: Int, taps: [Int]) -> [String]',
 statement="""Before the peg chooser (L6), CodeBreaker lets you tap a slot to cycle its colour through `choices`. Slots start **missing** (`nil`). Implement `mutating func changeGuessPeg(at index: Int)` on a `Guess` struct: a missing peg becomes the first choice; otherwise it advances to the next choice, wrapping around. Taps on invalid indices are ignored. Return the guess after all taps (`"-"` for missing).""",
 solution="""
 struct Guess {
     let choices: [String]
     var pegs: [String?]

     mutating func changeGuessPeg(at index: Int) {
         guard pegs.indices.contains(index), !choices.isEmpty else { return }
         if let current = pegs[index], let i = choices.firstIndex(of: current) {
             pegs[index] = choices[(i + 1) % choices.count]
         } else {
             pegs[index] = choices.first
         }
     }
 }

 func cyclePegs(choices: [String], slots: Int, taps: [Int]) -> [String] {
     var guess = Guess(choices: choices, pegs: Array(repeating: nil, count: max(slots, 0)))
     taps.forEach { guess.changeGuessPeg(at: $0) }
     return guess.pegs.map { $0 ?? "-" }
 }
 """,
 explain="""Model methods that change the model are `mutating`; the view's `.onTapGesture { game.changeGuessPeg(at: i) }` just forwards the intent and SwiftUI re-renders because `game` is `@State`. `if let … , let …` unwraps the current peg and finds its index in one statement.""",
 hints=("A missing peg is `nil`; the first tap sets it to the first choice.","Otherwise find the current choice's index and move to `(i + 1) % count`.","Guard against invalid indices and an empty choice list."),
 tests=[{'choices':['R','G','B'],'slots':3,'taps':[0,0,0,0,2,9]}, {'choices':[],'slots':2,'taps':[0]}, {'choices':['A'],'slots':1,'taps':[0,0]}]))
P.append(dict(id='cs193p-hstack-layout', title='L5: How HStack Divides Space', topic='L5–L7 · Layout, data flow & generics', diff='hard', platforms=MAC, concepts=['sort-custom','higher-order-functions'], docs=[('Layout', DOC+'layout'), ('layoutPriority(_:)', DOC+'view/layoutpriority(_:)')], videos=lec(5),
 sig='func layoutWidths(available: Double, children: [[Double]]) -> [Double]',
 statement="""L5's layout rule: a container **offers** space, each child **chooses** its size, then the container positions them — and an HStack offers space to its **least flexible** children first. Model it: each child is `[minWidth, maxWidth, priority]`.
 1. Every child first gets its `minWidth`; the leftover is `available − Σ min` (if negative, children just get their minimums).
 2. Hand out leftover by `priority` group, **highest first**. Within a group, go from least flexible (smallest `max − min`) to most; each child is offered `leftover ÷ childrenRemainingInGroup` and takes `min(offer, max − min)` extra.
 Return widths in the original order, rounded to 2 decimals.""",
 compare='float:1e-9',
 solution="""
 func layoutWidths(available: Double, children: [[Double]]) -> [Double] {
     var widths = children.map { $0[0] }
     var leftover = max(0, available - widths.reduce(0, +))
     let priorities = Set(children.map { $0[2] }).sorted(by: >)
     for priority in priorities {
         var group = children.indices.filter { children[$0][2] == priority }
         group.sort { (children[$0][1] - children[$0][0]) < (children[$1][1] - children[$1][0]) }
         for (k, i) in group.enumerated() {
             let offer = leftover / Double(group.count - k)
             let extra = min(offer, children[i][1] - children[i][0])
             widths[i] += extra
             leftover -= extra
         }
     }
     return widths.map { ($0 * 100).rounded() / 100 }
 }
 """,
 explain="""Offering to the least flexible children first means a `Text` gets what it needs before a stretchy `Rectangle` or `Spacer` soaks up the rest; `layoutPriority` changes the order. That's why a long label can squeeze an image, and why `.layoutPriority(1)` on the important view fixes truncation. (This is a simplified model of SwiftUI's real algorithm.)""",
 hints=("Everyone gets their minimum first; only the leftover is negotiated.","Process priority groups from high to low; inside a group, least flexible first.","Each child's offer is `leftover / remainingInGroup`; it takes at most `max − min`."),
 tests=[({'available':300,'children':[[50,120,0],[20,1000,0],[80,80,0]]},[120,100,80]), {'available':100,'children':[[60,60,0],[60,60,0]]}, {'available':400,'children':[[10,500,0],[10,500,1]]}, {'available':50,'children':[]}]))
P.append(dict(id='cs193p-functional-refactor', title='L5: From For-Loops to map & Captured Locals', topic='L5–L7 · Layout, data flow & generics', mode='predict', platforms=MAC, concepts=['closures','capturing-values','map-filter-reduce'], docs=[('Closures', 'https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/')], videos=lec(5),
 statement="""L5 refactors loops into `map` and shows closures **capturing local variables**. Predict the output — especially the value `bonus` has when each closure actually runs.""",
 snippet="""
 var bonus = 1
 let pegs = ["R", "G", "B"]
 let labels = pegs.map { peg in "\\(peg)\\(bonus)" }
 bonus = 10
 let makers = pegs.map { peg in { "\\(peg)\\(bonus)" } }
 bonus = 100
 print(labels)
 print(makers.map { $0() })
 let indexed = pegs.enumerated().map { i, peg in i.isMultiple(of: 2) ? peg.lowercased() : peg }
 print(indexed)
 """,
 explain="""`map`'s closure runs **immediately**, so `labels` captured `bonus` at 1. The inner closures in `makers` capture the **variable** `bonus` and only run later, when it's 100. `enumerated()` gives `(offset, element)` tuples a closure can destructure.""",
 hints=("`map` runs its closure right away; the closures it *returns* run later.","Captured variables are read when the closure runs, not when it's created.","The second line prints `[\"R100\", \"G100\", \"B100\"]`.")))
P.append(dict(id='cs193p-color-gray-extension', title='L6: Extending Color & CGFloat vs Double', topic='L5–L7 · Layout, data flow & generics', platforms=MAC, concepts=['extensions','fundamental-types','float-vs-double'], docs=[('Color', DOC+'color'), ('CGFloat', 'https://developer.apple.com/documentation/corefoundation/cgfloat')], videos=lec(6),
 sig='func grays(_ levels: [Double]) async -> [String]',
 statement="""L6 adds `static func gray(_ brightness: CGFloat) -> Color` in an `extension Color` (drawing APIs take `CGFloat`; general math uses `Double`). Implement it (clamp brightness to 0…1, equal RGB), resolve each colour with `resolve(in: EnvironmentValues())`, and return `"<r>,<g>,<b>"` as 0–255 integers.""",
 solution="""
 import SwiftUI

 extension Color {
     static func gray(_ brightness: CGFloat) -> Color {
         let b = Double(min(max(brightness, 0), 1))
         return Color(.sRGB, red: b, green: b, blue: b)
     }
 }

 @MainActor func components(_ color: Color) -> String {
     let r = color.resolve(in: EnvironmentValues())
     return [r.red, r.green, r.blue].map { String(Int(($0 * 255).rounded())) }.joined(separator: ",")
 }

 func grays(_ levels: [Double]) async -> [String] {
     var out: [String] = []
     for level in levels { out.append(await components(.gray(CGFloat(level)))) }
     return out
 }
 """,
 explain="""A static method in an extension reads like a built-in colour: `.gray(0.5)`. `CGFloat` is the Core Graphics float type (a `Double` on 64-bit), and Swift requires explicit conversion between the two — which is why drawing code is full of `CGFloat(…)`.""",
 hints=("Add `static func gray(_ brightness: CGFloat) -> Color` in `extension Color`.","Clamp, convert to `Double`, and use the same value for red, green and blue.","Resolve and scale each component by 255."),
 tests=[({'levels':[0,0.5,1,2]},['0,0,0','128,128,128','255,255,255','255,255,255']), {'levels':[]}]))
P.append(dict(id='cs193p-generic-code-view', title='L7: Generic Views with @ViewBuilder', topic='L5–L7 · Layout, data flow & generics', mode='predict', diff='medium', platforms=MAC, concepts=['generics','generic-constraints','result-builders','escaping'], docs=[('ViewBuilder', DOC+'viewbuilder')], videos=lec(7),
 statement="""L7 refactors `CodeView` to accept **any** ancillary view (match markers or a guess button) via a generic `AncillaryView: View` with a `@ViewBuilder` init, plus an `@escaping` action. Predict the concrete types and the action output.""",
 snippet="""
 import SwiftUI

 struct CodeView<AncillaryView: View>: View {
     let pegs: [String]
     let onTap: () -> String
     @ViewBuilder let ancillaryView: () -> AncillaryView

     init(pegs: [String], onTap: @escaping () -> String = { "none" }, @ViewBuilder ancillaryView: @escaping () -> AncillaryView) {
         self.pegs = pegs
         self.onTap = onTap
         self.ancillaryView = ancillaryView
     }

     var body: some View {
         HStack { ForEach(pegs, id: \\.self) { Text($0) }; ancillaryView() }
     }
 }

 @MainActor func show() {
     let markers = CodeView(pegs: ["R", "G"]) { Text("2E 0I") }
     let button = CodeView(pegs: ["B"], onTap: { "guessed!" }) { Button("Guess") {} }
     let empty = CodeView(pegs: []) { EmptyView() }
     print(type(of: markers))
     print(type(of: button))
     print(type(of: empty), markers.onTap(), button.onTap())
 }
 show()
 """,
 explain="""Generics let one `CodeView` wrap different ancillary views while keeping full type information — each use is a **different type** (`CodeView<Text>`, `CodeView<Button<Text>>`). `@ViewBuilder` on the closure parameter lets callers write view-builder syntax; `@escaping` is needed because the closure is stored.""",
 hints=("Each call site specialises the generic with a different concrete view type.","`Button(\"Guess\") {}` is a `Button<Text>`.","The default `onTap` returns `\"none\"`.")))
P.append(dict(id='cs193p-hide-master-code', title='L8: Game Over Rules & Not Leaking Secrets', topic='L8–L9 · Animation & time', diff='medium', platforms=MAC, concepts=['enums','higher-order-functions'], docs=[('withAnimation(_:_:)', DOC+'withanimation(_:_:)'), ('Transaction', DOC+'transaction')], videos=lec(8),
 sig='func playRound(master: [String], guesses: [[String]], maxAttempts: Int) -> [String]',
 statement="""L8 adds restart and warns about **animation revealing hidden state** (e.g. the master code flashing during a transition). The model decides visibility: implement `CodeBreaker` with `attempt(_:)`, `isOver` (solved or out of attempts), `restart()` and `masterDisplay` (`"????"`-style while playing; the real pegs once over). Guesses of the wrong length or already tried are rejected.

 Process guesses (`"restart"` restarts); after each, log `"<attempts> <masterDisplay> <playing|solved|lost|rejected>"`.""",
 solution="""
 struct CodeBreaker {
     let master: [String]
     let maxAttempts: Int
     private(set) var attempts: [[String]] = []

     var isSolved: Bool { attempts.last == master }
     var isOver: Bool { isSolved || attempts.count >= maxAttempts }
     var masterDisplay: String { isOver ? master.joined() : String(repeating: "?", count: master.count) }

     mutating func attempt(_ guess: [String]) -> Bool {
         guard !isOver, guess.count == master.count, !attempts.contains(guess) else { return false }
         attempts.append(guess)
         return true
     }

     mutating func restart() { attempts = [] }
 }

 func playRound(master: [String], guesses: [[String]], maxAttempts: Int) -> [String] {
     var game = CodeBreaker(master: master, maxAttempts: maxAttempts)
     return guesses.map { g in
         var status: String
         if g == ["restart"] {
             game.restart()
             status = "playing"
         } else if !game.attempt(g) {
             status = "rejected"
         } else {
             status = game.isSolved ? "solved" : game.isOver ? "lost" : "playing"
         }
         return "\\(game.attempts.count) \\(game.masterDisplay) \\(status)"
     }
 }
 """,
 explain="""Secrets belong behind **model** rules, not just view styling: if the view merely hides the master with `.opacity(0)`, an animation (or accessibility) can still expose it. Computed properties like `isOver` and `masterDisplay` derive state instead of storing flags that can drift out of sync.""",
 hints=("Derive `isSolved`, `isOver` and `masterDisplay` from the attempts — don't store flags.","Reject guesses when the game is over, the length is wrong, or it was already tried.","`restart()` clears the attempts; the master is hidden again automatically."),
 tests=[({'master':['R','G','B','Y'],'guesses':[['R','R','G','G'],['R','R','G','G'],['R','G'],['R','G','B','Y'],['Y','Y','Y','Y'],['restart']],'maxAttempts':5},['1 ???? playing','1 ???? rejected','1 ???? rejected','2 RGBY solved','2 RGBY rejected','0 ???? playing']), {'master':['A','B'],'guesses':[['B','A'],['A','A']],'maxAttempts':2}]))
P.append(dict(id='cs193p-elapsed-time', title='L9: Elapsed Time with Pause & Resume', topic='L8–L9 · Animation & time', diff='medium', platforms=MAC, concepts=['optionals','computed-properties'], docs=[('Text init(_:style:)', DOC+'text/init(_:style:)'), ('Date', 'https://developer.apple.com/documentation/foundation/date')], videos=lec(9),
 sig='func elapsed(_ events: [[String]]) -> [String]',
 statement="""L9 tracks how long a game has been played, pausing when the app leaves the screen. Store `elapsedBeforePause: TimeInterval` and `startTime: Date?` (non-nil while running). Events are `[action, secondsSinceReference]` with actions `start`, `pause`, `check`. `elapsed(at:)` = stored time + (now − start) when running. Log `check` results as `"m:ss"` (what `Text(.offset)`-style formatting shows).""",
 solution="""
 import Foundation

 struct GameClock {
     private(set) var elapsedBeforePause: TimeInterval = 0
     private(set) var startTime: Date?

     mutating func start(at now: Date) { if startTime == nil { startTime = now } }

     mutating func pause(at now: Date) {
         guard let start = startTime else { return }
         elapsedBeforePause += now.timeIntervalSince(start)
         startTime = nil
     }

     func elapsed(at now: Date) -> TimeInterval {
         elapsedBeforePause + (startTime.map { now.timeIntervalSince($0) } ?? 0)
     }
 }

 func elapsed(_ events: [[String]]) -> [String] {
     var clock = GameClock()
     var out: [String] = []
     let reference = Date(timeIntervalSinceReferenceDate: 0)
     for e in events {
         let now = reference.addingTimeInterval(Double(e[1]) ?? 0)
         switch e[0] {
         case "start": clock.start(at: now)
         case "pause": clock.pause(at: now)
         default:
             let total = Int(clock.elapsed(at: now))
             out.append("\\(total / 60):\\(total % 60 < 10 ? "0" : "")\\(total % 60)")
         }
     }
     return out
 }
 """,
 explain="""Store a **start time**, not a ticking counter: elapsed time is computed from dates, so it's correct even if the app is suspended and nothing ran. SwiftUI's `Text(startDate, style: .timer)` renders a live timer from a date without re-running `body` every second.""",
 hints=("Keep accumulated time plus an optional start date.","Pausing adds `now − start` to the accumulator and clears the start.","Elapsed = accumulated + (now − start) while running."),
 tests=[({'events':[['start','0'],['check','65'],['pause','70'],['check','500'],['start','600'],['check','610']]},['1:05','1:10','1:20']), {'events':[['check','9']]}, {'events':[['pause','5'],['start','5'],['start','20'],['check','35']]}]))
P.append(dict(id='cs193p-foreach-identity', title='L10: The Three Rules for ForEach Identity', topic='L10–L12 · Complex UIs', diff='medium', platforms=MAC, concepts=['equatable-hashable','protocols','set-vs-array'], docs=[('ForEach', DOC+'foreach'), ('Identifiable', 'https://developer.apple.com/documentation/swift/identifiable')], videos=lec(10),
 sig='func checkIdentities(_ snapshots: [[String]]) -> [String]',
 statement="""L10: a `ForEach` identifier must be **unique**, **stable** (the same item keeps the same id across updates) and **Hashable**. Each snapshot is a list of `"<id>:<content>"` items, representing the list at successive moments. Report problems:
 - `"duplicate <id> in snapshot <n>"` for repeated ids within a snapshot
 - `"unstable <content>"` when the same content appears with a **different** id in a later snapshot (e.g. using array indices as ids)

 Return the problems sorted, or `["ok"]`.""",
 solution="""
 func checkIdentities(_ snapshots: [[String]]) -> [String] {
     var problems: Set<String> = []
     var idForContent: [String: String] = [:]
     for (n, snapshot) in snapshots.enumerated() {
         var seen: Set<String> = []
         for item in snapshot {
             let parts = item.split(separator: ":", maxSplits: 1).map(String.init)
             guard parts.count == 2 else { continue }
             let (id, content) = (parts[0], parts[1])
             if !seen.insert(id).inserted { problems.insert("duplicate \\(id) in snapshot \\(n)") }
             if let previous = idForContent[content], previous != id { problems.insert("unstable \\(content)") }
             idForContent[content] = id
         }
     }
     return problems.isEmpty ? ["ok"] : problems.sorted()
 }
 """,
 explain="""Using array **indices** as ids fails stability: delete item 0 and every other item's id shifts, so SwiftUI animates the wrong rows and loses their state. Give models a real identity (`Identifiable` with a stored `UUID` or database id) — exactly React's rule for `key`.""",
 hints=("Uniqueness is per snapshot; stability is across snapshots.","Track the last id each content had; a different id later means instability.","Use a `Set` to detect duplicates within a snapshot."),
 tests=[({'snapshots':[['0:apple','1:pear'],['0:pear']]},['unstable pear']), {'snapshots':[['a:x','a:y']]}, {'snapshots':[['u1:x','u2:y'],['u2:y']]}, {'snapshots':[]}]))
P.append(dict(id='cs193p-game-chooser', title='L10: Game Chooser with Custom Identity', topic='L10–L12 · Complex UIs', diff='medium', platforms=MAC, concepts=['equatable-hashable','protocols','identifiable-dedupe' if False else 'protocols'], docs=[('List', DOC+'list'), ('Hashable', 'https://developer.apple.com/documentation/swift/hashable')], videos=lec(10),
 sig='func chooser(_ ops: [String]) -> [String]',
 statement="""L10's `GameChooser` lists named games with themes (Mastermind, Earth Tones, Undersea). Make `struct GameSummary: Identifiable, Hashable` whose **identity is its `id: UUID`**, but whose `Hashable`/`==` conformance is **manual** and compares only `id` (so renaming doesn't change identity). Ops: `add <name> <theme>`, `rename <old> <new>`, `select <name>`, `remove <name>`. The selection is stored as the game's `id`; removing the selected game clears it. Log `"<names joined by ,> | selected: <name or none>"` after each op.""",
 solution="""
 import Foundation

 struct GameSummary: Identifiable, Hashable {
     let id = UUID()
     var name: String
     var theme: String

     static func == (a: GameSummary, b: GameSummary) -> Bool { a.id == b.id }
     func hash(into hasher: inout Hasher) { hasher.combine(id) }
 }

 func chooser(_ ops: [String]) -> [String] {
     var games: [GameSummary] = []
     var selection: GameSummary.ID?
     return ops.map { op in
         let p = op.split(separator: " ").map(String.init)
         func index(_ name: String) -> Int? { games.firstIndex { $0.name == name } }
         switch (p.first ?? "", p.count) {
         case ("add", 3): games.append(GameSummary(name: p[1], theme: p[2]))
         case ("rename", 3): if let i = index(p[1]) { games[i].name = p[2] }
         case ("select", 2): selection = index(p[1]).map { games[$0].id }
         case ("remove", 2):
             if let i = index(p[1]) {
                 if games[i].id == selection { selection = nil }
                 games.remove(at: i)
             }
         default: break
         }
         let selectedName = games.first { $0.id == selection }?.name ?? "none"
         return "\\(games.map(\\.name).joined(separator: ",")) | selected: \\(selectedName)"
     }
 }
 """,
 explain="""Selecting by `id` (not by index or by the whole value) keeps the selection correct across renames and reorders — `List(selection:)` binds to exactly this. A manual `Hashable` that hashes only the id makes equality mean "same game", which is what SwiftUI needs for stable identity.""",
 hints=("Store the selection as the game's `id`, not its index or name.","Implement `==` and `hash(into:)` using only `id`.","Renaming mutates the element in place, so the selection still points to it."),
 tests=[({'ops':['add Mastermind classic','add Undersea ocean','select Undersea','rename Undersea Deep','remove Mastermind','remove Deep']},['Mastermind | selected: none','Mastermind,Undersea | selected: none','Mastermind,Undersea | selected: Undersea','Mastermind,Deep | selected: Deep','Deep | selected: Deep',' | selected: none']), {'ops':[]}]))
P.append(dict(id='cs193p-split-view-columns', title='L11: NavigationSplitView & Size Classes', topic='L10–L12 · Complex UIs', platforms=MAC, concepts=['enums','optionals','switch-statement'], docs=[('NavigationSplitView', DOC+'navigationsplitview'), ('UserInterfaceSizeClass', DOC+'userinterfacesizeclass')], videos=lec(11),
 sig='func visibleColumns(_ states: [[String]]) -> [String]',
 statement="""L11 makes CodeBreaker adaptive. A two-column `NavigationSplitView` behaves differently by **horizontal size class**: in `regular` width (iPad, Mac) both columns show side by side; in `compact` width (iPhone) it collapses into a stack showing the list **or** the detail. Each state is `[sizeClass, selectedGame or "-", columnVisibility]` with visibility `all`, `detailOnly` or `automatic`.

 Return what's on screen: `"list+detail(<game or placeholder>)"`, `"list"`, or `"detail(<game>)"`. In compact width: a selection shows its detail, otherwise the list. In regular width: `detailOnly` hides the list; otherwise both show (placeholder text `"Choose a game"` when nothing is selected).""",
 solution="""
 func visibleColumns(_ states: [[String]]) -> [String] {
     states.map { s in
         let selection: String? = s[1] == "-" ? nil : s[1]
         if s[0] == "compact" {
             return selection.map { "detail(\\($0))" } ?? "list"
         }
         if s[2] == "detailOnly", let selection { return "detail(\\(selection))" }
         return "list+detail(\\(selection ?? "Choose a game"))"
     }
 }
 """,
 explain="""Adaptive UIs react to **size classes**, not device models — an iPad in Split View can be compact. `NavigationSplitView` handles the collapse automatically; your job is to supply a sensible detail placeholder and to bind column visibility when you want to control it.""",
 hints=("Compact width shows one column at a time; regular width can show both.","In compact, the selection decides list vs detail.","In regular, `detailOnly` with a selection hides the list; otherwise show both with a placeholder."),
 tests=[({'states':[['compact','-','automatic'],['compact','Undersea','automatic'],['regular','-','all'],['regular','Mastermind','detailOnly'],['regular','-','detailOnly']]},['list','detail(Undersea)','list+detail(Choose a game)','detail(Mastermind)','list+detail(Choose a game)']), {'states':[]}]))
P.append(dict(id='cs193p-peg-choices-editor', title='L12: @Bindable Editor for Create & Edit', topic='L10–L12 · Complex UIs', diff='medium', platforms=MAC, concepts=['property-wrappers','optionals','dependency-injection'], docs=[('Bindable', DOC+'bindable'), ('sheet(isPresented:onDismiss:content:)', DOC+'view/sheet(ispresented:ondismiss:content:)')], videos=lec(12),
 sig='func editGames(_ actions: [String]) -> [String]',
 statement="""L12 builds one sheet that both **creates** a new game and **edits** an existing one, binding to an `@Observable` game with `@Bindable`. Model `@Observable final class GameConfig { var name; var pegChoices: [String] }` with rules: 2…6 choices, no duplicates, name non-empty. The editor works on a **draft copy**; `save` validates and either appends (create) or writes back (edit); `cancel` discards.

 Actions: `new`, `edit <name>`, `name <n>`, `addPeg <c>`, `removePeg <c>`, `save`, `cancel`. Log after `save` (`"saved"` or `"invalid: <reason>"`) and at the end list games as `"<name>(<pegs>)"`.""",
 solution="""
 import Observation

 @Observable
 final class GameConfig {
     var name: String
     var pegChoices: [String]
     init(name: String, pegChoices: [String]) {
         self.name = name
         self.pegChoices = pegChoices
     }
     func copy() -> GameConfig { GameConfig(name: name, pegChoices: pegChoices) }

     var validationError: String? {
         if name.isEmpty { return "name" }
         if !(2...6).contains(pegChoices.count) { return "peg count" }
         if Set(pegChoices).count != pegChoices.count { return "duplicates" }
         return nil
     }
 }

 func editGames(_ actions: [String]) -> [String] {
     var games = [GameConfig(name: "Mastermind", pegChoices: ["R", "G", "B", "Y"])]
     var draft: GameConfig?
     var editing: GameConfig?
     var log: [String] = []
     for action in actions {
         let p = action.split(separator: " ", maxSplits: 1).map(String.init)
         let arg = p.count > 1 ? p[1] : ""
         switch p[0] {
         case "new": editing = nil; draft = GameConfig(name: "", pegChoices: [])
         case "edit": editing = games.first { $0.name == arg }; draft = editing?.copy()
         case "name": draft?.name = arg
         case "addPeg": draft?.pegChoices.append(arg)
         case "removePeg": if let i = draft?.pegChoices.firstIndex(of: arg) { draft?.pegChoices.remove(at: i) }
         case "cancel": draft = nil; editing = nil
         case "save":
             guard let d = draft else { break }
             if let error = d.validationError { log.append("invalid: \\(error)"); break }
             if let original = editing {
                 original.name = d.name
                 original.pegChoices = d.pegChoices
             } else {
                 games.append(d)
             }
             log.append("saved")
             draft = nil
             editing = nil
         default: break
         }
     }
     return log + games.map { "\\($0.name)(\\($0.pegChoices.joined()))" }
 }
 """,
 explain="""`@Bindable var game: GameConfig` gives `$game.name` bindings into an `@Observable` class. Editing a **draft copy** makes Cancel trivial and keeps half-edited data out of the model. The same sheet serves create and edit by passing an optional original.""",
 hints=("Edit a draft copy; only `save` touches the real list.","Validation is a computed property returning the first problem or nil.","`save` appends for a new game, or writes the draft's fields back for an edit."),
 tests=[{'actions':['new','name Earth','addPeg T','save','addPeg G','addPeg T','save','removePeg T','addPeg B','save','edit Mastermind','removePeg Y','cancel']}, {'actions':[]}, {'actions':['edit Mastermind','name ','save','name Classic','save']}]))
P.append(dict(id='cs193p-swiftdata-model', title='L13: Converting the Model to SwiftData', topic='L13–L15 · SwiftData & threads', diff='hard', platforms=MAC, concepts=['codable','class-definition','property-wrappers'], docs=[('Model()', SD+'model()'), ('Transient()', SD+'transient()')], videos=lec(13),
 sig='func persistGames(_ ops: [String]) async -> [String]',
 statement="""L13 turns CodeBreaker's structs into `@Model` classes. Rules shown in class: stored vars must be primitives, other `@Model`s, or `Codable` values; UI-only state is `@Transient`; relationships use `@Relationship`. Model `@Model final class GameRecord { var name: String; var pegChoices: [String] (Codable array); var lastAttempt: Date?; @Transient var isSelected = false; @Relationship(deleteRule: .cascade) var attempts: [AttemptRecord] }` and `@Model final class AttemptRecord { var pegs: [String]; var at: Date }`.

 Ops: `game <name> <pegs>`, `attempt <name> <pegs> <day>` (sets `lastAttempt`), `select <name>`, `delete <name>`. Finally fetch games sorted by `lastAttempt` descending (nil last) then name, and log `"<name>: <attempts> attempts, last <day|never>, selected <Bool>"` — using a **fresh context** so you can see `@Transient` isn't persisted.""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class AttemptRecord {
     var pegs: [String]
     var at: Date
     init(pegs: [String], at: Date) { self.pegs = pegs; self.at = at }
 }

 @Model
 final class GameRecord {
     var name: String
     var pegChoices: [String]
     var lastAttempt: Date?
     @Transient var isSelected = false
     @Relationship(deleteRule: .cascade) var attempts: [AttemptRecord] = []
     init(name: String, pegChoices: [String]) { self.name = name; self.pegChoices = pegChoices }
 }

 @MainActor func run(_ ops: [String]) throws -> [String] {
     let container = try ModelContainer(for: GameRecord.self, AttemptRecord.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     func game(_ name: String) throws -> GameRecord? {
         try context.fetch(FetchDescriptor<GameRecord>(predicate: #Predicate { $0.name == name })).first
     }
     for op in ops {
         let p = op.split(separator: " ").map(String.init)
         switch (p.first ?? "", p.count) {
         case ("game", 3): context.insert(GameRecord(name: p[1], pegChoices: p[2].map(String.init)))
         case ("attempt", 4):
             guard let g = try game(p[1]) else { break }
             let at = Date(timeIntervalSinceReferenceDate: (Double(p[3]) ?? 0) * 86_400)
             g.attempts.append(AttemptRecord(pegs: p[2].map(String.init), at: at))
             g.lastAttempt = at
         case ("select", 2): try game(p[1])?.isSelected = true
         case ("delete", 2): if let g = try game(p[1]) { context.delete(g) }
         default: break
         }
     }
     try context.save()
     let fresh = ModelContext(container)
     let games = try fresh.fetch(FetchDescriptor<GameRecord>(sortBy: [SortDescriptor(\\.name)]))
         .sorted { ($0.lastAttempt ?? .distantPast, $1.name) > ($1.lastAttempt ?? .distantPast, $0.name) }
     return games.map { g in
         let day = g.lastAttempt.map { String(Int($0.timeIntervalSinceReferenceDate / 86_400)) } ?? "never"
         return "\\(g.name): \\(g.attempts.count) attempts, last \\(day), selected \\(g.isSelected)"
     }
 }

 func persistGames(_ ops: [String]) async -> [String] {
     (try? await run(ops)) ?? ["error"]
 }
 """,
 explain="""`@Model` classes persist stored properties automatically (arrays of `Codable` values included); `@Transient` opts UI-only state out, so a fresh context sees its default. Sorting by an **optional** date happens in Swift here because "nil last" isn't expressible in every predicate/sort — L15 discusses these query limits. Cascade delete removes a game's attempts.""",
 hints=("Mark UI-only state `@Transient`; persisted arrays of strings are fine.","Append attempts to the relationship and set `lastAttempt`.","Read back through a new `ModelContext(container)` to see what was actually stored."),
 tests=[({'ops':['game Mastermind RGBY','game Undersea ABCD','attempt Mastermind RRGG 3','attempt Mastermind RGBY 5','select Mastermind','game Earth TGBR','delete Earth']},['Mastermind: 2 attempts, last 5, selected false','Undersea: 0 attempts, last never, selected false']), {'ops':[]}]))
P.append(dict(id='cs193p-swiftdata-queries', title='L14–L15: Predicates Across Relationships', topic='L13–L15 · SwiftData & threads', diff='hard', platforms=MAC, concepts=['closures','higher-order-functions'], docs=[('Predicate', 'https://developer.apple.com/documentation/foundation/predicate'), ('FetchDescriptor', SD+'fetchdescriptor')], videos=lec(14,15),
 sig='func gameQueries(_ games: [[String]]) async -> [String]',
 statement="""L14–L15 write predicates that traverse relationships and hit query limits ("no computed vars in predicates"). Each game is `[name, isComplete "y"/"n", attempts as comma-separated counts of exact matches]`. Store `@Model Game { name, isComplete, attempts: [Attempt] }` with `@Model Attempt { exact: Int }`, then run:
 1. completed games (`#Predicate { $0.isComplete }`), sorted by name
 2. games with **any** attempt having `exact >= 3` — `#Predicate { $0.attempts.contains { $0.exact >= 3 } }`
 3. games with at most 2 attempts — `$0.attempts.count <= 2`

 Return the three lists, names joined by `,`.""",
 solution="""
 import SwiftData
 import Foundation

 @Model
 final class Attempt {
     var exact: Int
     init(exact: Int) { self.exact = exact }
 }

 @Model
 final class Game {
     var name: String
     var isComplete: Bool
     @Relationship(deleteRule: .cascade) var attempts: [Attempt] = []
     init(name: String, isComplete: Bool) { self.name = name; self.isComplete = isComplete }
 }

 @MainActor func run(_ specs: [[String]]) throws -> [String] {
     let container = try ModelContainer(for: Game.self, Attempt.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
     let context = container.mainContext
     for s in specs {
         let g = Game(name: s[0], isComplete: s[1] == "y")
         context.insert(g)
         g.attempts = s[2].split(separator: ",").compactMap { Int($0) }.map { Attempt(exact: $0) }
     }
     try context.save()
     let byName = [SortDescriptor(\\Game.name)]
     let completed = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.isComplete }, sortBy: byName))
     let close = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.attempts.contains { $0.exact >= 3 } }, sortBy: byName))
     let quick = try context.fetch(FetchDescriptor<Game>(predicate: #Predicate { $0.attempts.count <= 2 }, sortBy: byName))
     return [completed, close, quick].map { $0.map(\\.name).joined(separator: ",") }
 }

 func gameQueries(_ games: [[String]]) async -> [String] {
     (try? await run(games)) ?? ["error"]
 }
 """,
 explain="""`#Predicate` can traverse relationships (`attempts.contains { … }`, `attempts.count`) and SwiftData translates it into a SQL join. It **can't** call computed properties or arbitrary functions — they don't exist in the database — so store what you need to query (e.g. `isComplete`) as a real property.""",
 hints=("Store queryable facts (`isComplete`) as stored properties.","Relationship predicates: `$0.attempts.contains { $0.exact >= 3 }`.","`$0.attempts.count <= 2` counts the related rows."),
 tests=[({'games':[['Mastermind','y','1,2,4'],['Undersea','n','0,1'],['Earth','y','3'],['Blank','n','']]},['Earth,Mastermind','Earth,Mastermind','Blank,Earth,Undersea']), {'games':[]}]))
P.append(dict(id='cs193p-mainactor-background', title='L15: Heavy Work Off the Main Actor', topic='L13–L15 · SwiftData & threads', diff='hard', platforms=MAC, concepts=['actors','async-await','sendable'], docs=[('MainActor', 'https://developer.apple.com/documentation/swift/mainactor'), ('Concurrency', 'https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/')], videos=lec(15),
 sig='func solverDemo(master: [String], choices: [String]) async -> [String]',
 statement="""L15: the UI (and the view model) live on the **main actor**; long work must not block it. A `@MainActor @Observable final class HintModel` has `status` and `func findHint()`, which awaits a **nonisolated async** solver that brute-forces how many possible codes (all length-`master.count` sequences over `choices`) would produce the same score as a fixed probe guess (the first choice repeated). The solver runs off the main actor; the model updates `status` on the main actor.

 Return the statuses the model went through (`idle`, `thinking`, `<n> candidates`) plus `"main thread during solve: <Bool>"`, recorded by the solver via `Thread.isMainThread`.""",
 solution="""
 import Foundation
 import Observation

 struct Solver {
     /// Runs on the cooperative thread pool (nonisolated), not on the main actor.
     /// `Thread.isMainThread` is unavailable directly in async code (Swift 6), so ask from a sync helper.
     static func onMainThread() -> Bool { Thread.isMainThread }

     @concurrent
     static func candidates(master: [String], choices: [String]) async -> (count: Int, onMain: Bool) {
         let onMain = onMainThread()
         guard let probePeg = choices.first, !master.isEmpty else { return (0, onMain) }
         let probe = Array(repeating: probePeg, count: master.count)
         func score(_ code: [String], _ guess: [String]) -> Int { zip(code, guess).count(where: ==) }
         let target = score(master, probe)
         var codes: [[String]] = [[]]
         for _ in master { codes = codes.flatMap { c in choices.map { c + [$0] } } }
         return (codes.count(where: { score($0, probe) == target }), onMain)
     }
 }

 @MainActor
 @Observable
 final class HintModel {
     private(set) var statuses = ["idle"]
     private(set) var solvedOnMain = true

     func findHint(master: [String], choices: [String]) async {
         statuses.append("thinking")
         let result = await Solver.candidates(master: master, choices: choices)
         solvedOnMain = result.onMain
         statuses.append("\\(result.count) candidates")
     }
 }

 func solverDemo(master: [String], choices: [String]) async -> [String] {
     let model = await HintModel()
     await model.findHint(master: master, choices: choices)
     return await model.statuses + ["main thread during solve: \\(await model.solvedOnMain)"]
 }
 """,
 explain="""`@MainActor` state updates stay on the main thread, while `@concurrent` (Swift 6.2) guarantees the async solver runs on the global executor — the UI stays responsive during the brute force. `await` is the hop point both ways. Before 6.2, a plain `nonisolated async` function did the same by default. Note Swift 6 forbids `Thread.isMainThread` directly inside `async` code — threads aren't a meaningful concept there (a task may hop threads at every `await`); isolation is what you reason about. A synchronous helper is fine for a diagnostic like this.""",
 hints=("Keep UI state on `@MainActor`; mark the heavy async function `@concurrent` (or nonisolated). (`Thread.isMainThread` can't be used directly in async code — wrap it in a sync function.)","Await the solver from the model and update `statuses` afterwards.","Record `Thread.isMainThread` inside the solver to prove where it ran."),
 tests=[({'master':['R','G','B'],'choices':['R','G','B']},['idle','thinking','12 candidates','main thread during solve: false']), {'master':[],'choices':['R']}]))
P.append(dict(id='cs193p-custom-shape-fit', title='L16: Custom Shapes & Fitting with Geometry', topic='L16 · Shapes, gestures, persistence', diff='medium', platforms=MAC, concepts=['protocols','fundamental-types'], docs=[('Shape', DOC+'shape'), ('GeometryReader', DOC+'geometryreader')], videos=lec(16),
 sig='func pegLayout(width: Double, height: Double, count: Int, spacing: Double) async -> [String]',
 statement="""L16 builds custom Shapes and uses `GeometryReader` to size things. Given the space a `GeometryReader` reports (`width × height`), lay out `count` circular pegs in one row with `spacing` between them: diameter = `min(height, (width − spacing × (count − 1)) / count)`, clamped at ≥ 0. Draw them with a custom `struct PegRow: Shape` (a `Path` of `addEllipse` circles, vertically centred) and return `["diameter <d>", "bounds <x>,<y>,<w>,<h>"]` of the path (2 decimals), or `["empty"]` when nothing is drawn.""",
 solution="""
 import SwiftUI

 struct PegRow: Shape {
     let count: Int
     let spacing: Double

     func diameter(in rect: CGRect) -> Double {
         guard count > 0 else { return 0 }
         return max(0, min(rect.height, (rect.width - spacing * Double(count - 1)) / Double(count)))
     }

     func path(in rect: CGRect) -> Path {
         var path = Path()
         let d = diameter(in: rect)
         guard d > 0 else { return path }
         for i in 0..<count {
             let x = rect.minX + Double(i) * (d + spacing)
             path.addEllipse(in: CGRect(x: x, y: rect.midY - d / 2, width: d, height: d))
         }
         return path
     }
 }

 func pegLayout(width: Double, height: Double, count: Int, spacing: Double) async -> [String] {
     let rect = CGRect(x: 0, y: 0, width: width, height: height)
     let row = PegRow(count: count, spacing: spacing)
     let path = row.path(in: rect)
     guard !path.isEmpty else { return ["empty"] }
     let b = path.boundingRect
     let r = { (v: Double) in String((v * 100).rounded() / 100) }
     return ["diameter \\(r(row.diameter(in: rect)))", "bounds \\([b.minX, b.minY, b.width, b.height].map(r).joined(separator: ","))"]
 }
 """,
 explain="""A `Shape` draws itself for whatever rect it's given, so the same `PegRow` works at any size; `GeometryReader` (or a `Layout`) tells you that size. Choosing the diameter as the smaller of "fits the height" and "fits the width after spacing" keeps pegs circular.""",
 hints=("The diameter must fit both the height and the width left after spacing.","Place circle i at `x = i × (d + spacing)`, centred vertically.","An empty path means nothing to draw."),
 tests=[({'width':300,'height':50,'count':4,'spacing':10},['diameter 50.0','bounds 0.0,0.0,230.0,50.0']), {'width':100,'height':80,'count':4,'spacing':4}, {'width':10,'height':10,'count':0,'spacing':2}]))
P.append(dict(id='cs193p-gesture-state', title='L16: Combining Pinch & Drag Gestures', topic='L16 · Shapes, gestures, persistence', diff='medium', platforms=MAC, concepts=['mutating','fundamental-types'], docs=[('GestureState', DOC+'gesturestate'), ('SimultaneousGesture', DOC+'simultaneousgesture')], videos=lec(16),
 sig='func boardGestures(_ events: [String]) -> [String]',
 statement="""L16's multi-touch pattern: keep **committed** state (`zoom`, `pan`) plus **in-flight** gesture state (`@GestureState`) that automatically resets when the gesture ends. Rendered values = committed combined with in-flight. Events: `pinch <m>` (in-flight magnification), `drag <dx> <dy>`, `end` (commit whatever is in flight), `cancel` (in-flight resets without committing). Log `"zoom <z> pan <x>,<y>"` (rendered values, 2 decimals) after each event.""",
 solution="""
 struct BoardState {
     private(set) var zoom = 1.0
     private(set) var pan = (x: 0.0, y: 0.0)
     private(set) var gestureZoom = 1.0
     private(set) var gesturePan = (x: 0.0, y: 0.0)

     var renderedZoom: Double { zoom * gestureZoom }
     var renderedPan: (x: Double, y: Double) { (pan.x + gesturePan.x, pan.y + gesturePan.y) }

     mutating func pinch(_ m: Double) { gestureZoom = m }
     mutating func drag(_ dx: Double, _ dy: Double) { gesturePan = (dx, dy) }

     mutating func end() {
         zoom *= gestureZoom
         pan = renderedPan
         cancel()
     }

     mutating func cancel() {
         gestureZoom = 1
         gesturePan = (0, 0)
     }
 }

 func boardGestures(_ events: [String]) -> [String] {
     var board = BoardState()
     let r = { (v: Double) in String((v * 100).rounded() / 100) }
     return events.map { e in
         let p = e.split(separator: " ").map(String.init)
         switch p[0] {
         case "pinch": board.pinch(Double(p.count > 1 ? p[1] : "") ?? 1)
         case "drag": board.drag(Double(p.count > 1 ? p[1] : "") ?? 0, Double(p.count > 2 ? p[2] : "") ?? 0)
         case "end": board.end()
         default: board.cancel()
         }
         let pan = board.renderedPan
         return "zoom \\(r(board.renderedZoom)) pan \\(r(pan.x)),\\(r(pan.y))"
     }
 }
 """,
 explain="""`@GestureState` is exactly the "in-flight" half: it tracks the gesture while it's active and snaps back to its initial value when it ends or is cancelled — you commit to `@State` in `.onEnded`. Rendering `committed ∘ inFlight` gives smooth feedback without corrupting the model mid-gesture.""",
 hints=("Keep committed values and in-flight values separately.","Rendered = committed zoom × in-flight zoom, committed pan + in-flight pan.","`end` folds in-flight into committed; `cancel` just resets in-flight."),
 tests=[({'events':['pinch 2','end','pinch 1.5','drag 10 -5','cancel','drag 3 4','end']},['zoom 2.0 pan 0.0,0.0','zoom 2.0 pan 0.0,0.0','zoom 3.0 pan 0.0,0.0','zoom 3.0 pan 10.0,-5.0','zoom 2.0 pan 0.0,0.0','zoom 2.0 pan 3.0,4.0','zoom 2.0 pan 3.0,4.0']), {'events':[]}]))
P.append(dict(id='cs193p-file-persistence', title='L16: Persisting Games to the File System', topic='L16 · Shapes, gestures, persistence', diff='medium', platforms=MAC, concepts=['codable','file-manager','error-handling'], docs=[('FileManager', 'https://developer.apple.com/documentation/foundation/filemanager'), ('JSONEncoder', 'https://developer.apple.com/documentation/foundation/jsonencoder')], videos=lec(16),
 sig='func saveAndLoad(_ games: [[String]]) -> [String]',
 statement="""L16's alternative to SwiftData: encode the model with `Codable` and write it to a file in the app's documents directory (here: a unique temp directory). Model `struct SavedGame: Codable, Equatable { var name: String; var master: [String]; var attempts: [[String]] }` from `[name, master, attempts comma-separated]`, write `[SavedGame]` as JSON (`.prettyPrinted, .sortedKeys`), read it back, and return `["<bytes> bytes", "round trip <equal|different>", names joined by ","]`. Clean up afterwards.""",
 solution="""
 import Foundation

 struct SavedGame: Codable, Equatable {
     var name: String
     var master: [String]
     var attempts: [[String]]
 }

 func saveAndLoad(_ games: [[String]]) -> [String] {
     let models = games.map { g in
         SavedGame(name: g[0], master: g[1].map(String.init), attempts: g[2].split(separator: ",").map { $0.map(String.init) })
     }
     let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
     defer { try? FileManager.default.removeItem(at: dir) }
     do {
         try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
         let url = dir.appendingPathComponent("games.json")
         let encoder = JSONEncoder()
         encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
         let data = try encoder.encode(models)
         try data.write(to: url, options: .atomic)
         let loaded = try JSONDecoder().decode([SavedGame].self, from: Data(contentsOf: url))
         return ["\\(data.count) bytes", "round trip \\(loaded == models ? "equal" : "different")", loaded.map(\\.name).joined(separator: ",")]
     } catch {
         return ["error \\(error)"]
     }
 }
 """,
 explain="""For small, self-contained data, `Codable` + a JSON file is simpler than a database: one encode, one atomic write. `Equatable` makes the round-trip check a one-liner. Switch to SwiftData once you need queries, relationships or partial updates.""",
 hints=("Make the model `Codable` and `Equatable`.","Encode to JSON, write atomically, then read and decode it back.","Compare the loaded array with the original using `==`."),
 tests=[{'games':[['Mastermind','RGBY','RRGG,RGBY'],['Undersea','ABCD','']]}, {'games':[]}]))
write_all(P, 'cs193p', 100)
