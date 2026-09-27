import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
DOC='https://developer.apple.com/documentation/swiftui/'
MAC=['darwin']
P=[]
P.append(dict(id='predict-text-concatenation', title='Predict: Text Modifiers Return Text', topic='View composition', mode='predict', platforms=MAC, concepts=['operator-overloading','opaque-types'], docs=[('Text', DOC+'text')],
 statement="""Most modifiers wrap a view in `ModifiedContent`, but some `Text`-specific modifiers return **`Text`** itself — which is what makes `Text + Text` concatenation possible. Predict the types.""",
 snippet="""
 import SwiftUI

 @MainActor func show() {
     let bold = Text("Hi").bold()
     let padded = Text("Hi").padding()
     let combined = Text("Hello ").bold() + Text("world").italic()
     print(type(of: bold))
     print(type(of: padded))
     print(type(of: combined))
 }
 show()
 """,
 explain="""`bold()`, `italic()`, `font(_:)` and `foregroundStyle(_:)` have `Text`-returning overloads, so styled runs can be joined with `+` into one `Text` (one text layout, correct line wrapping). General view modifiers like `padding()` return `ModifiedContent`, which can't be concatenated.""",
 hints=("Some modifiers are defined on `Text` and return `Text`.","`padding()` is a general view modifier.","Two of the three lines print `Text`.")))
P.append(dict(id='predict-property-wrapper-types', title='Predict: @State, Binding & Projected Values', topic='State & data flow', mode='predict', diff='medium', platforms=MAC, concepts=['property-wrappers','generics'], docs=[('State', DOC+'state'), ('Binding', DOC+'binding')],
 statement="""A property wrapper has a `wrappedValue` (what `count` means) and a `projectedValue` (what `$count` means). Predict the types.""",
 snippet="""
 import SwiftUI

 @MainActor func show() {
     let state = State(initialValue: 3)
     print(type(of: state.wrappedValue))
     print(type(of: state.projectedValue))
     let constant = Binding.constant(true)
     print(type(of: constant), constant.wrappedValue)
     let binding = Binding<[String]>.constant(["a", "b"])
     print(type(of: binding.first), type(of: binding[0]))
 }
 show()
 """,
 explain="""For `@State var count`, `count` is the `Int` and `$count` is a `Binding<Int>` — the projected value. `Binding` also forwards key paths and subscripts (`$array[0]` is a `Binding<String>`), which is how you bind into collections. `.constant` is handy for previews.""",
 hints=("`wrappedValue` is the plain value; `projectedValue` is what `$` gives you.","A `State<Int>`'s projected value is a `Binding<Int>`.","Subscripting a `Binding<[String]>` gives a `Binding<String>`.")))
P.append(dict(id='dynamic-type-sizes', title='Accessibility: Dynamic Type Sizes', topic='Accessibility', platforms=MAC, concepts=['enums','case-iterable','comparable'], docs=[('DynamicTypeSize', DOC+'dynamictypesize'), ('Accessibility', 'https://developer.apple.com/documentation/accessibility')],
 sig='func layoutFor(_ sizes: [String]) async -> [String]',
 statement="""Swiftful's *Accessibility: Dynamic Text*. `DynamicTypeSize` is `Comparable` and `CaseIterable`, with `isAccessibilitySize` for the largest five. A common pattern: switch from `HStack` to `VStack` layout when `size >= .accessibility1` (use `ViewThatFits` or `AnyLayout`).

 Map each size name (e.g. `large`, `xxxLarge`, `accessibility2`) to `"<name>: <HStack|VStack>"` (`unknown` for invalid names). Finally append `"accessibility sizes: <count>"`.""",
 solution="""
 import SwiftUI

 func layoutFor(_ sizes: [String]) async -> [String] {
     let byName = Dictionary(uniqueKeysWithValues: DynamicTypeSize.allCases.map { ("\\($0)", $0) })
     var out = sizes.map { name -> String in
         guard let size = byName[name] else { return "\\(name): unknown" }
         return "\\(name): \\(size >= .accessibility1 ? "VStack" : "HStack")"
     }
     out.append("accessibility sizes: \\(DynamicTypeSize.allCases.filter(\\.isAccessibilitySize).count)")
     return out
 }
 """,
 explain="""Text sizes run from `xSmall` to `accessibility5`; the `accessibility*` sizes are huge, so horizontal layouts must reflow vertically. Reading `@Environment(\\.dynamicTypeSize)` and comparing with `>=` is how adaptive layouts respect user settings.""",
 hints=("`DynamicTypeSize` is `CaseIterable` and `Comparable`.","Build a name → size dictionary from `allCases`, then compare with `>= .accessibility1`.","Count `allCases.filter(\\.isAccessibilitySize)`."),
 tests=[({'sizes':['large','xxxLarge','accessibility2','huge']},['large: HStack','xxxLarge: HStack','accessibility2: VStack','huge: unknown','accessibility sizes: 5']), {'sizes':[]}]))
P.append(dict(id='swipe-card-decision', title='DragGesture: Swipe Card Decisions', topic='Gestures', diff='medium', platforms=MAC, concepts=['enums','fundamental-types','tuples'], docs=[('DragGesture', DOC+'draggesture'), ('DragGesture.Value', DOC+'draggesture/value')],
 sig='func swipeDecisions(_ drags: [[Double]]) -> [String]',
 statement="""Like Swiftful's *Rebuild Bumble in SwiftUI*: when a drag ends you get `translation` and `predictedEndTranslation`. Decide per drag `[translationX, predictedEndX, translationY]`:
 - `"like"` if translationX > 120 **or** predictedEndX > 300
 - `"nope"` if translationX < −120 or predictedEndX < −300
 - `"superlike"` if translationY < −150 and |translationX| < 60
 - otherwise `"return"` (spring back)

 Also report the card's rotation for the translation: `rotation = translationX / 20` degrees, clamped to ±15, as `"<decision> <rotation rounded to 1dp>°"`.""",
 solution="""
 enum SwipeDecision: String { case like, nope, superlike, `return` }

 func decide(x: Double, predictedX: Double, y: Double) -> SwipeDecision {
     if y < -150 && abs(x) < 60 { return .superlike }
     if x > 120 || predictedX > 300 { return .like }
     if x < -120 || predictedX < -300 { return .nope }
     return .return
 }

 func swipeDecisions(_ drags: [[Double]]) -> [String] {
     drags.map { d in
         let rotation = min(max(d[0] / 20, -15), 15)
         return "\\(decide(x: d[0], predictedX: d[1], y: d[2]).rawValue) \\((rotation * 10).rounded() / 10)°"
     }
 }
 """,
 explain="""`predictedEndTranslation` includes the fling's momentum, so a short, fast flick still counts as a swipe — this is what makes gestures feel native. Keeping the decision a pure function of the gesture values makes it testable; the view just animates the result. (Backticks let you use `return` as a case name.)""",
 hints=("Use both the actual translation and the predicted end translation (momentum).","Check the super-like rule first, then like/nope thresholds, else return.","Rotation: `min(max(x / 20, -15), 15)`."),
 tests=[({'drags':[[150,200,0],[40,400,0],[-10,-50,-200],[-130,-100,10],[30,60,-20]]},['like 7.5°','like 2.0°','superlike -0.5°','nope -6.5°','return 1.5°']), {'drags':[]}, {'drags':[[400,400,0],[-400,0,0]]}]))
P.append(dict(id='magnification-clamp', title='MagnifyGesture: Zoom with Limits', topic='Gestures', platforms=MAC, concepts=['fundamental-types','mutating'], docs=[('MagnifyGesture', DOC+'magnifygesture')],
 sig='func zoomSession(_ events: [String]) -> [Double]',
 statement="""Swiftful's *MagnificationGesture*. Keep `lastScale` (committed) and `currentScale` (live). Events: `change <m>` → `currentScale = clamp(lastScale × m)`; `end` → commit (`lastScale = currentScale`); `doubletap` → reset both to 1. Clamp to 1…4. Return `currentScale` after each event (2 decimals).""",
 compare='float:1e-9',
 solution="""
 struct ZoomState {
     private(set) var lastScale = 1.0
     private(set) var currentScale = 1.0

     private func clamp(_ v: Double) -> Double { min(max(v, 1), 4) }

     mutating func change(by magnification: Double) { currentScale = clamp(lastScale * magnification) }
     mutating func end() { lastScale = currentScale }
     mutating func reset() { lastScale = 1; currentScale = 1 }
 }

 func zoomSession(_ events: [String]) -> [Double] {
     var zoom = ZoomState()
     return events.map { e in
         let p = e.split(separator: " ")
         switch p[0] {
         case "change": zoom.change(by: Double(p[1]) ?? 1)
         case "end": zoom.end()
         default: zoom.reset()
         }
         return (zoom.currentScale * 100).rounded() / 100
     }
 }
 """,
 explain="""Magnification is **relative to the start of the gesture**, so you multiply by the last committed scale and only commit on `.onEnded`. Forgetting that split is the classic "zoom jumps back" bug.""",
 hints=("A gesture's magnification is relative to where *this* gesture started.","Live value = clamp(lastScale × m); commit it on end.","Clamp with `min(max(v, 1), 4)`."),
 tests=[({'events':['change 2','end','change 1.5','end','change 0.1','doubletap']},[2,2,3,3,1,1]), {'events':[]}, {'events':['change 10','change 0.5']}]))
P.append(dict(id='rotation-snap', title='RotateGesture: Snap to 90°', topic='Gestures', platforms=MAC, concepts=['fundamental-types'], docs=[('RotateGesture', DOC+'rotategesture'), ('Angle', DOC+'angle')],
 sig='func snapAngles(_ degrees: [Double]) async -> [Double]',
 statement="""Swiftful's *RotationGesture*: when the gesture ends, snap the accumulated rotation to the nearest multiple of 90° and normalise into `0..<360`. Use SwiftUI's `Angle` (`.degrees(x)` / `.degrees` / `.radians`) for the conversions.""",
 compare='float:1e-9',
 solution="""
 import SwiftUI

 func snap(_ angle: Angle) -> Angle {
     let snapped = (angle.degrees / 90).rounded() * 90
     // Adding 360 and taking the remainder again maps negatives into range and turns -0.0 into +0.0.
     let normalised = (snapped.truncatingRemainder(dividingBy: 360) + 360).truncatingRemainder(dividingBy: 360)
     return .degrees(normalised)
 }

 func snapAngles(_ degrees: [Double]) async -> [Double] {
     degrees.map { snap(.degrees($0)).degrees }
 }
 """,
 explain="""`Angle` stores radians and converts on demand, so you never mix units by accident. `truncatingRemainder` keeps the sign, hence the fix-up for negative angles — and watch out for **negative zero**: snapping −30° gives `-0.0`, which is *not* `< 0`, so a naive `if x < 0 { x += 360 }` leaves `-0` behind. `(x % 360 + 360) % 360` handles both.""",
 hints=("Snap first: `(degrees / 90).rounded() * 90`.","Normalise with `truncatingRemainder(dividingBy: 360)` and add 360 if negative.","Wrap values in `Angle.degrees(_:)` and read `.degrees` back."),
 tests=[({'degrees':[44,46,-30,270]},[0,90,0,270]), {'degrees':[400]}, {'degrees':[]}, {'degrees':[-135,720,89.9]}]))
P.append(dict(id='long-press-progress', title='LongPressGesture: Hold-to-Confirm Progress', topic='Gestures', platforms=MAC, concepts=['fundamental-types','enums'], docs=[('LongPressGesture', DOC+'longpressgesture')],
 sig='func holdProgress(_ holds: [Double], required: Double) -> [String]',
 statement="""Swiftful's *LongPressGesture* hold-to-confirm button. Given how long the finger was held (seconds) and the required duration, return `"<percent>% <state>"` where percent is `min(held / required, 1)` as an integer and state is `"confirmed"` when complete, `"cancelled"` if released under 30%, else `"partial"` (the bar animates back).""",
 solution="""
 func holdProgress(_ holds: [Double], required: Double) -> [String] {
     holds.map { held in
         let progress = required > 0 ? min(max(held / required, 0), 1) : 1
         let state = progress >= 1 ? "confirmed" : progress < 0.3 ? "cancelled" : "partial"
         return "\\(Int((progress * 100).rounded(.down)))% \\(state)"
     }
 }
 """,
 explain="""`LongPressGesture(minimumDuration:)` gives `onPressingChanged` and `onEnded`; the progress bar is just state animated over the duration. Guarding `required > 0` avoids dividing by zero.""",
 hints=("Progress is held ÷ required, capped at 1.","Decide the state from the progress: complete, under 30%, or in between.","Truncate the percentage with `rounded(.down)`."),
 tests=[({'holds':[0.5,1.5,3,0.1],'required':2},['25% cancelled','75% partial','100% confirmed','5% cancelled']), {'holds':[],'required':1}, {'holds':[1],'required':0}]))
P.append(dict(id='scroll-parallax', title='Scroll Effects: Parallax & Fade', topic='Layout', diff='medium', platforms=MAC, concepts=['fundamental-types'], docs=[('visualEffect(_:)', DOC+'view/visualeffect(_:)'), ('ScrollView', DOC+'scrollview')],
 sig='func headerEffects(_ offsets: [Double], headerHeight: Double) -> [[Double]]',
 statement="""Paul's *ScrollView effects using visualEffect()*. For a sticky header of height `h` and scroll offset `y` (negative = pulled down):
 - **stretch**: when `y < 0`, height = `h − y`, else `h`
 - **parallax**: the image moves at half speed: `offsetY = max(y, 0) / 2`
 - **fade**: opacity = `1 − min(max(y, 0) / h, 1)`

 Return `[height, offsetY, opacity]` rounded to 2 decimals per offset.""",
 compare='float:1e-9',
 solution="""
 func headerEffects(_ offsets: [Double], headerHeight h: Double) -> [[Double]] {
     offsets.map { y in
         let height = y < 0 ? h - y : h
         let offsetY = max(y, 0) / 2
         let opacity = 1 - min(max(y, 0) / h, 1)
         return [height, offsetY, opacity].map { ($0 * 100).rounded() / 100 }
     }
 }
 """,
 explain="""Scroll-linked effects are pure functions of the scroll offset; `visualEffect { content, proxy in … }` (iOS 17) gives you the geometry each frame without re-running `body`. Keep the math separate and it's easy to tune and test.""",
 hints=("Each effect is a small formula of the scroll offset.","Pulling down (negative y) stretches; scrolling up (positive y) moves and fades.","`opacity = 1 − min(max(y, 0) / h, 1)`."),
 tests=[({'offsets':[-50,0,100,300],'headerHeight':200},[[250,0,1],[200,0,1],[200,50,0.5],[200,150,0]]), {'offsets':[],'headerHeight':100}]))
P.append(dict(id='paging-target', title='Paging ScrollView: Choosing the Target Page', topic='Lists', diff='medium', platforms=MAC, concepts=['fundamental-types'], docs=[('scrollTargetBehavior(_:)', DOC+'view/scrolltargetbehavior(_:)')],
 sig='func targetPages(_ gestures: [[Double]], pageWidth: Double, pageCount: Int) -> [Int]',
 statement="""Swiftful's *Paging ScrollView for iOS 17*. A paging behaviour decides the final page from the release offset and velocity `[offset, velocity]`: if `|velocity| > 0.5`, move one page in the velocity's direction from the page you were on (`floor` for positive, `ceil` for negative, of offset/pageWidth); otherwise snap to the **nearest** page. Clamp to `0..<pageCount`.""",
 solution="""
 func targetPages(_ gestures: [[Double]], pageWidth: Double, pageCount: Int) -> [Int] {
     gestures.map { g in
         let position = g[0] / pageWidth
         let page: Double
         if g[1] > 0.5 { page = position.rounded(.down) + 1 }
         else if g[1] < -0.5 { page = position.rounded(.up) - 1 }
         else { page = position.rounded() }
         return min(max(Int(page), 0), max(pageCount - 1, 0))
     }
 }
 """,
 explain="""`.scrollTargetBehavior(.paging)` does this for you; writing a custom `ScrollTargetBehavior` means implementing exactly this decision. Velocity-aware snapping is what makes a flick feel intentional.""",
 hints=("Convert the offset to a fractional page position first.","Fast flicks move one page in the flick direction; slow releases snap to the nearest page.","Clamp the result to `0...(pageCount - 1)`."),
 tests=[({'gestures':[[130,0],[130,1],[260,-2],[-40,-3],[990,5]],'pageWidth':100,'pageCount':5},[1,2,2,0,4]), {'gestures':[],'pageWidth':100,'pageCount':3}]))
P.append(dict(id='view-that-fits', title='ViewThatFits: Picking the First Fit', topic='Layout', platforms=MAC, concepts=['optionals','higher-order-functions'], docs=[('ViewThatFits', DOC+'viewthatfits')],
 sig='func chooseLayouts(idealWidths: [Double], available: [Double]) -> [Int]',
 statement="""Swiftful's *ViewThatFits*: SwiftUI tries each child in order and shows the **first** whose ideal width fits the available width; if none fit, it shows the **last**. Given the children's ideal widths, return the chosen index for each available width.""",
 solution="""
 func chooseLayouts(idealWidths: [Double], available: [Double]) -> [Int] {
     available.map { width in
         idealWidths.firstIndex { $0 <= width } ?? max(idealWidths.count - 1, 0)
     }
 }
 """,
 explain="""Order children from most to least spacious (e.g. full labels, then icons only). `ViewThatFits` measures ideal sizes, so it can't shrink a view to fit — it only *chooses* between alternatives.""",
 hints=("Try the options in order and take the first that fits.","`firstIndex { $0 <= width }` finds it.","Fall back to the last index when none fit."),
 tests=[({'idealWidths':[300,180,60],'available':[400,200,100,10]},[0,1,2,2]), {'idealWidths':[50],'available':[]}, {'idealWidths':[100,50],'available':[100,49.9]}]))
P.append(dict(id='sheet-item-state', title='Sheets & Alerts Driven by Optional Items', topic='Navigation', diff='medium', platforms=MAC, concepts=['enums','optionals','protocols'], docs=[('sheet(item:onDismiss:content:)', DOC+'view/sheet(item:ondismiss:content:)')],
 sig='func presentations(_ actions: [String]) -> [String]',
 statement="""Paul's *Using alert() and sheet() with optionals*: instead of several `Bool`s, drive presentation with one optional `Identifiable` enum: `enum ActiveSheet: Identifiable { case settings, profile(Int), share(String) }` whose `id` is a string.

 Actions: `open settings`, `open profile 7`, `open share url`, `dismiss`. SwiftUI can show one sheet at a time: opening while one is presented **replaces** it (logs `"replace <old> with <new>"`), otherwise logs `"present <id>"`; dismiss logs `"dismiss <id>"` or `"nothing to dismiss"`.""",
 solution="""
 enum ActiveSheet: Identifiable {
     case settings, profile(Int), share(String)

     var id: String {
         switch self {
         case .settings: "settings"
         case .profile(let id): "profile-\\(id)"
         case .share(let url): "share-\\(url)"
         }
     }
 }

 func presentations(_ actions: [String]) -> [String] {
     var active: ActiveSheet?
     var log: [String] = []
     for action in actions {
         let p = action.split(separator: " ").map(String.init)
         if p[0] == "dismiss" {
             log.append(active.map { "dismiss \\($0.id)" } ?? "nothing to dismiss")
             active = nil
             continue
         }
         let next: ActiveSheet? = switch (p.count > 1 ? p[1] : "", p.count > 2 ? p[2] : "") {
         case ("settings", _): .settings
         case ("profile", let n): Int(n).map(ActiveSheet.profile)
         case ("share", let url): .share(url)
         default: nil
         }
         guard let next else { continue }
         log.append(active.map { "replace \\($0.id) with \\(next.id)" } ?? "present \\(next.id)")
         active = next
     }
     return log
 }
 """,
 explain="""One optional `Identifiable` item makes impossible states unrepresentable (two sheets "open" at once) and carries the data the sheet needs. `.sheet(item: $activeSheet) { sheet in switch sheet { … } }` presents whatever is set; SwiftUI re-presents when the `id` changes.""",
 hints=("Replace several Bools with one optional enum.","The enum's `id` must distinguish cases *and* their payloads.","Opening while `active != nil` is a replacement; `dismiss` sets it back to `nil`."),
 tests=[({'actions':['open settings','open profile 7','dismiss','dismiss','open share x']},['present settings','replace settings with profile-7','dismiss profile-7','nothing to dismiss','present share-x']), {'actions':[]}, {'actions':['open profile abc','open unknown']}]))
P.append(dict(id='tab-badges', title='TabView Selection & Badges', topic='Navigation', platforms=MAC, concepts=['enums','case-iterable','dictionary-basics'], docs=[('TabView', DOC+'tabview'), ('badge(_:)', DOC+'view/badge(_:)-84e43')],
 sig='func tabBar(_ events: [String]) -> [String]',
 statement="""Swiftful's *Badges on TabView*. `enum Tab: String, CaseIterable { case home, search, inbox, profile }` with selection and a `[Tab: Int]` badge store. Events: `select <tab>` (selecting `inbox` clears its badge), `notify <tab> <n>` (adds to the badge), `logout` (select `home`, clear all). After all events return one line per tab `"<tab><*> <badge>"` where `*` marks the selected tab and badges of 0 show `-`.""",
 solution="""
 enum Tab: String, CaseIterable { case home, search, inbox, profile }

 func tabBar(_ events: [String]) -> [String] {
     var selected = Tab.home
     var badges: [Tab: Int] = [:]
     for e in events {
         let p = e.split(separator: " ").map(String.init)
         switch p[0] {
         case "select":
             guard p.count > 1, let tab = Tab(rawValue: p[1]) else { continue }
             selected = tab
             if tab == .inbox { badges[.inbox] = nil }
         case "notify":
             guard p.count > 2, let tab = Tab(rawValue: p[1]), let n = Int(p[2]) else { continue }
             badges[tab, default: 0] += n
         default:
             selected = .home
             badges.removeAll()
         }
     }
     return Tab.allCases.map { tab in
         let badge = badges[tab] ?? 0
         return "\\(tab.rawValue)\\(tab == selected ? "*" : "") \\(badge == 0 ? "-" : String(badge))"
     }
 }
 """,
 explain="""`TabView(selection:)` binds to a `Hashable` value — an enum is ideal. `.badge(count)` hides itself at 0. Keeping badge counts in a dictionary keyed by the tab enum keeps the view declarative.""",
 hints=("Use an enum for tab selection and a `[Tab: Int]` for badges.","Selecting inbox clears its badge; `logout` resets everything.","Print tabs in `allCases` order, marking the selected one."),
 tests=[({'events':['notify inbox 3','notify search 1','select inbox','notify inbox 2','select profile']},['home -','search 1','inbox 2','profile* -']), {'events':[]}, {'events':['notify home 5','logout','select nope']}]))
P.append(dict(id='countdown-viewmodel', title='Timer-Driven Countdown View Model', topic='State & data flow', diff='medium', platforms=MAC, concepts=['property-wrappers','enums','computed-properties'], docs=[('Timer', 'https://developer.apple.com/documentation/foundation/timer'), ('onReceive(_:perform:)', DOC+'view/onreceive(_:perform:)')],
 sig='func countdown(seconds: Int, events: [String]) -> [String]',
 statement="""Swiftful's *Timer and onReceive*: the view forwards ticks from `Timer.publish(every: 1, …)` to an `@Observable` view model, which owns the logic. Implement `CountdownModel` with `remaining`, `isRunning`, `func start()`, `pause()`, `reset()`, `tick()` (only counts while running; stops at 0 and marks `finished`) and a computed `display` in `"m:ss"` format.

 Events: `start`, `pause`, `reset`, `tick`. Return `display` (plus `" done"` when finished) after each event.""",
 solution="""
 import Observation

 @Observable
 final class CountdownModel {
     let total: Int
     private(set) var remaining: Int
     private(set) var isRunning = false
     private(set) var finished = false

     init(seconds: Int) {
         total = seconds
         remaining = seconds
     }

     var display: String { "\\(remaining / 60):\\(remaining % 60 < 10 ? "0" : "")\\(remaining % 60)" }

     func start() { if remaining > 0 { isRunning = true } }
     func pause() { isRunning = false }
     func reset() { remaining = total; isRunning = false; finished = false }

     func tick() {
         guard isRunning, remaining > 0 else { return }
         remaining -= 1
         if remaining == 0 { isRunning = false; finished = true }
     }
 }

 func countdown(seconds: Int, events: [String]) -> [String] {
     let model = CountdownModel(seconds: seconds)
     return events.map { e in
         switch e {
         case "start": model.start()
         case "pause": model.pause()
         case "reset": model.reset()
         default: model.tick()
         }
         return model.display + (model.finished ? " done" : "")
     }
 }
 """,
 explain="""Keep timers dumb and models smart: the view does `.onReceive(timer) { _ in model.tick() }`, and all rules live in a testable class. Tests call `tick()` directly instead of waiting for real seconds.""",
 hints=("Ticks only count while running; the model decides what a tick means.","`tick()` guards `isRunning` and stops (and flags `finished`) at zero.","Format with `remaining / 60` and a zero-padded `remaining % 60`."),
 tests=[({'seconds':62,'events':['tick','start','tick','tick','pause','tick','reset']},['1:02','1:02','1:01','1:00','1:00','1:00','1:02']), {'seconds':2,'events':['start','tick','tick','tick','start']}, {'seconds':0,'events':['start','tick']}]))
P.append(dict(id='slider-stepper-snap', title='Slider & Stepper Value Snapping', topic='Controls & input', platforms=MAC, concepts=['fundamental-types','range-clamp' if False else 'half-open-range'], docs=[('Slider', DOC+'slider'), ('Stepper', DOC+'stepper')],
 sig='func snapValues(_ raw: [Double], min lower: Double, max upper: Double, step: Double) -> [Double]',
 statement="""`Slider(value:in:step:)` and `Stepper(value:in:step:)` snap values to the nearest step **measured from the lower bound**, then clamp into the range. Implement that rule for each raw value.""",
 compare='float:1e-9',
 solution="""
 func snapValues(_ raw: [Double], min lower: Double, max upper: Double, step: Double) -> [Double] {
     raw.map { v in
         let stepped = step > 0 ? lower + ((v - lower) / step).rounded() * step : v
         return min(max(stepped, lower), upper)
     }
 }
 """,
 explain="""Snapping relative to the lower bound matters when the range doesn't start at a multiple of the step (e.g. 5…50 in steps of 10 → 5, 15, 25…). Binding a control to a model value that already obeys the rule avoids jumps.""",
 hints=("Snap relative to the lower bound, not to zero.","`lower + ((v − lower) / step).rounded() * step`, then clamp.","Handle `step <= 0` by skipping the snapping."),
 tests=[({'raw':[7,12,49,100,-3],'lower':5,'upper':50,'step':10},[5,15,45,50,5]), {'raw':[0.26,0.74],'lower':0,'upper':1,'step':0.25}, {'raw':[3.3],'lower':0,'upper':10,'step':0}]))
P[-1]['tests'] = [({'raw':[7,12,49,100,-3],'lower':5,'upper':50,'step':10},[5,15,45,50,5]), {'raw':[0.26,0.74],'lower':0,'upper':1,'step':0.25}, {'raw':[3.3],'lower':0,'upper':10,'step':0}]
P.append(dict(id='observableobject-vs-observable', title='ObservableObject vs @Observable', topic='State & data flow', diff='hard', platforms=MAC, concepts=['property-wrappers','combine' if False else 'closures'], docs=[('ObservableObject', 'https://developer.apple.com/documentation/combine/observableobject'), ('Migrating to the Observable macro', 'https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro')],
 sig='func invalidations(_ changes: [String]) -> [Int]',
 statement="""Compare how many times a view that shows only `name` would be invalidated:
 - **Legacy**: `final class ProfileVM: ObservableObject { @Published var name; @Published var followers }` — any `@Published` change fires `objectWillChange` (count via `sink`).
 - **Modern**: `@Observable final class ProfileModel { var name; var followers }` — only reads of `name` are tracked (re-arm after each fire).

 Apply changes `name <v>` / `followers <n>` to both and return `[legacyCount, modernCount]`.""",
 solution="""
 import Combine
 import Observation

 final class ProfileVM: ObservableObject {
     @Published var name = ""
     @Published var followers = 0
 }

 @Observable
 final class ProfileModel {
     var name = ""
     var followers = 0
 }

 final class Tally: @unchecked Sendable {
     var fires = 0
     var armed = false
 }

 func track(_ model: ProfileModel, _ tally: Tally) {
     guard !tally.armed else { return }
     tally.armed = true
     withObservationTracking { _ = model.name } onChange: {
         tally.fires += 1
         tally.armed = false
     }
 }

 func invalidations(_ changes: [String]) -> [Int] {
     let legacy = ProfileVM()
     var legacyCount = 0
     let cancellable = legacy.objectWillChange.sink { legacyCount += 1 }
     let modern = ProfileModel()
     let tally = Tally()
     for change in changes {
         track(modern, tally)
         let p = change.split(separator: " ", maxSplits: 1).map(String.init)
         let value = p.count > 1 ? p[1] : ""
         if p[0] == "name" {
             legacy.name = value
             modern.name = value
         } else {
             legacy.followers = Int(value) ?? 0
             modern.followers = Int(value) ?? 0
         }
     }
     _ = cancellable
     return [legacyCount, tally.fires]
 }
 """,
 explain="""`ObservableObject` has one coarse signal (`objectWillChange`) — every `@Published` write re-renders every observing view, even ones that don't show that property. `@Observable` tracks per-property access, so the name label ignores follower updates. That's the main performance reason to migrate.""",
 hints=("`objectWillChange` fires for *every* `@Published` property.","Count legacy fires with `objectWillChange.sink`; for the modern model, track only `model.name` and re-arm after each fire.","Apply every change to both models, then return both counts."),
 tests=[({'changes':['followers 10','name Ana','followers 11','followers 12']},[4,1]), {'changes':[]}, {'changes':['name a','name b']}]))
P.append(dict(id='appstorage-onboarding', title='@AppStorage: Persisted Onboarding', topic='State & data flow', diff='medium', platforms=MAC, concepts=['property-wrappers','enums'], docs=[('AppStorage', DOC+'appstorage'), ('UserDefaults', 'https://developer.apple.com/documentation/foundation/userdefaults')],
 sig='func onboardingRuns(_ sessions: [[String]]) async -> [String]',
 statement="""Swiftful's *Manage user onboarding with @AppStorage*. Use `AppStorage(wrappedValue:_:store:)` with a **private** `UserDefaults(suiteName:)` so tests don't touch real settings. Keys: `"onboardingStep"` (Int, default 0) and `"userName"` (String, default "").

 Each inner array is one app launch: actions `next` (step += 1, max 3), `name <n>`, `skip` (step = 3). At the start of each launch, log `"launch step <s> name <n|->"` — showing values **persisted** from previous launches. Clear the suite first.""",
 solution="""
 import SwiftUI

 @MainActor func run(_ sessions: [[String]]) -> [String] {
     // A suite named by an absolute path is a private plist file: one per process, in the temp
     // directory, so parallel runs never clobber each other and ~/Library/Preferences stays clean.
     let suite = NSTemporaryDirectory() + "swift-judge-onboarding-\\(ProcessInfo.processInfo.processIdentifier)"
     let store = UserDefaults(suiteName: suite)!
     store.removePersistentDomain(forName: suite)
     var log: [String] = []
     for actions in sessions {
         let step = AppStorage(wrappedValue: 0, "onboardingStep", store: store)
         let name = AppStorage(wrappedValue: "", "userName", store: store)
         log.append("launch step \\(step.wrappedValue) name \\(name.wrappedValue.isEmpty ? "-" : name.wrappedValue)")
         for action in actions {
             let p = action.split(separator: " ", maxSplits: 1).map(String.init)
             switch p[0] {
             case "next": step.wrappedValue = min(step.wrappedValue + 1, 3)
             case "skip": step.wrappedValue = 3
             case "name": name.wrappedValue = p.count > 1 ? p[1] : ""
             default: break
             }
         }
     }
     store.removePersistentDomain(forName: suite)
     try? FileManager.default.removeItem(atPath: suite + ".plist")
     return log
 }

 func onboardingRuns(_ sessions: [[String]]) async -> [String] {
     await run(sessions)
 }
 """,
 explain="""`@AppStorage` is a property wrapper over `UserDefaults` that also re-renders views when the value changes. Values survive relaunches; injecting a custom `store:` keeps tests and previews isolated. Store small settings only — not models or secrets (use files/SwiftData and the Keychain).""",
 hints=("`@AppStorage` is backed by `UserDefaults`; pass a suite store to isolate it.","Create fresh `AppStorage` wrappers per launch — they read what the previous launch saved.","Write through `wrappedValue`; clear the suite with `removePersistentDomain(forName:)`."),
 tests=[({'sessions':[['next','name Ana'],['next'],['skip'],[]]},['launch step 0 name -','launch step 1 name Ana','launch step 2 name Ana','launch step 3 name Ana']), {'sessions':[]}, {'sessions':[['next','next','next','next'],[]]}]))
P.append(dict(id='environment-shared-model', title='Sharing an @Observable Model via the Environment', topic='State & data flow', diff='medium', platforms=MAC, concepts=['value-vs-reference','dependency-injection'], docs=[('environment(_:)', DOC+'environment'), ('Managing model data in your app', DOC+'managing-model-data-in-your-app')],
 sig='func cartScreens(_ actions: [String]) -> [String]',
 statement="""Paul's *Sharing @Observable objects through SwiftUI's environment*. One `@Observable final class Cart` is injected at the root (`.environment(cart)`); a product list "screen" adds items and a badge "screen" reads the count. Simulate both screens as structs that each hold the **same** injected reference.

 Actions: `add <item>` (list screen), `remove <item>` (list screen, first match), `badge` (badge screen logs `"badge <count>"`). Also log `"same instance <Bool>"` at the end (compare with `===`).""",
 solution="""
 import Observation

 @Observable
 final class Cart {
     var items: [String] = []
 }

 struct ProductListScreen {
     let cart: Cart
     func add(_ item: String) { cart.items.append(item) }
     func remove(_ item: String) {
         if let i = cart.items.firstIndex(of: item) { cart.items.remove(at: i) }
     }
 }

 struct BadgeScreen {
     let cart: Cart
     var label: String { "badge \\(cart.items.count)" }
 }

 func cartScreens(_ actions: [String]) -> [String] {
     let cart = Cart()
     let list = ProductListScreen(cart: cart)
     let badge = BadgeScreen(cart: cart)
     var log: [String] = []
     for action in actions {
         let p = action.split(separator: " ", maxSplits: 1).map(String.init)
         switch p[0] {
         case "add": list.add(p.count > 1 ? p[1] : "")
         case "remove": list.remove(p.count > 1 ? p[1] : "")
         default: log.append(badge.label)
         }
     }
     log.append("same instance \\(list.cart === badge.cart)")
     return log
 }
 """,
 explain="""Because the model is a **class**, every view that receives it shares one instance — writes from one screen are seen by all, and `@Observable` re-renders just the readers. Structs holding the reference (like SwiftUI views) stay cheap to recreate. In a view you'd write `@Environment(Cart.self) private var cart`.""",
 hints=("Shared, mutable app state lives in a class so everyone sees the same instance.","Give both screen structs the same `Cart` reference.","`list.cart === badge.cart` proves identity."),
 tests=[({'actions':['add tea','badge','add jam','remove tea','badge']},['badge 1','badge 1','same instance true']), {'actions':[]}]))
P.append(dict(id='list-diffing-identity', title='Identity in Lists: Diffing by ID', topic='Lists', diff='hard', platforms=MAC, concepts=['equatable-hashable','protocols','higher-order-functions'], docs=[('CollectionDifference', 'https://developer.apple.com/documentation/swift/collectiondifference'), ('Demystify SwiftUI (WWDC21)', 'https://developer.apple.com/videos/play/wwdc2021/10022/')],
 sig='func diffRows(old: [[String]], new: [[String]]) -> [String]',
 statement="""SwiftUI (like React) diffs lists by **identity**. Rows are `[id, title]`. Compute what changed between `old` and `new` **by id** using `CollectionDifference` (`new.map(\\.id).difference(from: old.map(\\.id)).inferringMoves()`): report `"insert <id>"`, `"remove <id>"`, `"move <id>"` (a removal paired with an insertion), then `"update <id>"` for ids present in both whose title changed. Sort each category by id.""",
 solution="""
 func diffRows(old: [[String]], new: [[String]]) -> [String] {
     let diff = new.map { $0[0] }.difference(from: old.map { $0[0] }).inferringMoves()
     var inserts: [String] = [], removes: [String] = [], moves: Set<String> = []
     for change in diff {
         switch change {
         case let .insert(_, id, associatedWith):
             if associatedWith != nil { moves.insert(id) } else { inserts.append(id) }
         case let .remove(_, id, associatedWith):
             if associatedWith != nil { moves.insert(id) } else { removes.append(id) }
         }
     }
     let oldTitles = Dictionary(old.map { ($0[0], $0[1]) }, uniquingKeysWith: { a, _ in a })
     let updates = new.filter { row in oldTitles[row[0]].map { $0 != row[1] } ?? false }.map { $0[0] }
     return inserts.sorted().map { "insert \\($0)" }
         + removes.sorted().map { "remove \\($0)" }
         + moves.sorted().map { "move \\($0)" }
         + updates.sorted().map { "update \\($0)" }
 }
 """,
 explain="""With stable ids, a reorder is a **move** (the row keeps its state and animates) and an edited title is an **update** — without ids, both look like remove + insert, losing state. That's why `ForEach` needs `Identifiable` data, and why using array indices as ids causes glitches. Note that a diff is *a* minimal edit script, not *the* one: when `[1, 2, 3]` becomes `[3, 1, 4]`, calling either 1 or 3 "the mover" is equally short — the algorithm's choice is deterministic but arbitrary.""",
 hints=("Diff the id arrays, not the rows themselves.","`difference(from:).inferringMoves()` pairs removals and insertions of the same id into moves.","Updates are ids present in both whose title changed."),
 tests=[{'old':[['1','a'],['2','b'],['3','c']],'new':[['3','c'],['1','A'],['4','d']]}, {'old':[],'new':[]}, {'old':[['1','a']],'new':[['2','b']]}]))
write_all(P, 'swiftui', 300)
