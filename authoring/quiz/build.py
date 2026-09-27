"""Build content/quiz.json: the original interview MCQs plus the CS193p and non-judgeable-topic items below.

Each item: (id, topic, question, correct answer, [wrong answers], explanation, source). The correct answer's
position is shuffled deterministically by id, so it isn't always the first choice.
"""
import hashlib, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
Q = []
def q(id, topic, question, right, wrong, explain, source):
    Q.append((id, topic, question, right, wrong, explain, source))

# ---- Stanford CS193p (2025), lecture by lecture
S = 'Stanford CS193p 2025'
q('193-l1-some-view', 'CS193p', 'In `var body: some View`, what does `some View` mean?', 'body returns one specific concrete type that conforms to View; the compiler knows it, callers don\'t need to',
  ['body can return a different view type each time it runs', 'body returns an `AnyView` box', 'body is an optional view'],
  'An opaque type: one fixed concrete type (often a huge nested generic), hidden behind the protocol.', S + ' · L1')
q('193-l1-body-computed', 'CS193p', 'Why must `body` be cheap and free of side effects?', 'SwiftUI may re-evaluate it many times, whenever state it depends on changes',
  ['It runs only once, at app launch', 'It runs on a background thread', 'Xcode previews forbid side effects only in debug builds'],
  'body is a computed property that SwiftUI calls whenever it needs the view description again.', S + ' · L1')
q('193-l2-modifiers', 'CS193p', 'What does a view modifier such as `.padding()` return?', 'A new view that wraps the original (a `ModifiedContent`)',
  ['The same view instance, mutated in place', 'A copy of the view with a changed stored property', 'Nothing; it registers a style globally'],
  'Views are immutable values; modifiers build new wrapper views, which is why modifier order matters.', S + ' · L2')
q('193-l2-count-where', 'CS193p', 'What does `matches.count(where: { $0 == .exact })` avoid compared with `filter { … }.count`?', 'Allocating an intermediate array',
  ['Evaluating the closure', 'Iterating the whole array', 'Needing `Equatable`'], '`count(where:)` (Swift 6) just counts.', S + ' · L2')
q('193-l3-mvvm', 'CS193p', 'In the course\'s MVVM, who owns the game rules (e.g. scoring a guess)?', 'The Model: UI-independent Swift code',
  ['The View', 'The ViewModel only', 'SwiftUI\'s environment'], 'The Model is the "truth" and knows nothing about UI; the ViewModel interprets it for the View.', S + ' · L3')
q('193-l3-struct-model', 'CS193p', 'Why is the CodeBreaker model a `struct`?', 'Value semantics: every change is a new value, which SwiftUI can observe and reason about',
  ['Structs are required for `Codable`', 'Classes can\'t have methods', 'Structs are always faster than classes in every case'],
  'Copy-on-assign plus `mutating` makes changes explicit and observable.', S + ' · L3')
q('193-l4-mutating', 'CS193p', 'Why do model methods that change a guess need `mutating`?', 'They modify `self`, which is immutable inside non-mutating struct methods',
  ['To make them run on the main thread', 'To allow them to throw', 'To allow calling them from a class'],
  'Inside a struct method `self` is a constant unless the method is `mutating`.', S + ' · L4')
q('193-l4-enum-payload', 'CS193p', 'Why model a code\'s kind as `enum Kind { case master(isHidden: Bool), guess, attempt([Match]), unknown }`?', 'Each case carries exactly the data that makes sense for it, so impossible combinations can\'t exist',
  ['Enums use less memory than any struct', 'Associated values are required for SwiftUI', 'It lets the compiler skip exhaustiveness checks'],
  'Associated values are Swift\'s discriminated unions.', S + ' · L4')
q('193-l5-layout', 'CS193p', 'How does SwiftUI layout negotiate sizes?', 'The parent offers a size, the child chooses its own size, then the parent positions it',
  ['The child dictates the parent\'s size first', 'Every view is given exactly the screen size', 'Sizes are computed by Auto Layout constraints'],
  'Offer → choose → place. Stacks offer space to their least flexible children first.', S + ' · L5')
q('193-l5-hstack', 'CS193p', 'Which child does an HStack offer space to first?', 'The least flexible one (e.g. a fixed-size Image)',
  ['The first child in code order', 'The most flexible one (e.g. a Spacer)', 'All children at once, equally'],
  'Inflexible views take what they need, then the rest is divided among flexible views.', S + ' · L5')
q('193-l6-extension', 'CS193p', 'Why add `static func gray(_:)` to `Color` in an extension?', 'So call sites can write `.gray(0.5)` wherever a Color is expected',
  ['Because Color has no initialisers', 'Extensions can override Color\'s stored properties', 'To make Color a class'],
  'Implicit member expressions look up static members on the expected type.', S + ' · L6')
q('193-l6-binding', 'CS193p', 'What does passing `$selection` to a child view give it?', 'A Binding: read and write access to state owned elsewhere',
  ['A copy of the value', 'Ownership of the state', 'A publisher of changes'], '`$` projects a Binding from `@State`.', S + ' · L6')
q('193-l7-generics', 'CS193p', 'Why make `CodeView` generic over `AncillaryView: View`?', 'So it can show any trailing view (markers, a restart button) while keeping full type information',
  ['Generics are required for every SwiftUI view', 'To allow AnyView erasure', 'To make previews compile faster'],
  'Generic views with @ViewBuilder parameters are SwiftUI\'s typed "children" pattern.', S + ' · L7')
q('193-l7-viewbuilder', 'CS193p', 'What does `@ViewBuilder` on a closure parameter allow?', 'Writing several views, `if` and `switch` in the closure, combined into one view',
  ['Returning `AnyView` automatically', 'Running the closure on a background thread', 'Caching the view'], 'A result builder turns a list of view expressions into one view value.', S + ' · L7')
q('193-l8-animation', 'CS193p', 'What does `withAnimation { model.restart() }` animate?', 'Every view change that results from the state change inside the closure',
  ['Only views that have an `.animation` modifier', 'Nothing unless you call `.transition`', 'Only the restart button'],
  'Explicit animation: the state change is animated wherever it shows up.', S + ' · L8')
q('193-l8-transition', 'CS193p', 'When does a `.transition` apply?', 'When a view is inserted into or removed from the view hierarchy (with an animation)',
  ['Whenever any modifier value changes', 'Only on app launch', 'Whenever the device rotates'], 'Transitions are for insertion/removal, not for property changes.', S + ' · L8')
q('193-l9-time', 'CS193p', 'Why track elapsed time as `startTime` + accumulated time instead of counting timer ticks?', 'Ticks drift and stop in the background; timestamps give exact elapsed time',
  ['Timers are unavailable in SwiftUI', 'Dates are faster to compare than Ints', 'It\'s required by `Codable`'], 'Compute from timestamps; let the UI refresh with TimelineView or `Text(date, style: .timer)`.', S + ' · L9')
q('193-l10-foreach', 'CS193p', 'Which is a valid rule for `ForEach` identifiers?', 'They must be unique and stable for each item',
  ['They must be sequential integers', 'They may repeat if items look identical', 'They must be strings'], 'Identity drives diffing and animations.', S + ' · L10')
q('193-l10-index-id', 'CS193p', 'Why is `ForEach(items.indices, id: \\.self)` risky for a list you reorder?', 'Identity follows position, not the item, so state and animations attach to the wrong rows',
  ['It doesn\'t compile', 'Indices aren\'t Hashable', 'It\'s always slower'], 'Same as React\'s index-as-key bug.', S + ' · L10')
q('193-l11-splitview', 'CS193p', 'What decides whether `NavigationSplitView` shows side-by-side columns?', 'The horizontal size class (compact vs regular)',
  ['The device model name', 'The number of items in the list', 'Whether the app uses SwiftData'], 'On compact width it collapses into a stack.', S + ' · L11')
q('193-l11-sizeclass', 'CS193p', 'An iPad app in Slide Over has which horizontal size class?', 'Compact', ['Regular', 'Unspecified', 'Large'], 'Size classes describe the space available, not the device.', S + ' · L11')
q('193-l12-bindable', 'CS193p', 'What does `@Bindable` let you do with an `@Observable` model passed into a view?', 'Create bindings like `$game.name` to its properties',
  ['Own the model\'s lifetime', 'Observe it on a background thread', 'Copy it on write'], '`@Bindable` projects bindings from an observable reference.', S + ' · L12')
q('193-l12-sheet', 'CS193p', 'One editor sheet for both create and edit: what\'s the key design choice?', 'Pass it the model to edit (a new one for create) and decide how Cancel undoes changes',
  ['Write two separate views', 'Use UIKit for the sheet', 'Store the draft in UserDefaults'], 'Editing live needs a rollback strategy (copy, undo, or child context).', S + ' · L12')
q('193-l13-model-class', 'CS193p', 'Why must SwiftData `@Model` types be classes?', 'Persistent objects need identity and shared, tracked mutation',
  ['Structs can\'t be stored on disk', 'Macros only work on classes', 'Classes are required for Codable'], 'The model context tracks changes to instances.', S + ' · L13')
q('193-l13-codable-storage', 'CS193p', 'An enum with payloads doesn\'t store directly in `@Model`. What\'s a workaround shown?', 'Make it Codable (or store raw data) and keep a computed accessor',
  ['Use `NSManagedObject`', 'Store it in a global', 'SwiftData stores any enum automatically'], 'Store something the store understands; convert in code.', S + ' · L13')
q('193-l14-query', 'CS193p', 'What does `@Query` in a view give you?', 'A live, auto-updating array of models fetched from the model context',
  ['A one-time fetch at view creation', 'A publisher you must subscribe to', 'A background-thread fetch'], 'Changes in the store update the view.', S + ' · L14')
q('193-l14-predicate-limits', 'CS193p', 'Why can\'t `#Predicate` call your model\'s computed properties?', 'The predicate is translated to a store query (SQL), which can\'t run your Swift code',
  ['Computed properties are private', 'Predicates run on the main thread', 'Macros can\'t see extensions'], 'Store the value you want to filter on as a real property.', S + ' · L14')
q('193-l15-mainactor', 'CS193p', 'Where should heavy work triggered from a `@MainActor` view model run?', 'Off the main actor (e.g. a `@concurrent` or nonisolated async function), returning results to update state',
  ['Directly in the view model method', 'In `body`', 'In a `didSet`'], 'Blocking the main actor freezes the UI.', S + ' · L15')
q('193-l15-sendable', 'CS193p', 'What must values crossing from a background task to the main actor be?', 'Sendable (safe to share across concurrency domains)',
  ['Codable', 'Hashable', 'Identifiable'], 'Swift 6 checks this at compile time.', S + ' · L15')
q('193-l16-gesturestate', 'CS193p', 'What\'s special about `@GestureState`?', 'It resets to its initial value automatically when the gesture ends or is cancelled',
  ['It persists across launches', 'It can only hold Bool', 'It triggers haptics'], 'Keep committed state in `@State` and in-flight state in `@GestureState`.', S + ' · L16')
q('193-l16-geometry', 'CS193p', 'What does `GeometryReader` do to the space it\'s offered?', 'It takes all of it, and gives its content the size to compute from',
  ['It shrinks to fit its content', 'It ignores the offer', 'It always returns zero size'], 'Greedy by design, so wrap carefully inside stacks.', S + ' · L16')
q('193-l16-atomic', 'CS193p', 'Why write saved games with `.atomic`?', 'The file is written to a temporary location then swapped in, so a crash never leaves a half-written file',
  ['It compresses the data', 'It encrypts the file', 'It makes the write run on a background thread'], 'Atomic writes protect against corruption.', S + ' · L16')

# ---- Xcode & tooling
X = 'Apple developer tooling'
q('tool-scheme', 'Xcode & tooling', 'What is an Xcode *scheme*?', 'A recipe for which targets to build and how to run, test, profile and archive them',
  ['A colour theme for the editor', 'A Swift package manifest', 'The app\'s Info.plist'], 'Schemes pick build configuration, environment variables and test plans.', X)
q('tool-config', 'Xcode & tooling', 'Debug vs Release build configurations differ mainly in…', 'Optimisation level and compile-time flags like `DEBUG`',
  ['The Swift version', 'The app\'s bundle identifier, always', 'Whether SwiftUI is available'], '`#if DEBUG` checks the active compilation condition.', X)
q('tool-xcconfig', 'Xcode & tooling', 'What are `.xcconfig` files for?', 'Keeping build settings in plain text files you can review and share across targets',
  ['Storing user preferences', 'Defining Swift packages', 'Localising strings'], 'They make build settings diffable in code review.', X)
q('tool-lldb-po', 'Xcode & tooling', 'In LLDB, what\'s the difference between `po` and `p`/`v`?', '`po` evaluates an expression and prints its description; `v` reads variables without running code',
  ['They\'re identical aliases', '`po` only works for Objective-C', '`v` evaluates arbitrary Swift code'], '`v` (frame variable) is faster and has no side effects.', X)
q('tool-breakpoint', 'Xcode & tooling', 'A breakpoint that logs a message and continues without pausing is…', 'A breakpoint with a log action and "Automatically continue" enabled',
  ['Impossible; use print()', 'A symbolic breakpoint only', 'An exception breakpoint'], 'Logging breakpoints avoid rebuilding to add prints.', X)
q('tool-exception-bp', 'Xcode & tooling', 'Why add a Swift Error breakpoint?', 'To stop exactly where an error is thrown, before it\'s caught elsewhere',
  ['To silence thrown errors', 'To make all errors fatal in release', 'To log network traffic'], 'Great for tracking where a caught error originated.', X)
q('tool-preview', 'Xcode & tooling', 'What should a SwiftUI preview avoid depending on?', 'Real network, real databases and singletons with side effects; inject mocks instead',
  ['Any `@State`', 'Custom fonts', 'Multiple previews in one file'], 'Previews should be fast and deterministic.', X)
q('tool-signing', 'Xcode & tooling', 'What does code signing prove on iOS?', 'Who built the app and that it hasn\'t been modified since signing',
  ['That the app has no bugs', 'That the app was reviewed by Apple', 'That the app uses Swift 6'], 'Certificates + provisioning profiles tie a build to a team and devices.', X)
q('tool-profile', 'Xcode & tooling', 'A provisioning profile ties together…', 'An App ID, a signing certificate, entitlements and (for development) device IDs',
  ['A scheme and a test plan', 'A Git branch and a build number', 'An Info.plist and an asset catalog'], 'Automatic signing manages these for you.', X)
q('tool-symbolicate', 'Xcode & tooling', 'Why do you need dSYM files for crash reports?', 'To symbolicate: map addresses in the crash back to function names and line numbers',
  ['To sign the app', 'To enable bitcode', 'To shrink the binary'], 'Upload dSYMs to your crash reporter for readable stack traces.', X)

# ---- UIKit (not judgeable from a CLI)
U = 'UIKit'
q('uikit-lifecycle', 'UIKit', 'Which `UIViewController` method is called every time the view is about to appear?', '`viewWillAppear(_:)`',
  ['`viewDidLoad()`', '`loadView()`', '`init(coder:)`'], '`viewDidLoad` runs once per view load; `viewWillAppear` on every appearance.', U)
q('uikit-viewdidload', 'UIKit', 'Where is the one-time setup of a view controller\'s views usually done?', '`viewDidLoad()`',
  ['`viewDidAppear(_:)`', '`deinit`', '`viewWillLayoutSubviews()`'], 'Frames may not be final yet in viewDidLoad; layout-dependent work goes later.', U)
q('uikit-reuse', 'UIKit', 'Why do table and collection views *reuse* cells?', 'To avoid allocating a view per row: only the visible cells exist and get reconfigured',
  ['To cache network responses', 'Because cells can\'t be deallocated', 'To share state between rows'], 'Reset cell state in `prepareForReuse` or configuration.', U)
q('uikit-prepare-reuse', 'UIKit', 'An image from a previous row flashes in a reused cell. The classic cause?', 'An async image load finishing after the cell was reused for another row',
  ['Too many cells', 'A missing `reloadData()`', 'Auto Layout conflicts'], 'Cancel or verify the request against the current item when it completes.', U)
q('uikit-autolayout', 'UIKit', 'In Auto Layout, what does *content hugging priority* express?', 'How strongly a view resists growing larger than its intrinsic size',
  ['How strongly it resists shrinking', 'Its z-order', 'Its tap priority'], 'Compression resistance is the opposite (resisting shrinking).', U)
q('uikit-main-thread', 'UIKit', 'What happens if you update UIKit views from a background thread?', 'Undefined behaviour: glitches or crashes; UIKit must be used on the main thread',
  ['It\'s fine for labels only', 'UIKit automatically hops to the main thread', 'The update is queued until next launch'], 'Main Thread Checker flags this in debug.', U)
q('uikit-responder', 'UIKit', 'What is the responder chain?', 'The path events travel through: from the first responder up through views, controllers, window and app',
  ['The order view controllers are pushed', 'A list of notification observers', 'Auto Layout\'s constraint solver'], 'Unhandled events move up the chain.', U)
q('uikit-hosting', 'UIKit', 'How do you show a SwiftUI view inside a UIKit app?', 'Wrap it in a `UIHostingController`',
  ['Subclass `UIView` and call `body`', 'Use `UIViewRepresentable`', 'It isn\'t possible'], '`UIViewRepresentable` is the other direction (UIKit in SwiftUI).', U)
q('uikit-representable', 'UIKit', 'What is `UIViewRepresentable` for?', 'Using a UIKit view inside SwiftUI',
  ['Using SwiftUI inside UIKit', 'Converting storyboards to SwiftUI', 'Rendering UIKit off-screen'], 'Coordinate delegates through its `Coordinator`.', U)
q('uikit-delegate-weak', 'UIKit', 'Why are UIKit `delegate` properties `weak`?', 'The delegate usually owns the delegating object; a strong reference back would create a retain cycle',
  ['Weak references are faster', 'Delegates are optional', 'To allow structs as delegates'], 'e.g. a view controller owns its table view, which references it as delegate.', U)
q('uikit-coordinator', 'UIKit', 'What problem does the Coordinator pattern solve in UIKit apps?', 'It moves navigation flow out of view controllers so they don\'t know about each other',
  ['It replaces Auto Layout', 'It manages Core Data contexts', 'It reuses cells'], 'View controllers become reusable; flows become testable.', U)
q('uikit-scenes', 'UIKit', 'Since iOS 13, what owns a window\'s UI lifecycle (and allows multiple windows on iPad)?', 'The `UIScene` / `UIWindowSceneDelegate`',
  ['`UIApplicationDelegate` only', '`UIViewController`', '`UIWindow` alone'], 'App-level vs scene-level lifecycle were split.', U)

# ---- App lifecycle, background & platform
P = 'Apple platform docs'
q('life-background', 'App lifecycle', 'After your app moves to the background, what generally happens?', 'It gets a short time to finish work, then is suspended (and may be terminated to free memory)',
  ['It keeps running indefinitely', 'It\'s terminated immediately', 'It keeps full network access forever'], 'Use background tasks APIs for longer work.', P)
q('life-bgtask', 'App lifecycle', 'Which framework schedules deferrable background work like refreshes or cleanup?', 'BackgroundTasks (`BGTaskScheduler`)',
  ['CoreData', 'Combine', 'WidgetKit'], 'The system decides when to run it based on conditions.', P)
q('life-silent-push', 'App lifecycle', 'Are silent (content-available) pushes guaranteed to wake your app?', 'No, they\'re throttled by the system and never delivered if the user force-quit the app',
  ['Yes, always within one second', 'Yes, if the payload is small', 'Only on Wi-Fi'], 'Design sync so missed pushes are harmless.', P)
q('life-urlsession-bg', 'App lifecycle', 'How do you download large files that should continue after the app is suspended?', 'A background `URLSessionConfiguration`',
  ['A `Task` with high priority', 'A timer', 'A widget'], 'The system performs the transfer and relaunches your app on completion.', P)
q('life-state-restoration', 'App lifecycle', 'Which SwiftUI property wrapper stores small per-scene UI state for restoration?', '`@SceneStorage`',
  ['`@AppStorage`', '`@State`', '`@Environment`'], 'SceneStorage is per scene; AppStorage is app-wide UserDefaults.', P)
q('life-extensions', 'App lifecycle', 'Widgets, share extensions and notification service extensions run…', 'In separate processes, sharing data with the app via App Groups',
  ['Inside the app\'s process', 'Only while the app is in the foreground', 'On Apple\'s servers'], 'Use an App Group container or shared keychain.', P)

# ---- Performance & Instruments
I = 'Instruments / WWDC'
q('perf-time-profiler', 'Performance & Instruments', 'Which Instruments tool shows where CPU time goes?', 'Time Profiler',
  ['Leaks', 'Allocations', 'Network'], 'Sample stacks at intervals to find hot paths.', I)
q('perf-leaks', 'Performance & Instruments', 'A view controller never deinitialises. Which tools help find why?', 'Xcode\'s Memory Graph debugger and Instruments Leaks/Allocations',
  ['Time Profiler only', 'Energy Log', 'Core Animation FPS'], 'Look for retain cycles through closures and delegates.', I)
q('perf-hangs', 'Performance & Instruments', 'A "hang" in Apple\'s terminology is…', 'The main thread being unresponsive long enough for the user to notice (roughly 250 ms or more)',
  ['A crash on launch', 'A slow network request on a background thread', 'A memory warning'], 'Xcode Organizer and Instruments report hangs.', I)
q('perf-launch', 'Performance & Instruments', 'Which is a common cause of slow app launch?', 'Doing heavy synchronous work (I/O, big static initialisers) before the first frame',
  ['Using SwiftUI', 'Having many asset catalog images', 'Using structs'], 'Defer non-essential work until after first render.', I)
q('perf-swiftui-body', 'Performance & Instruments', 'How do you find SwiftUI views whose `body` is re-evaluated too often?', 'The SwiftUI instrument (view body counts) or `Self._printChanges()` while debugging',
  ['Leaks instrument', 'Adding `AnyView`', 'Turning on Release mode'], 'Then narrow dependencies (smaller views, @Observable).', I)
q('perf-images', 'Performance & Instruments', 'What most affects memory for images on screen?', 'Their decoded pixel size (width × height × 4 bytes)',
  ['The JPEG file size', 'The number of image views', 'The image format\'s name'], 'Downsample to display size.', I)
q('perf-energy', 'Performance & Instruments', 'Which habit drains battery the most?', 'Frequent wake-ups: polling timers, constant location updates, chatty networking',
  ['Using value types', 'Large asset catalogs', 'Dark mode'], 'Batch work and prefer push over polling.', I)
q('perf-metrickit', 'Performance & Instruments', 'What does MetricKit give you?', 'On-device performance and diagnostic reports (hangs, crashes, launch time) from real users',
  ['A UI testing framework', 'A profiler you run in Xcode only', 'Server-side logging'], 'Aggregated daily payloads delivered to your app.', I)

# ---- SPM & dependencies
M = 'swift.org / Swift Package Manager docs'
q('spm-manifest', 'Swift Package Manager', 'What is `Package.swift`?', 'The package manifest: products, targets and dependencies, written in Swift',
  ['A generated lockfile', 'An Xcode project file', 'A CocoaPods spec'], 'Like package.json, but executable Swift.', M)
q('spm-resolved', 'Swift Package Manager', 'What does `Package.resolved` do?', 'Pins the exact dependency versions that were resolved, like a lockfile',
  ['Lists your targets', 'Configures code signing', 'Stores build caches'], 'Commit it for apps so builds are reproducible.', M)
q('spm-semver', 'Swift Package Manager', '`.package(url: …, from: "2.1.0")` allows which versions?', '2.1.0 up to (but not including) 3.0.0',
  ['Exactly 2.1.0', 'Any version at all', '2.1.x only'], 'Semantic versioning: "up to next major".', M)
q('spm-local-modules', 'Swift Package Manager', 'Why split a large app into local Swift packages (modules)?', 'Faster incremental builds, enforced boundaries via access control, and isolated tests and previews',
  ['Swift requires one package per screen', 'To avoid code signing', 'To use CocoaPods'], 'Modularisation is a common senior-level lever.', M)
q('spm-plugins', 'Swift Package Manager', 'What can a SwiftPM build-tool plugin do?', 'Generate code or run tools (e.g. SwiftGen, linting) as part of the build',
  ['Replace the Swift compiler', 'Sign the app', 'Upload to TestFlight'], 'Plugins run in a sandbox during builds.', M)
q('spm-package-access', 'Swift Package Manager', 'What does the `package` access level allow?', 'Access from other modules in the same package, but not from outside it',
  ['Access only within one file', 'Access from any app that imports it', 'Access from Objective-C only'], 'Sits between internal and public.', M)

# ---- Shipping: Git, CI, TestFlight, App Store
A = 'App Store Connect / Apple docs'
q('ship-build-number', 'Shipping', 'Version (`CFBundleShortVersionString`) vs build number (`CFBundleVersion`)?', 'Version is what users see (1.4.0); the build number must increase for every upload of that version',
  ['They must always be equal', 'Build number is optional', 'Version must increase every upload'], 'CI usually sets the build number automatically.', A)
q('ship-testflight', 'Shipping', 'What\'s the difference between internal and external TestFlight testers?', 'External testers need a Beta App Review of the build; internal testers (team members) don\'t',
  ['Internal testers pay for the app', 'External testers get Xcode access', 'There is no difference'], 'Up to 10,000 external testers.', A)
q('ship-phased', 'Shipping', 'What does a phased release do?', 'Rolls an update out to automatic-update users gradually over 7 days, and can be paused',
  ['Releases one feature at a time', 'Releases to one country per day', 'Delays review'], 'Pair it with crash monitoring to catch regressions early.', A)
q('ship-review', 'Shipping', 'Which is a common App Review rejection reason?', 'Missing a way to delete an account that the app lets users create',
  ['Using SwiftUI', 'Using dark mode', 'Having more than 10 screens'], 'Account deletion has been required since 2022.', A)
q('ship-privacy-manifest', 'Shipping', 'What is a privacy manifest (`PrivacyInfo.xcprivacy`)?', 'A file declaring data your app and SDKs collect, and "required reason" APIs they use',
  ['A GDPR consent screen', 'The App Store privacy policy URL', 'An encryption key file'], 'Third-party SDKs must ship their own.', A)
q('ship-ci', 'Shipping', 'What does a typical iOS CI pipeline do on every pull request?', 'Build, run unit/UI tests, and lint; release branches also archive, sign and upload',
  ['Submit to App Review', 'Publish to the App Store', 'Rotate signing certificates'], 'Xcode Cloud, GitHub Actions, or Bitrise are common.', A)
q('ship-feature-flags', 'Shipping', 'Why do teams ship unfinished features behind flags?', 'To merge continuously and release on a schedule, turning features on remotely later',
  ['To bypass App Review', 'Because branches can\'t be merged', 'Flags make apps smaller'], 'Don\'t hide functionality from reviewers.', A)

# ---- Backend: CloudKit & Firebase
B = 'Apple / Firebase docs'
q('be-cloudkit-dbs', 'Cloud & backend', 'CloudKit\'s three database scopes are…', 'Private (per user), public (shared by all users), and shared (records shared between users)',
  ['Local, remote and cache', 'Dev, staging and prod', 'Read, write and admin'], 'Private data counts against the user\'s iCloud storage.', B)
q('be-cloudkit-coredata', 'Cloud & backend', 'What gives you automatic iCloud sync of a Core Data or SwiftData store?', '`NSPersistentCloudKitContainer` (and SwiftData\'s CloudKit option)',
  ['UserDefaults', 'Keychain sharing', 'URLCache'], 'Mind the schema rules (optional or defaulted attributes, no unique constraints).', B)
q('be-firebase-auth', 'Cloud & backend', 'With Firebase Auth, where should authorisation rules for Firestore live?', 'In Firestore Security Rules on the server, never only in the app',
  ['In the app\'s view models', 'In UserDefaults', 'In the Info.plist'], 'Clients can be modified; the server must enforce access.', B)
q('be-offline', 'Cloud & backend', 'What does Firestore\'s offline persistence give you?', 'Reads from a local cache and queued writes that sync when back online',
  ['Guaranteed conflict-free merges', 'Unlimited storage', 'End-to-end encryption'], 'Last write wins by default; design for conflicts.', B)
q('be-sign-in-apple', 'Cloud & backend', 'When must an app offer Sign in with Apple?', 'When it offers other third-party social logins for the main account (with some exceptions)',
  ['Always', 'Never; it\'s optional', 'Only for paid apps'], 'App Store Review Guideline 4.8.', B)
q('be-cursor', 'Cloud & backend', 'Why prefer cursor-based pagination for feeds?', 'Offsets skip or duplicate items when new items are inserted; cursors stay stable',
  ['Cursors are required by HTTP', 'Offsets aren\'t supported by databases', 'Cursors use less battery'], '`startAfter(lastDocument)` in Firestore.', B)

# ---- Security & privacy
C = 'Apple Platform Security'
q('sec-keychain', 'Security & privacy', 'Where should an auth token be stored?', 'In the Keychain',
  ['In UserDefaults', 'In a plist in Documents', 'Hard-coded in the binary'], 'The Keychain is encrypted and access-controlled.', C)
q('sec-ats', 'Security & privacy', 'What does App Transport Security enforce by default?', 'HTTPS with modern TLS for network connections',
  ['That all APIs are Apple\'s', 'Certificate pinning', 'End-to-end encryption'], 'Exceptions must be declared and justified.', C)
q('sec-pinning', 'Security & privacy', 'What\'s the main risk of certificate pinning?', 'A certificate rotation you didn\'t plan for can lock every installed app out of your API',
  ['It disables HTTPS', 'It leaks the private key', 'It slows every request by seconds'], 'Pin to public keys and ship backup pins.', C)
q('sec-secrets', 'Security & privacy', 'Is an API key compiled into the app a secret?', 'No: anyone can extract it from the binary, so keep real secrets on a server',
  ['Yes, binaries are encrypted', 'Yes, if obfuscated', 'Yes, on iOS only'], 'Use a backend proxy or per-user tokens.', C)
q('sec-att', 'Security & privacy', 'What does App Tracking Transparency require?', 'Asking permission before tracking users across other companies\' apps and websites',
  ['Asking permission before any analytics', 'Encrypting all data', 'Disabling crash reporting'], 'First-party analytics isn\'t "tracking" in ATT\'s sense.', C)
q('sec-secure-enclave', 'Security & privacy', 'What can the Secure Enclave do for your app?', 'Create and use private keys that can never be exported from the device',
  ['Store unlimited files', 'Run your Swift code faster', 'Encrypt network traffic automatically'], 'CryptoKit\'s `SecureEnclave.P256` keys.', C)

# ---- Testing
T = 'Swift Testing / XCTest docs'
q('test-swift-testing', 'Testing', 'In Swift Testing, how do you write an assertion?', '`#expect(value == 3)`',
  ['`XCTAssertEqual(value, 3)` only', '`assert(value == 3)`', '`expect(value).toBe(3)`'], '`#require` also stops the test when it fails.', T)
q('test-parameterized', 'Testing', 'How do you run one Swift Testing test over many inputs?', '`@Test(arguments: [...])` with a parameter',
  ['A for loop inside the test only', 'Copy the test', 'XCTest subclasses'], 'Each argument is reported as its own case.', T)
q('test-async', 'Testing', 'How do you test an `async` function?', 'Mark the test `async` and `await` the call',
  ['Use a semaphore', 'Sleep for a second', 'It can\'t be tested'], 'Both XCTest and Swift Testing support async tests.', T)
q('test-ui', 'Testing', 'What do XCUITests drive?', 'The real app, through accessibility, from a separate test process',
  ['View models directly', 'SwiftUI previews', 'The Swift compiler'], 'Good accessibility makes UI tests reliable.', T)
q('test-snapshot', 'Testing', 'What do snapshot tests catch?', 'Unintended visual changes, by comparing rendered views against reference images',
  ['Memory leaks', 'Network failures', 'Data races'], 'Record references per device and appearance.', T)
q('test-pyramid', 'Testing', 'In a healthy test pyramid for an iOS app, which tests are most numerous?', 'Fast unit tests of models and view models',
  ['UI tests', 'Manual QA scripts', 'Snapshot tests'], 'UI tests are slow and flaky; keep them few and valuable.', T)

# ---- Accessibility & localisation
L = 'Apple Human Interface Guidelines'
q('a11y-labels', 'Accessibility & localisation', 'What should an icon-only button provide for VoiceOver?', 'An accessibility label describing its action (e.g. "Delete")',
  ['Nothing; VoiceOver reads the SF Symbol name', 'A tooltip', 'A larger icon'], 'Symbol names are not user-facing language.', L)
q('a11y-tap-target', 'Accessibility & localisation', 'Apple\'s minimum recommended tap target size is…', '44×44 points', ['20×20 points', '100×100 points', '1 square centimetre'], 'Pad small controls with `contentShape`.', L)
q('a11y-reduce-motion', 'Accessibility & localisation', 'When Reduce Motion is on, what should you do?', 'Replace large movements (parallax, zooms) with fades or no animation',
  ['Disable all UI updates', 'Nothing; it\'s cosmetic', 'Increase animation speed'], 'Read `accessibilityReduceMotion` from the environment.', L)
q('l10n-catalog', 'Accessibility & localisation', 'What replaced `Localizable.strings` and `.stringsdict` files?', 'String Catalogs (`.xcstrings`), extracted automatically by Xcode',
  ['Plain JSON files', 'Swift enums of strings', 'Asset catalogs'], 'They handle plurals and device variations in one file.', L)
q('l10n-rtl', 'Accessibility & localisation', 'How should layouts handle right-to-left languages?', 'Use leading/trailing instead of left/right so the layout mirrors automatically',
  ['Reverse strings manually', 'Ship a separate RTL app', 'Nothing; iOS only supports LTR'], 'SwiftUI mirrors leading/trailing automatically.', L)

# ---- Senior staff engineering practice
E = 'Industry practice'
q('staff-module-boundaries', 'Senior engineering', 'Your app\'s build takes 10 minutes. Which change usually helps most long-term?', 'Splitting into modules with clear dependencies so builds are incremental and parallel',
  ['Switching to Objective-C', 'Removing tests', 'Using more `AnyView`'], 'Modular architecture also enforces boundaries between teams.', E)
q('staff-crash-free', 'Senior engineering', 'Which metric best summarises release stability?', 'Crash-free users (or sessions) percentage per release',
  ['Lines of code', 'Number of commits', 'App size'], 'Track it per version and roll back or hotfix quickly.', E)
q('staff-min-os', 'Senior engineering', 'What mostly decides when to raise the minimum iOS version?', 'Your user analytics (what share runs older OSes) weighed against the APIs you gain',
  ['Always support every version', 'Always require the newest version', 'Whatever the latest Xcode template uses'], 'Many teams support the current and previous major version.', E)
q('staff-rfc', 'Senior engineering', 'Before a large migration (e.g. to Swift 6 strict concurrency), a staff engineer typically…', 'Writes a proposal with the plan, risks, incremental steps and success metrics, and gets buy-in',
  ['Migrates everything in one PR', 'Waits for Apple to automate it', 'Disables the compiler checks'], 'Incremental migration by module is the norm.', E)
q('staff-server-driven', 'Senior engineering', 'What\'s the main trade-off of server-driven UI?', 'Faster iteration without app releases, versus complexity, weaker type safety and harder offline behaviour',
  ['It\'s banned by App Review', 'It always improves performance', 'It removes the need for a backend'], 'Keep native fallbacks for unknown components.', E)


def main():
    # The original 40 interview-question items live in base.json (so rebuilding never loses them).
    base = json.load(open(os.path.join(os.path.dirname(__file__), 'base.json')))
    for x in base:
        x.setdefault('topic', 'Swift fundamentals')
    items = []
    for id_, topic, question, right, wrong, explain, source in Q:
        assert len(wrong) == 3, id_
        pos = int(hashlib.sha1(id_.encode()).hexdigest(), 16) % 4
        choices = list(wrong)
        choices.insert(pos, right)
        items.append({'id': id_, 'topic': topic, 'question': question, 'choices': choices, 'answer': pos, 'explanation': explain, 'source': source})
    ids = [x['id'] for x in base + items]
    assert len(ids) == len(set(ids)), 'duplicate quiz ids'
    json.dump(base + items, open(os.path.join(ROOT, 'content', 'quiz.json'), 'w'), indent=1, ensure_ascii=False)
    print(f'{len(base)} + {len(items)} = {len(base) + len(items)} quiz items')


main()
