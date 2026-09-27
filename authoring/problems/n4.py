import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
DOC='https://developer.apple.com/documentation/swiftui/'
MAC=['darwin']
P=[]
P.append(dict(id='predict-viewbuilder-types', title='Predict: What @ViewBuilder Really Builds', topic='View composition', mode='predict', diff='medium', platforms=MAC, concepts=['result-builders','opaque-types'], docs=[('ViewBuilder', DOC+'viewbuilder')],
 statement="""A SwiftUI `body` is a **result builder**. Each `if`, `if/else` and group of views becomes a concrete generic type. Predict the printed types (module prefixes are shown as SwiftUI prints them).""",
 snippet="""
 import SwiftUI

 @MainActor func types(flag: Bool) {
     let a = VStack { Text("A"); Text("B") }
     let b = VStack { Text("A"); if flag { Text("B") } }
     let c = VStack { if flag { Text("A") } else { Image(systemName: "star") } }
     print(type(of: a))
     print(type(of: b))
     print(type(of: c))
 }
 types(flag: true)
 """,
 explain="""Two children become `TupleView<(Text, Text)>`; an `if` without `else` becomes `Optional<Text>`; `if/else` becomes `_ConditionalContent<Text, Image>`. `some View` hides these types from you, but SwiftUI uses them to diff **structurally** — which is why `AnyView` (which erases them) can hurt performance and animations.""",
 hints=("Several child views are packed into a tuple view.","An `if` without `else` produces an optional; `if/else` produces a two-branch conditional type.","Line 1 is `VStack<TupleView<(Text, Text)>>`.")))
P.append(dict(id='predict-modifier-order', title='Predict: Why Modifier Order Matters', topic='View composition', mode='predict', diff='medium', platforms=MAC, concepts=['generics','result-builders'], docs=[('ViewModifier', DOC+'viewmodifier')],
 statement="""Every modifier **wraps** the view it's applied to in a new `ModifiedContent` type. Predict the types — then reason about why `padding().background(.red)` looks different from `background(.red).padding()`.""",
 snippet="""
 import SwiftUI

 @MainActor func show() {
     let one = Text("Hi").padding().background(Color.red)
     let two = Text("Hi").background(Color.red).padding()
     print(type(of: one))
     print(type(of: two))
     print(type(of: one) == type(of: two))
 }
 show()
 """,
 explain="""`one` is `ModifiedContent<ModifiedContent<Text, _PaddingLayout>, _BackgroundStyleModifier<Color>>`: the background wraps the **padded** view, so the red fills the padding too. `two` pads **after** the background, leaving the padding clear. Modifiers aren't flags on one view — they're nested wrappers, applied inside-out.""",
 hints=("Each modifier returns a *new* view that wraps the previous one.","The outermost type is the **last** modifier you applied.","The two types are different, so the last line prints `false`.")))
P.append(dict(id='predict-anyview-foreach', title='Predict: AnyView, Group & ForEach Types', topic='View composition', mode='predict', diff='medium', platforms=MAC, concepts=['type-erasure','opaque-types'], docs=[('AnyView', DOC+'anyview'), ('ForEach', DOC+'foreach')],
 statement="Predict the types SwiftUI builds for these containers.",
 snippet="""
 import SwiftUI

 @MainActor func show() {
     let erased = AnyView(Text("x"))
     let looped = ForEach(0..<3, id: \\.self) { Text("\\($0)") }
     let grouped = Group { Text("a"); Text("b"); Text("c") }
     print(type(of: erased))
     print(type(of: looped))
     print(type(of: grouped))
 }
 show()
 """,
 explain="""`AnyView` erases everything to one type (SwiftUI must then compare contents dynamically). `ForEach` keeps the data, ID and content types — `ForEach<Range<Int>, Int, Text>`. `Group` is a transparent wrapper around a tuple view.""",
 hints=("`AnyView` hides the wrapped type completely.","`ForEach`'s generic parameters are the data, the ID type and the content view.","`ForEach<Range<Int>, Int, Text>` for the loop.")))
P.append(dict(id='diag-state-needed', title='Diagnostic: Why @State Exists', topic='State & data flow', mode='diagnostic', platforms=MAC, concepts=['mutating','property-wrappers','struct-vs-class'], docs=[('State', DOC+'state')],
 statement="""A SwiftUI view is a **struct**, and `body` is not `mutating`. Write a view with a plain `var count = 0` and a `Button("+") { count += 1 }` inside `body`. You pass when the compiler rejects the mutation — the problem `@State` solves.""",
 starter="import SwiftUI\n\nstruct CounterView: View {\n    @State private var count = 0\n    var body: some View {\n        Button(\"Count: \\(count)\") { count += 1 }\n    }\n}\n",
 solution="import SwiftUI\n\nstruct CounterView: View {\n    var count = 0\n    var body: some View {\n        Button(\"Count: \\(count)\") { count += 1 }\n    }\n}\n",
 explain="""*cannot assign to property: 'self' is immutable*. Views are short-lived value descriptions; SwiftUI recreates them freely. `@State` moves the storage **outside** the struct into SwiftUI-managed memory, and its nonmutating setter triggers a re-render — like `useState` but owned by the framework's view graph.""",
 hints=("`body` can't mutate the view struct's own stored properties.","Declare `var count = 0` without a property wrapper and increment it in a button action.","`Button(\"+\") { count += 1 }` with a plain `var count`."),
 tests=[{'name':'Mutation rejected','pattern':"'self' is immutable"}]))
P.append(dict(id='diag-opaque-mismatch', title="Diagnostic: some View Must Be One Type", topic='View composition', mode='diagnostic', platforms=MAC, concepts=['opaque-types','result-builders'], docs=[('ViewBuilder', DOC+'viewbuilder')],
 statement="""Write a helper `func badge(_ on: Bool) -> some View` (no `@ViewBuilder`) that uses `return Text("on")` in one branch and `return Image(systemName: "xmark")` in another. You pass when the compiler rejects the mismatched underlying types.""",
 starter="import SwiftUI\n\n@ViewBuilder func badge(_ on: Bool) -> some View {\n    if on { Text(\"on\") } else { Image(systemName: \"xmark\") }\n}\n",
 solution="import SwiftUI\n\nfunc badge(_ on: Bool) -> some View {\n    if on { return Text(\"on\") } else { return Image(systemName: \"xmark\") }\n}\n",
 explain="""`some View` promises **one** concrete type. Two different `return` types break that promise. `@ViewBuilder` fixes it by combining both branches into `_ConditionalContent<Text, Image>` — which is why `body` (implicitly a view builder) can branch freely.""",
 hints=("An opaque return type must be the same concrete type on every path.","Return `Text` on one path and `Image` on the other with explicit `return`s.","Remove `@ViewBuilder` and use `return Text(...)` / `return Image(...)`."),
 tests=[{'name':'Mismatched opaque types','pattern':'underlying types|opaque return type'}]))
P.append(dict(id='shape-triangle', title='Custom Shape: Triangle Path', topic='Drawing', platforms=MAC, concepts=['protocols','fundamental-types'], docs=[('Shape', DOC+'shape'), ('Path', DOC+'path')],
 sig='func triangleInfo(width: Double, height: Double, points: [[Double]]) async -> [String]',
 statement="""Swiftful's *Custom Shapes*: implement `struct Triangle: Shape` whose `path(in:)` draws from top-center to bottom-right to bottom-left and closes. For the given rect size, return the path's `boundingRect` as `"w×h"` followed by `"in"`/`"out"` for each point using `path.contains(CGPoint)`.""",
 solution="""
 import SwiftUI

 struct Triangle: Shape {
     func path(in rect: CGRect) -> Path {
         var p = Path()
         p.move(to: CGPoint(x: rect.midX, y: rect.minY))
         p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
         p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
         p.closeSubpath()
         return p
     }
 }

 func triangleInfo(width: Double, height: Double, points: [[Double]]) async -> [String] {
     let path = Triangle().path(in: CGRect(x: 0, y: 0, width: width, height: height))
     let box = path.boundingRect
     return ["\\(Int(box.width))×\\(Int(box.height))"] + points.map { path.contains(CGPoint(x: $0[0], y: $0[1])) ? "in" : "out" }
 }
 """,
 explain="""A `Shape` is just a function from a rectangle to a `Path` — resolution-independent, so it adapts to any frame. Paths support hit-testing (`contains`) and geometry queries, which is how custom tappable shapes work.""",
 hints=("A `Shape` only needs `func path(in rect: CGRect) -> Path`.","Use `rect.midX`, `rect.maxX`, `rect.maxY` for the corners, then `closeSubpath()`.","`path.boundingRect` and `path.contains(CGPoint(x:y:))` answer the questions."),
 tests=[({'width':100,'height':50,'points':[[50,40],[5,5],[95,49]]},['100×50','in','out','in']), {'width':10,'height':10,'points':[]}, {'width':200,'height':100,'points':[[100,1],[0,100],[150,20]]}]))
P.append(dict(id='shape-star', title='Custom Shape: Star with N Points', topic='Drawing', diff='medium', platforms=MAC, concepts=['protocols','stride'], docs=[('Shape', DOC+'shape'), ('Path', DOC+'path')],
 sig='func starInfo(points: Int, size: Double) async -> [String]',
 statement="""Implement `struct Star: Shape { let corners: Int; let smoothness: Double }` that alternates outer points (radius = half the smaller side) and inner points (radius × smoothness), starting straight up. Return `["vertices <n>", "center in:<Bool>", "top y:<Int>"]` where vertices counts `move`+`line` elements (via `path.forEach`), and `top y` is the bounding box's `minY` rounded — or `none` for an empty path (fewer than 2 corners), whose `boundingRect` is `CGRect.null`.""",
 solution="""
 import SwiftUI

 struct Star: Shape {
     let corners: Int
     let smoothness: Double

     func path(in rect: CGRect) -> Path {
         guard corners >= 2 else { return Path() }
         let center = CGPoint(x: rect.midX, y: rect.midY)
         let outer = min(rect.width, rect.height) / 2
         var path = Path()
         for i in 0..<(corners * 2) {
             let radius = i.isMultiple(of: 2) ? outer : outer * smoothness
             let angle = Double(i) * .pi / Double(corners) - .pi / 2
             let point = CGPoint(x: center.x + radius * cos(angle), y: center.y + radius * sin(angle))
             if i == 0 { path.move(to: point) } else { path.addLine(to: point) }
         }
         path.closeSubpath()
         return path
     }
 }

 func starInfo(points: Int, size: Double) async -> [String] {
     let rect = CGRect(x: 0, y: 0, width: size, height: size)
     let path = Star(corners: points, smoothness: 0.45).path(in: rect)
     var vertices = 0
     path.forEach { element in
         switch element {
         case .move, .line: vertices += 1
         default: break
         }
     }
     // An empty path's boundingRect is CGRect.null (infinite) — never convert that to Int.
     let top = path.isEmpty ? "none" : String(Int(path.boundingRect.minY.rounded()))
     return ["vertices \\(vertices)", "center in:\\(path.contains(CGPoint(x: size / 2, y: size / 2)))", "top y:\\(top)"]
 }
 """,
 explain="""Polar coordinates (`cos`/`sin` of evenly spaced angles, starting at −π/2 for "up") generate regular shapes. `path.forEach` walks the path's elements — useful for testing or for converting paths to other formats.""",
 hints=("Place 2×corners points around the center, alternating outer and inner radius.","Angle for point i: `Double(i) * .pi / Double(corners) - .pi / 2`.","Count elements with `path.forEach { if case .move = $0 … }` or a switch."),
 tests=[({'points':5,'size':100},['vertices 10','center in:true','top y:0']), {'points':3,'size':60}, {'points':1,'size':10}, {'points':8,'size':200}]))
P.append(dict(id='shape-progress-ring', title='Arcs & trimmedPath: Progress Ring', topic='Drawing', diff='medium', platforms=MAC, concepts=['protocols'], docs=[('Path', DOC+'path'), ('Shape.trim(from:to:)', DOC+'shape/trim(from:to:)')],
 sig='func ringBounds(progress: [Double]) async -> [String]',
 statement="""A circular progress ring is a full circle **trimmed** to the progress fraction. For a 100×100 rect, build `Path(ellipseIn:)`, take `trimmedPath(from: 0, to: p)` for each progress `p`, and return its bounding box as `"x,y,w,h"` (rounded integers), or `"empty"` when nothing is drawn (an empty path's bounding box is `CGRect.null`). Note where SwiftUI starts drawing an ellipse.""",
 solution="""
 import SwiftUI

 func ringBounds(progress: [Double]) async -> [String] {
     let circle = Path(ellipseIn: CGRect(x: 0, y: 0, width: 100, height: 100))
     return progress.map { p in
         let trimmed = circle.trimmedPath(from: 0, to: min(max(p, 0), 1))
         guard !trimmed.isEmpty else { return "empty" }
         let b = trimmed.boundingRect
         return [b.minX, b.minY, b.width, b.height].map { String(Int($0.rounded())) }.joined(separator: ",")
     }
 }
 """,
 explain="""`trim(from:to:)` draws a fraction of a path's length — the basis of progress rings and "drawing" animations (animate the `to` value). An ellipse path starts at the **right-hand** point (3 o'clock), which is why rings are usually rotated −90° to start at the top.""",
 hints=("A ring is a circle path, trimmed to a fraction of its length.","`Path(ellipseIn:)` then `.trimmedPath(from: 0, to: p)`.","Round each bounding-box component and join with commas."),
 tests=[{'progress':[1,0.5,0.25]}, {'progress':[]}, {'progress':[0,0.75,1.5]}]))
P.append(dict(id='animatable-shape', title='Animatable Shapes: animatableData', topic='Animation', diff='hard', platforms=MAC, concepts=['protocols','computed-properties'], docs=[('Animatable', DOC+'animatable')],
 sig='func animateCorner(from: Double, to: Double, steps: Int) async -> [Double]',
 statement="""Swiftful's *Animate Custom Shapes with AnimatableData*: SwiftUI animates a shape by setting its `animatableData` to interpolated values each frame. Implement `struct RoundedCornerRect: Shape` with `var cornerRadius: Double` exposed through `var animatableData: Double { get set }`.

 Simulate an animation: for `t` in `0...steps` (linear), set `shape.animatableData = from + (to - from) * t / steps` and record the **path's corner radius effect**: the y-coordinate of the first point in the path (`path(in: 100×100).currentPoint`? no — use the first `.move` point's x). Return those x values rounded to 2 decimals.""",
 compare='float:1e-6',
 solution="""
 import SwiftUI

 struct RoundedCornerRect: Shape {
     var cornerRadius: Double

     var animatableData: Double {
         get { cornerRadius }
         set { cornerRadius = newValue }
     }

     func path(in rect: CGRect) -> Path {
         var p = Path()
         p.move(to: CGPoint(x: rect.minX + cornerRadius, y: rect.minY))
         p.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
         p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
         p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
         p.addLine(to: CGPoint(x: rect.minX, y: rect.minY + cornerRadius))
         p.addQuadCurve(to: CGPoint(x: rect.minX + cornerRadius, y: rect.minY), control: CGPoint(x: rect.minX, y: rect.minY))
         return p
     }
 }

 func animateCorner(from: Double, to: Double, steps: Int) async -> [Double] {
     var shape = RoundedCornerRect(cornerRadius: from)
     var xs: [Double] = []
     for t in 0...max(steps, 0) {
         shape.animatableData = steps == 0 ? to : from + (to - from) * Double(t) / Double(steps)
         var firstX = 0.0
         var found = false
         shape.path(in: CGRect(x: 0, y: 0, width: 100, height: 100)).forEach { element in
             if !found, case .move(let point) = element { firstX = point.x; found = true }
         }
         xs.append((firstX * 100).rounded() / 100)
     }
     return xs
 }
 """,
 explain="""Without `animatableData`, SwiftUI can only cross-fade a shape; with it, SwiftUI interpolates your property frame by frame and calls `path(in:)` for each value — so the geometry itself animates. For two values use `AnimatablePair`.""",
 hints=("SwiftUI animates a shape by writing interpolated values into `animatableData`.","Make `animatableData` a computed property that reads and writes `cornerRadius`.","Read the first `.move` point with `path.forEach { if case .move(let p) = $0 { … } }`."),
 tests=[({'from':0,'to':20,'steps':4},[0,5,10,15,20]), {'from':10,'to':10,'steps':2}, {'from':30,'to':0,'steps':3}, {'from':0,'to':1,'steps':0}]))
P[-1]['statement'] = P[-1]['statement'].replace("and record the **path's corner radius effect**: the y-coordinate of the first point in the path (`path(in: 100×100).currentPoint`? no — use the first `.move` point's x).", "and record where the path starts: the x-coordinate of its first `.move` point in a 100×100 rect (it equals the current corner radius).")
P.append(dict(id='animatable-pair', title='AnimatablePair & VectorArithmetic', topic='Animation', diff='medium', platforms=MAC, concepts=['protocols','generics','operator-overloading'], docs=[('AnimatablePair', DOC+'animatablepair'), ('VectorArithmetic', DOC+'vectorarithmetic')],
 sig='func interpolatePairs(_ start: [Double], _ end: [Double], _ fractions: [Double]) async -> [[Double]]',
 statement="""To animate two values at once, SwiftUI uses `AnimatablePair<A, B>`, which conforms to `VectorArithmetic` (`+`, `-`, `scale(by:)`). Implement a generic `func lerp<V: VectorArithmetic>(_ a: V, _ b: V, _ t: Double) -> V` as `a + (b − a) scaled by t`, and apply it to `AnimatablePair(start[0], start[1])` → `AnimatablePair(end[0], end[1])` for each fraction. Return `[first, second]` rounded to 3 decimals.""",
 compare='float:1e-9',
 solution="""
 import SwiftUI

 func lerp<V: VectorArithmetic>(_ a: V, _ b: V, _ t: Double) -> V {
     var delta = b - a
     delta.scale(by: t)
     return a + delta
 }

 func interpolatePairs(_ start: [Double], _ end: [Double], _ fractions: [Double]) async -> [[Double]] {
     let a = AnimatablePair(start[0], start[1])
     let b = AnimatablePair(end[0], end[1])
     return fractions.map { t in
         let v = lerp(a, b, t)
         return [v.first, v.second].map { ($0 * 1000).rounded() / 1000 }
     }
 }
 """,
 explain="""`VectorArithmetic` is the algebra SwiftUI's animation engine needs: subtract to get a delta, scale by progress, add back. `AnimatablePair` nests to animate any number of values (`AnimatablePair<CGFloat, AnimatablePair<…>>`).""",
 hints=("Interpolation is `a + (b - a) × t`, written with `VectorArithmetic` operations.","`scale(by:)` is mutating, so copy the delta into a `var` first.","`var delta = b - a; delta.scale(by: t); return a + delta`."),
 tests=[({'start':[0,100],'end':[10,50],'fractions':[0,0.5,1]},[[0,100],[5,75],[10,50]]), {'start':[1,1],'end':[1,1],'fractions':[0.3]}, {'start':[-5,0],'end':[5,1],'fractions':[0.25,0.1]}]))
P.append(dict(id='color-hex-resolve', title='Color from Hex & Resolving Components', topic='Drawing', diff='medium', platforms=MAC, concepts=['extensions','failable-init'], docs=[('Color', DOC+'color'), ('Color.Resolved', DOC+'color/resolved')],
 sig='func hexColors(_ hexes: [String]) async -> [String]',
 statement="""Swiftful's *Color, UIColor & Hex Colors*. Add `extension Color { init?(hex: String) }` accepting `"#RRGGBB"` or `"RRGGBB"` (sRGB). Resolve each color with `color.resolve(in: EnvironmentValues())` and return `"r,g,b"` as 0–255 integers, or `"invalid"`.""",
 solution="""
 import SwiftUI

 extension Color {
     init?(hex: String) {
         let digits = hex.hasPrefix("#") ? String(hex.dropFirst()) : hex
         guard digits.count == 6, let value = UInt32(digits, radix: 16) else { return nil }
         self.init(
             .sRGB,
             red: Double((value >> 16) & 0xFF) / 255,
             green: Double((value >> 8) & 0xFF) / 255,
             blue: Double(value & 0xFF) / 255
         )
     }
 }

 @MainActor func components(_ color: Color) -> String {
     let r = color.resolve(in: EnvironmentValues())
     return [r.red, r.green, r.blue].map { String(Int(($0 * 255).rounded())) }.joined(separator: ",")
 }

 func hexColors(_ hexes: [String]) async -> [String] {
     var out: [String] = []
     for hex in hexes {
         guard let color = Color(hex: hex) else { out.append("invalid"); continue }
         out.append(await components(color))
     }
     return out
 }
 """,
 explain="""`Color` is a *description* resolved against an environment (light/dark mode, color space) at render time — `resolve(in:)` exposes the concrete components (iOS 17 / macOS 14). A failable initialiser makes invalid hex strings impossible to use by accident.""",
 hints=("Parse the six hex digits with `UInt32(_, radix: 16)` and split channels with shifts and masks.","`Color(.sRGB, red:green:blue:)` builds the color; `resolve(in: EnvironmentValues())` reads it back.","Scale each resolved component by 255 and round."),
 tests=[({'hexes':['#FF8000','00ff00','#12345','zzzzzz']},['255,128,0','0,255,0','invalid','invalid']), {'hexes':[]}, {'hexes':['#000000','#FFFFFF']}]))
P.append(dict(id='binding-custom-get-set', title='Custom Bindings with get/set', topic='State & data flow', diff='medium', platforms=MAC, concepts=['closures','computed-properties','property-wrappers'], docs=[('Binding', DOC+'binding')],
 sig='func bindingDemo(_ writes: [Int]) async -> [String]',
 statement="""Swiftful's *Create custom Bindings*. Given storage in a class (`final class Store { var volume = 50 }`), create `Binding<Int>(get:set:)` whose setter **clamps** to 0…100, and a derived `Binding<Bool>` "isMuted" that reads `volume == 0` and, when set to `true`, stores 0 (setting `false` restores 50).

 Apply each write to the volume binding (negative numbers mean "set isMuted = true", `1000` means "set isMuted = false"). Return `"<volume> muted:<Bool>"` after each write.""",
 solution="""
 import SwiftUI

 final class Store: @unchecked Sendable {
     var volume = 50
 }

 @MainActor func run(_ writes: [Int]) -> [String] {
     let store = Store()
     let volume = Binding<Int>(
         get: { store.volume },
         set: { store.volume = min(max($0, 0), 100) }
     )
     let isMuted = Binding<Bool>(
         get: { volume.wrappedValue == 0 },
         set: { volume.wrappedValue = $0 ? 0 : 50 }
     )
     return writes.map { w in
         if w < 0 { isMuted.wrappedValue = true }
         else if w == 1000 { isMuted.wrappedValue = false }
         else { volume.wrappedValue = w }
         return "\\(volume.wrappedValue) muted:\\(isMuted.wrappedValue)"
     }
 }

 func bindingDemo(_ writes: [Int]) async -> [String] {
     await run(writes)
 }
 """,
 explain="""A `Binding` is just a getter/setter pair referring to storage owned elsewhere — like a controlled input's `value` + `onChange` in React. Custom bindings let you validate, derive (`isMuted` from `volume`) or adapt types without extra state.""",
 hints=("`Binding(get:set:)` takes two closures that read and write the real storage.","Clamp in the setter; the derived binding reads/writes through the first binding.","`set: { volume.wrappedValue = $0 ? 0 : 50 }` for `isMuted`."),
 tests=[({'writes':[70,150,-1,1000,-5]},['70 muted:false','100 muted:false','0 muted:true','50 muted:false','0 muted:true']), {'writes':[]}, {'writes':[0,30]}]))
P.append(dict(id='binding-keypath-projection', title='Binding Projections: $model.property', topic='State & data flow', diff='hard', platforms=MAC, concepts=['key-paths','dynamic-member-lookup'], docs=[('Binding', DOC+'binding')],
 sig='func projectionDemo(_ edits: [String]) async -> [String]',
 statement="""When you write `$profile.name`, SwiftUI uses `Binding`'s **key-path dynamic member lookup** to derive a `Binding<String>` from a `Binding<Profile>`. Create a root `Binding<Profile>` over class storage, then derive `nameBinding = root.name` and `ageBinding = root.age`. Apply edits `name=<v>` / `age=<n>` through the derived bindings and return the root's final `"name age"` plus the number of times the root setter ran.""",
 solution="""
 import SwiftUI

 struct Profile {
     var name = "anon"
     var age = 0
 }

 final class Box: @unchecked Sendable {
     var profile = Profile()
     var writes = 0
 }

 @MainActor func run(_ edits: [String]) -> [String] {
     let box = Box()
     let root = Binding<Profile>(
         get: { box.profile },
         set: { box.profile = $0; box.writes += 1 }
     )
     let nameBinding: Binding<String> = root.name
     let ageBinding: Binding<Int> = root.age
     for edit in edits {
         let p = edit.split(separator: "=").map(String.init)
         if p[0] == "name" { nameBinding.wrappedValue = p[1] }
         if p[0] == "age", let a = Int(p[1]) { ageBinding.wrappedValue = a }
     }
     return ["\\(box.profile.name) \\(box.profile.age)", "writes \\(box.writes)"]
 }

 func projectionDemo(_ edits: [String]) async -> [String] {
     await run(edits)
 }
 """,
 explain="""`root.name` is a *derived* binding: writing through it reads the whole `Profile`, changes one field, and writes the whole value back through the root setter — which is why each edit counts as one root write. That's exactly what `$model.name` passes into a `TextField`.""",
 hints=("`Binding` supports `@dynamicMemberLookup` with writable key paths.","`let nameBinding: Binding<String> = root.name` derives a child binding.","Writing to a child binding calls the **root** setter with the updated struct."),
 tests=[({'edits':['name=Ana','age=31','age=x']},['Ana 31','writes 2']), {'edits':[]}]))
P.append(dict(id='observable-tracking', title='@Observable: Fine-Grained Tracking', topic='State & data flow', diff='hard', platforms=MAC, concepts=['property-wrappers','closures'], docs=[('Observation', 'https://developer.apple.com/documentation/observation'), ('Observable()', 'https://developer.apple.com/documentation/observation/observable()')],
 sig='func trackingDemo(_ changes: [String]) async -> [String]',
 statement="""Swiftful's *@Observable Macro*. With `@Observable final class CartModel { var items: [String] = []; var coupon = ""; @ObservationIgnored var analyticsCount = 0 }`, a SwiftUI view re-renders only when a property **it read** changes.

 Simulate a view that reads only `items.count`: install `withObservationTracking({ _ = model.items.count }, onChange: …)` and re-install it **only after it fires** (as SwiftUI does when it re-renders) — installing a new tracker on every change would stack pending observers. Apply changes `add <x>`, `coupon <c>`, `track`; return how many times the "view" was notified, then the final item count.""",
 solution="""
 import Observation

 @Observable
 final class CartModel {
     var items: [String] = []
     var coupon = ""
     @ObservationIgnored var analyticsCount = 0
 }

 final class Counter: @unchecked Sendable {
     var fires = 0
     var armed = false
 }

 /// Like SwiftUI: track what `body` reads; after a change fires, re-render and track again.
 func observe(_ model: CartModel, _ counter: Counter) {
     guard !counter.armed else { return }
     counter.armed = true
     withObservationTracking {
         _ = model.items.count
     } onChange: {
         counter.fires += 1
         counter.armed = false
     }
 }

 func trackingDemo(_ changes: [String]) async -> [String] {
     let model = CartModel()
     let counter = Counter()
     for change in changes {
         observe(model, counter)
         let p = change.split(separator: " ", maxSplits: 1).map(String.init)
         switch p[0] {
         case "add": model.items.append(p.count > 1 ? p[1] : "")
         case "coupon": model.coupon = p.count > 1 ? p[1] : ""
         default: model.analyticsCount += 1
         }
     }
     return ["notified \\(counter.fires)", "items \\(model.items.count)"]
 }
 """,
 explain="""`@Observable` tracks **which properties were read** during a render, so changing `coupon` (never read) or an `@ObservationIgnored` property doesn't invalidate the view — unlike `ObservableObject`, where any `@Published` change re-renders every observer. `onChange` fires once per installation, so SwiftUI re-registers after each render.""",
 hints=("Only properties read inside the tracking closure are observed.","Read just `model.items.count`; keep an `armed` flag and re-install only after `onChange` fires.","Changing `coupon` or an `@ObservationIgnored` property doesn't fire."),
 tests=[({'changes':['add apple','coupon SAVE','track','add pear']},['notified 2','items 2']), {'changes':[]}, {'changes':['coupon X','track']}]))
P.append(dict(id='list-offsets', title='List onDelete & onMove Offsets', topic='Lists', diff='medium', platforms=MAC, concepts=['array-basics','inout'], docs=[('List', DOC+'list'), ('DynamicViewContent.onMove', DOC+'dynamicviewcontent/onmove(perform:)')],
 sig='func editList(_ items: [String], _ edits: [String]) async -> [String]',
 statement="""Swiftful's *Add, edit, move, and delete items in a List*. SwiftUI hands you an `IndexSet` for deletes and `(IndexSet, Int)` for moves; SwiftUI extends `Array` with `remove(atOffsets:)` and `move(fromOffsets:toOffset:)`.

 Edits: `del 0 2` (delete offsets 0 and 2), `move 3 0` (move offset 3 to destination 0), `move 0 2 4` (move offsets 0 and 2 to destination 4 — the destination is in terms of the **original** indices). Return the final array.""",
 solution="""
 import SwiftUI

 func editList(_ items: [String], _ edits: [String]) async -> [String] {
     var list = items
     for edit in edits {
         let p = edit.split(separator: " ")
         let numbers = p.dropFirst().compactMap { Int($0) }
         if p[0] == "del" {
             list.remove(atOffsets: IndexSet(numbers.filter { list.indices.contains($0) }))
         } else if let destination = numbers.last, numbers.count >= 2 {
             let sources = IndexSet(numbers.dropLast().filter { list.indices.contains($0) })
             list.move(fromOffsets: sources, toOffset: min(destination, list.count))
         }
     }
     return list
 }
 """,
 explain="""`move(fromOffsets:toOffset:)` interprets the destination **before** removing the moved items — so moving index 0 to offset 2 lands it after the old index 1. This matches what `List`'s drag-to-reorder reports, so you can pass the parameters straight through.""",
 hints=("SwiftUI extends `Array` with offset-based `remove` and `move`.","Build `IndexSet`s from the numbers and call `remove(atOffsets:)` / `move(fromOffsets:toOffset:)`.","For `move`, the last number is the destination; the others are sources."),
 tests=[({'items':['a','b','c','d'],'edits':['move 0 2']},['b','a','c','d']), {'items':['a','b','c','d','e'],'edits':['del 0 2','move 2 0']}, {'items':['a','b','c','d'],'edits':['move 0 2 4']}, {'items':[],'edits':['del 0']}]))
P.append(dict(id='searchable-scopes', title='Searchable Lists with Scopes', topic='Lists', platforms=MAC, concepts=['string-equality','enums','higher-order-functions'], docs=[('searchable(text:placement:prompt:)', DOC+'view/searchable(text:placement:prompt:)')],
 sig='func search(_ contacts: [[String]], query: String, scope: String) -> [String]',
 statement="""Swiftful's *Searchable, Search Suggestions, Search Scopes*. Contacts are `[name, group]` with groups `family`, `work`, `friends`. Implement the filter behind `.searchable(text:)` + `.searchScopes`: scope `all` or a group; the query matches names with `localizedStandardContains` (case- and diacritic-insensitive). An empty query returns everything in scope. Results sorted by name.""",
 solution="""
 import Foundation

 enum SearchScope: String, CaseIterable {
     case all, family, work, friends
 }

 func search(_ contacts: [[String]], query: String, scope: String) -> [String] {
     let scope = SearchScope(rawValue: scope) ?? .all
     let q = query.trimmingCharacters(in: .whitespaces)
     return contacts
         .filter { scope == .all || $0[1] == scope.rawValue }
         .filter { q.isEmpty || $0[0].localizedStandardContains(q) }
         .map { $0[0] }
         .sorted { $0.localizedStandardCompare($1) == .orderedAscending }
 }
 """,
 explain="""`localizedStandardContains` is what Finder-style search uses: case- and diacritic-insensitive (`"jose"` matches `"José"`). Keeping the filter a pure function of `(data, query, scope)` makes it trivially testable and lets the view just render.""",
 hints=("Filter by scope first, then by the query.","Use `localizedStandardContains` so case and accents don't matter.","An empty (trimmed) query matches everything in the scope."),
 tests=[({'contacts':[['José','family'],['Ana','work'],['joseph','friends']],'query':'jose','scope':'all'},['José','joseph']), {'contacts':[['José','family'],['Ana','work']],'query':'','scope':'work'}, {'contacts':[],'query':'x','scope':'all'}, {'contacts':[['Émile','work'],['emma','work'],['Bo','family']],'query':'EM','scope':'work'}]))
P.append(dict(id='sectioned-list', title='Sectioned Lists: Grouping by Letter', topic='Lists', platforms=MAC, concepts=['dictionary-basics','sort-custom'], docs=[('Section', DOC+'section')],
 sig='func sections(_ names: [String]) -> [String]',
 statement="""Prepare data for a `List` with `Section`s: group names by uppercased first letter (non-letters under `"#"`, listed last), sort sections alphabetically and names within each section case-insensitively. Return `"<letter>: <names joined by ', '>"`.""",
 solution="""
 import Foundation

 func sections(_ names: [String]) -> [String] {
     let grouped = Dictionary(grouping: names) { name -> String in
         guard let first = name.first, first.isLetter else { return "#" }
         return String(first).uppercased()
     }
     let keys = grouped.keys.sorted { ($0 == "#" ? 1 : 0, $0) < ($1 == "#" ? 1 : 0, $1) }
     return keys.map { key in
         let members = grouped[key]!.sorted { $0.localizedCaseInsensitiveCompare($1) == .orderedAscending }
         return "\\(key): \\(members.joined(separator: ", "))"
     }
 }
 """,
 explain="""`Dictionary(grouping:by:)` produces the sections; sorting keys with a tuple puts `#` last. In SwiftUI you'd `ForEach(keys, id: \\.self) { Section(key) { ForEach(grouped[key]!) … } }`.""",
 hints=("`Dictionary(grouping:by:)` builds sections from a key function.","Key: uppercased first letter, or `#` for non-letters.","Sort keys with `(isHash ? 1 : 0, key)` tuples so `#` comes last."),
 tests=[({'names':['bob','Alice','anna','42 Club','Ben']},['A: Alice, anna','B: Ben, bob','#: 42 Club']), {'names':[]}, {'names':['éclair','Zed','_x']}]))
P.append(dict(id='navigation-path', title='NavigationPath: Push, Pop & Restore', topic='Navigation', diff='medium', platforms=MAC, concepts=['codable','equatable-hashable','enums'], docs=[('NavigationPath', DOC+'navigationpath'), ('NavigationStack', DOC+'navigationstack')],
 sig='func navigate(_ commands: [String]) async -> [String]',
 statement="""Swiftful's *NavigationStack*. Model routes as `enum Route: Hashable, Codable { case profile(id: Int), settings, detail(String) }` and drive a `NavigationPath`:
 - `push profile 7`, `push settings`, `push detail x` · `pop` (if not empty) · `root` (clear)
 - `save` — encode `path.codable` to JSON and restore a new path from it, logging `"restored <count>"`

 Log `"depth <n>"` after each other command.""",
 solution="""
 import SwiftUI

 enum Route: Hashable, Codable {
     case profile(id: Int)
     case settings
     case detail(String)
 }

 @MainActor func run(_ commands: [String]) -> [String] {
     var path = NavigationPath()
     var log: [String] = []
     for command in commands {
         let p = command.split(separator: " ").map(String.init)
         switch p[0] {
         case "push" where p.count >= 2:
             switch p[1] {
             case "profile": path.append(Route.profile(id: Int(p.last!) ?? 0))
             case "settings": path.append(Route.settings)
             default: path.append(Route.detail(p.last!))
             }
         case "pop": if !path.isEmpty { path.removeLast() }
         case "root": path = NavigationPath()
         case "save":
             if let codable = path.codable,
                let data = try? JSONEncoder().encode(codable),
                let decoded = try? JSONDecoder().decode(NavigationPath.CodableRepresentation.self, from: data) {
                 path = NavigationPath(decoded)
                 log.append("restored \\(path.count)")
                 continue
             }
         default: break
         }
         log.append("depth \\(path.count)")
     }
     return log
 }

 func navigate(_ commands: [String]) async -> [String] {
     await run(commands)
 }
 """,
 explain="""`NavigationStack(path:)` renders one screen per element of the path, so navigation becomes **data** — push = append, pop = removeLast, pop-to-root = reset. Because the routes are `Codable`, `path.codable` lets you persist and restore the whole stack (state restoration, deep links).""",
 hints=("A `NavigationPath` is a type-erased list of `Hashable` route values.","`append` pushes, `removeLast()` pops, `NavigationPath()` resets.","Save with `path.codable` + `JSONEncoder`; restore with `NavigationPath(decodedRepresentation)`."),
 tests=[({'commands':['push profile 7','push settings','save','pop','root']},['depth 1','depth 2','restored 2','depth 1','depth 0']), {'commands':[]}, {'commands':['pop','push detail a','push detail b','save']}]))
P.append(dict(id='deep-link-router', title='Deep Links to Routes', topic='Navigation', diff='medium', platforms=MAC, concepts=['enums','optionals','failable-init'], docs=[('onOpenURL(perform:)', DOC+'view/onopenurl(perform:)'), ('URLComponents', 'https://developer.apple.com/documentation/foundation/urlcomponents')],
 sig='func routes(_ links: [String]) -> [String]',
 statement="""Parse deep links for `.onOpenURL` into a navigation stack. Scheme must be `myapp`. Paths: `myapp://profile/<id>` → `[profile(id)]`; `myapp://settings` → `[settings]`; `myapp://profile/<id>/posts/<postID>` → `[profile(id), post(postID)]`; query `?tab=<name>` selects a tab. Return `"<tab>: <routes joined by ' > '>"` (tab defaults to `home`) or `"invalid"`.""",
 solution="""
 import Foundation

 enum Route: CustomStringConvertible {
     case profile(Int), post(Int), settings
     var description: String {
         switch self {
         case .profile(let id): "profile(\\(id))"
         case .post(let id): "post(\\(id))"
         case .settings: "settings"
         }
     }
 }

 func parse(_ link: String) -> (tab: String, routes: [Route])? {
     guard let c = URLComponents(string: link), c.scheme == "myapp", let host = c.host else { return nil }
     let parts = [host] + c.path.split(separator: "/").map(String.init)
     let tab = c.queryItems?.first { $0.name == "tab" }?.value ?? "home"
     switch parts.count {
     case 1 where parts[0] == "settings": return (tab, [.settings])
     case 2 where parts[0] == "profile": return Int(parts[1]).map { (tab, [.profile($0)]) }
     case 4 where parts[0] == "profile" && parts[2] == "posts":
         guard let id = Int(parts[1]), let post = Int(parts[3]) else { return nil }
         return (tab, [.profile(id), .post(post)])
     default: return nil
     }
 }

 func routes(_ links: [String]) -> [String] {
     links.map { link in
         guard let r = parse(link) else { return "invalid" }
         return "\\(r.tab): \\(r.routes.map(\\.description).joined(separator: " > "))"
     }
 }
 """,
 explain="""`URLComponents` splits scheme, host, path and query items safely (no manual string slicing). For custom schemes the first segment is the **host**. Mapping URLs to an array of routes lets you set a `NavigationPath` in one assignment.""",
 hints=("`URLComponents` gives you `scheme`, `host`, `path` and `queryItems`.","For `myapp://profile/7`, `host` is `profile` and `path` is `/7`.","Switch on the number of path parts and the literal segments."),
 tests=[({'links':['myapp://profile/7','myapp://settings?tab=account','myapp://profile/3/posts/9','https://x.com','myapp://profile/abc']},['home: profile(7)','account: settings','home: profile(3) > post(9)','invalid','invalid']), {'links':[]}]))
P.append(dict(id='preference-key-reduce', title='PreferenceKey: Reducing Child Values', topic='View composition', diff='hard', platforms=MAC, concepts=['protocols','higher-order-functions','static-properties'], docs=[('PreferenceKey', DOC+'preferencekey')],
 sig='func reducePreferences(heights: [Double], titles: [String]) async -> [String]',
 statement="""Swiftful's *PreferenceKey*: children report values up the tree and SwiftUI combines them with the key's `static func reduce(value: inout Value, nextValue: () -> Value)`.

 Implement `MaxHeightKey` (default 0, keeps the max) and `TitlesKey` (default `[]`, concatenates). Simulate SwiftUI's fold: start from `defaultValue` and call `reduce` once per child value. Return `["max <h>", "titles <joined by ,>"]`.""",
 solution="""
 import SwiftUI

 struct MaxHeightKey: PreferenceKey {
     static let defaultValue: Double = 0
     static func reduce(value: inout Double, nextValue: () -> Double) {
         value = max(value, nextValue())
     }
 }

 struct TitlesKey: PreferenceKey {
     static let defaultValue: [String] = []
     static func reduce(value: inout [String], nextValue: () -> [String]) {
         value.append(contentsOf: nextValue())
     }
 }

 func fold<K: PreferenceKey>(_ key: K.Type, _ values: [K.Value]) -> K.Value {
     var result = K.defaultValue
     for v in values { K.reduce(value: &result, nextValue: { v }) }
     return result
 }

 func reducePreferences(heights: [Double], titles: [String]) async -> [String] {
     ["max \\(fold(MaxHeightKey.self, heights))", "titles \\(fold(TitlesKey.self, titles.map { [$0] }).joined(separator: ","))"]
 }
 """,
 explain="""Data normally flows *down* in SwiftUI; preferences flow *up*. A parent reads the reduced value with `.onPreferenceChange(Key.self)` — e.g. to size every column to the tallest child. `reduce` must be associative because SwiftUI folds in tree order.""",
 hints=("A `PreferenceKey` has a `defaultValue` and a `reduce(value:nextValue:)`.","Max: `value = max(value, nextValue())`; titles: `value.append(contentsOf: nextValue())`.","Fold generically: start from `K.defaultValue` and call `K.reduce(value: &result) { v }`."),
 tests=[({'heights':[20,55.5,30],'titles':['A','B']},['max 55.5','titles A,B']), {'heights':[],'titles':[]}]))
P.append(dict(id='environment-key', title='Custom Environment Values', topic='State & data flow', diff='medium', platforms=MAC, concepts=['protocols','static-properties','extensions'], docs=[('EnvironmentValues', DOC+'environmentvalues'), ('Entry()', DOC+'entry()')],
 sig='func environmentDemo(_ overrides: [String]) async -> [String]',
 statement="""Add a custom environment value the modern way: `extension EnvironmentValues { @Entry var accentName: String = "blue"; @Entry var cornerStyle: Int = 8 }`. Starting from `EnvironmentValues()`, read the defaults, apply overrides `accent=<v>` / `corner=<n>` (as `.environment(\\.accentName, …)` would), and return `"<accentName> <cornerStyle>"` before and after.""",
 solution="""
 import SwiftUI

 extension EnvironmentValues {
     @Entry var accentName: String = "blue"
     @Entry var cornerStyle: Int = 8
 }

 @MainActor func run(_ overrides: [String]) -> [String] {
     var env = EnvironmentValues()
     let before = "\\(env.accentName) \\(env.cornerStyle)"
     for o in overrides {
         let p = o.split(separator: "=").map(String.init)
         if p[0] == "accent" { env.accentName = p[1] }
         if p[0] == "corner", let n = Int(p[1]) { env.cornerStyle = n }
     }
     return [before, "\\(env.accentName) \\(env.cornerStyle)"]
 }

 func environmentDemo(_ overrides: [String]) async -> [String] {
     await run(overrides)
 }
 """,
 explain="""The `@Entry` macro (iOS 18 / Xcode 16) generates the `EnvironmentKey` boilerplate. Environment values flow **down** the view tree; `.environment(\\.accentName, "red")` overrides them for a subtree — SwiftUI's built-in dependency injection, similar to React context.""",
 hints=("`@Entry` inside `extension EnvironmentValues` declares a key and its default in one line.","Read and write the new properties on an `EnvironmentValues()` value.","`env.accentName = p[1]` applies an override."),
 tests=[({'overrides':['accent=red','corner=12']},['blue 8','red 12']), {'overrides':[]}]))
P.append(dict(id='flow-layout-rows', title='Flow Layout: Wrapping Tags into Rows', topic='Layout', diff='medium', platforms=MAC, concepts=['array-basics','higher-order-functions'], docs=[('Layout', DOC+'layout')],
 sig='func flowRows(widths: [Double], containerWidth: Double, spacing: Double) -> [[Int]]',
 statement="""A custom `Layout` for wrapping tags ("chips") needs this core algorithm in `placeSubviews`/`sizeThatFits`: place subviews left to right, starting a new row when the next one (plus spacing) wouldn't fit. A single subview wider than the container still gets its own row. Return the subview **indices** in each row.""",
 solution="""
 func flowRows(widths: [Double], containerWidth: Double, spacing: Double) -> [[Int]] {
     var rows: [[Int]] = []
     var current: [Int] = []
     var x = 0.0
     for (i, w) in widths.enumerated() {
         let needed = current.isEmpty ? w : x + spacing + w
         if !current.isEmpty && needed > containerWidth {
             rows.append(current)
             current = [i]
             x = w
         } else {
             current.append(i)
             x = needed
         }
     }
     if !current.isEmpty { rows.append(current) }
     return rows
 }
 """,
 explain="""SwiftUI's `Layout` protocol asks you to size and place subviews yourself. Keeping the row-breaking math in a pure function makes it testable; `sizeThatFits` uses it to report height, `placeSubviews` to position each subview.""",
 hints=("Walk the widths, tracking the current row's used width.","Adding a view to a non-empty row costs `spacing + width`; if that overflows, start a new row.","An empty row always accepts the next view, even if it's too wide."),
 tests=[({'widths':[40,60,30,80,20],'containerWidth':120,'spacing':8},[[0,1],[2,3],[4]]), {'widths':[],'containerWidth':100,'spacing':4}, {'widths':[200,10],'containerWidth':100,'spacing':4}, {'widths':[30,30,30],'containerWidth':100,'spacing':5}]))
P.append(dict(id='adaptive-grid-columns', title='LazyVGrid: Adaptive Column Math', topic='Layout', platforms=MAC, concepts=['fundamental-types'], docs=[('GridItem', DOC+'griditem'), ('LazyVGrid', DOC+'lazyvgrid')],
 sig='func adaptiveColumns(containerWidths: [Double], minimum: Double, spacing: Double) -> [[Double]]',
 statement="""`GridItem(.adaptive(minimum: m), spacing: s)` fits as many columns as possible: `count = max(1, floor((W + s) / (m + s)))`, and each column's width is `(W − s × (count − 1)) / count`. For each container width return `[count, width rounded to 2 decimals]`.""",
 compare='float:1e-9',
 solution="""
 func adaptiveColumns(containerWidths: [Double], minimum: Double, spacing: Double) -> [[Double]] {
     containerWidths.map { w in
         let count = max(1, ((w + spacing) / (minimum + spacing)).rounded(.down))
         let width = (w - spacing * (count - 1)) / count
         return [count, (width * 100).rounded() / 100]
     }
 }
 """,
 explain="""Adaptive grids trade a fixed column count for a minimum size, so the same grid shows 2 columns on an iPhone and 6 on an iPad. Knowing the formula helps you choose `minimum` values that avoid awkward leftover space.""",
 hints=("Each extra column costs its minimum width plus one spacing.","`count = max(1, floor((W + s) / (m + s)))`.","Then share the remaining width equally: `(W − s × (count − 1)) / count`."),
 tests=[{'containerWidths':[375,1024,80],'minimum':100,'spacing':10}, {'containerWidths':[],'minimum':50,'spacing':0}]))
P.append(dict(id='unit-curve', title='Animation Curves: Sampling UnitCurve', topic='Animation', platforms=MAC, concepts=['fundamental-types'], docs=[('UnitCurve', DOC+'unitcurve')],
 sig='func sampleCurves(_ times: [Double]) async -> [[Double]]',
 statement="""Swiftful's *Animation Curves and Animation Timing*. `UnitCurve` exposes the timing curves SwiftUI animations use. For each `t` return `[linear, easeIn, easeOut, easeInEaseOut]` values from `UnitCurve.<curve>.value(at: t)`, rounded to 3 decimals. Note which curve is ahead at `t = 0.25`.""",
 compare='float:1e-3',
 solution="""
 import SwiftUI

 func sampleCurves(_ times: [Double]) async -> [[Double]] {
     let curves: [UnitCurve] = [.linear, .easeIn, .easeOut, .easeInOut]
     return times.map { t in curves.map { ($0.value(at: t) * 1000).rounded() / 1000 } }
 }
 """,
 explain="""A timing curve maps elapsed time (0…1) to progress (0…1). `easeOut` starts fast (ahead early), `easeIn` starts slow — why `easeOut` feels responsive for things entering the screen. Springs, SwiftUI's default since iOS 17, aren't unit curves: they depend on velocity and can overshoot.""",
 hints=("`UnitCurve` has static curves like `.linear`, `.easeIn`, `.easeOut`, `.easeInOut`.","Call `curve.value(at: t)` for each time.","Round with `(x * 1000).rounded() / 1000`."),
 tests=[{'times':[0,0.25,0.5,1]}, {'times':[]}]))
P.append(dict(id='form-validation-viewmodel', title='Form Validation View Model', topic='Controls & input', diff='medium', platforms=MAC, concepts=['computed-properties','property-wrappers','guard'], docs=[('Form', DOC+'form'), ('Observation', 'https://developer.apple.com/documentation/observation')],
 sig='func signUpStates(_ edits: [String]) -> [String]',
 statement="""An `@Observable final class SignUpModel` backs a `Form` with `email`, `password`, `confirm` and `agreed`. Expose computed `errors: [String]` (in order: `"email"` if no `@`/`.` after it, `"short password"` if < 8, `"mismatch"` if password ≠ confirm, `"terms"` if not agreed) and `canSubmit`. After each edit (`email=…`, `password=…`, `confirm=…`, `agree`), return `"<canSubmit> [errors joined by ,]"`.""",
 solution="""
 import Observation

 @Observable
 final class SignUpModel {
     var email = ""
     var password = ""
     var confirm = ""
     var agreed = false

     var errors: [String] {
         var e: [String] = []
         let parts = email.split(separator: "@")
         if parts.count != 2 || !parts[1].contains(".") { e.append("email") }
         if password.count < 8 { e.append("short password") }
         if password != confirm { e.append("mismatch") }
         if !agreed { e.append("terms") }
         return e
     }

     var canSubmit: Bool { errors.isEmpty }
 }

 func signUpStates(_ edits: [String]) -> [String] {
     let model = SignUpModel()
     return edits.map { edit in
         let p = edit.split(separator: "=", maxSplits: 1).map(String.init)
         switch p[0] {
         case "email": model.email = p.count > 1 ? p[1] : ""
         case "password": model.password = p.count > 1 ? p[1] : ""
         case "confirm": model.confirm = p.count > 1 ? p[1] : ""
         default: model.agreed = true
         }
         return "\\(model.canSubmit) [\\(model.errors.joined(separator: ","))]"
     }
 }
 """,
 explain="""Derived state (errors, `canSubmit`) is computed, not stored — it can never go stale, and `@Observable` tracks the stored properties it reads. The view only binds fields and shows `errors`; the model is testable without any UI.""",
 hints=("Store only the inputs; compute errors from them.","Make `errors` a computed property that appends messages in a fixed order.","`canSubmit` is simply `errors.isEmpty`."),
 tests=[{'edits':['email=a@b.co','password=secret12','confirm=secret12','agree']}, {'edits':[]}, {'edits':['agree','email=bad']}]))
P.append(dict(id='focus-field-order', title='FocusState: Moving Between Fields', topic='Controls & input', platforms=MAC, concepts=['enums','case-iterable','optionals'], docs=[('FocusState', DOC+'focusstate')],
 sig='func focusSequence(_ actions: [String]) -> [String]',
 statement="""Swiftful's *@FocusState* and keyboard submit buttons. With `enum Field: CaseIterable { case username, email, password }` and `@FocusState var focused: Field?`, the submit button moves focus to the **next** field, and after the last field dismisses the keyboard (`nil`). Implement `next(after:)` / `previous(before:)` on `Field?` and apply actions `submit`, `back`, `tap <field>`, `dismiss`, starting unfocused (a `submit` while unfocused focuses the first field). Log the focus after each action (`"none"` for nil).""",
 solution="""
 enum Field: String, CaseIterable {
     case username, email, password
 }

 extension Optional where Wrapped == Field {
     func next() -> Field? {
         guard let current = self else { return Field.allCases.first }
         let i = Field.allCases.firstIndex(of: current)!
         return i + 1 < Field.allCases.count ? Field.allCases[i + 1] : nil
     }

     func previous() -> Field? {
         guard let current = self, let i = Field.allCases.firstIndex(of: current), i > 0 else { return self }
         return Field.allCases[i - 1]
     }
 }

 func focusSequence(_ actions: [String]) -> [String] {
     var focused: Field? = nil
     return actions.map { action in
         let p = action.split(separator: " ").map(String.init)
         switch p[0] {
         case "submit": focused = focused.next()
         case "back": focused = focused.previous()
         case "tap": focused = p.count > 1 ? Field(rawValue: p[1]) ?? focused : focused
         default: focused = nil
         }
         return focused?.rawValue ?? "none"
     }
 }
 """,
 explain="""`@FocusState` binds focus to an optional enum: `nil` means no field is focused (keyboard hidden). Keeping the "what's next" logic on the enum makes `.onSubmit { focused = focused.next() }` a one-liner.""",
 hints=("Focus is an optional enum: `nil` means nothing focused.","Use `allCases` order to find the next/previous case; past the end becomes `nil`.","Extend `Optional where Wrapped == Field` so you can call `focused.next()`."),
 tests=[({'actions':['submit','submit','back','tap password','submit','dismiss']},['username','email','username','password','none','none']), {'actions':[]}, {'actions':['back','tap nope','submit']}]))
write_all(P, 'swiftui', 100)
