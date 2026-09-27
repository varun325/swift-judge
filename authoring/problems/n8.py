import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
F='https://developer.apple.com/documentation/foundation/'
AD='https://developer.apple.com/documentation/'
MAC=['darwin']
P=[]
P.append(dict(id='corelocation-distances', title='CoreLocation: Distances & Nearest Place', topic='Maps & location', platforms=MAC, concepts=['sort-custom','optionals'], docs=[('CLLocation', AD+'corelocation/cllocation')],
 sig='func nearest(from: [Double], places: [[String]]) -> [String]',
 statement="""Swiftful's *SwiftUI Map App*. Given the user's `[lat, lon]` and places `[name, lat, lon]`, compute each place's distance with `CLLocation.distance(from:)` (metres, great-circle) and return places sorted nearest-first as `"<name> <km, 1 decimal> km"`. Places with invalid coordinates (latitude outside ±90, longitude outside ±180) are skipped.""",
 solution="""
 import CoreLocation

 func nearest(from: [Double], places: [[String]]) -> [String] {
     let me = CLLocation(latitude: from[0], longitude: from[1])
     return places
         .compactMap { p -> (String, Double)? in
             guard let lat = Double(p[1]), let lon = Double(p[2]), abs(lat) <= 90, abs(lon) <= 180 else { return nil }
             return (p[0], CLLocation(latitude: lat, longitude: lon).distance(from: me))
         }
         .sorted { $0.1 < $1.1 }
         .map { "\\($0.0) \\((($0.1 / 1000) * 10).rounded() / 10) km" }
 }
 """,
 explain="""`CLLocation.distance(from:)` accounts for the Earth's curvature — never compute distances with Pythagoras on lat/lon degrees. `CLLocationCoordinate2DIsValid` does the same range check as here.""",
 hints=("Wrap coordinates in `CLLocation` and ask for `distance(from:)`.","Skip invalid coordinates with a range check, then sort by distance.","Format kilometres to one decimal place."),
 tests=[({'from':[51.5074,-0.1278],'places':[['Paris','48.8566','2.3522'],['Oxford','51.752','-1.2577'],['Nowhere','99','0']]},None), {'from':[0,0],'places':[]}], hidden=0))
P[-1]['tests'] = [{'from':[51.5074,-0.1278],'places':[['Paris','48.8566','2.3522'],['Oxford','51.752','-1.2577'],['Nowhere','99','0']]}, {'from':[0,0],'places':[]}]
P.append(dict(id='mapkit-region', title='MapKit: Regions That Fit Annotations', topic='Maps & location', diff='medium', platforms=MAC, concepts=['higher-order-functions','fundamental-types'], docs=[('MKCoordinateRegion', AD+'mapkit/mkcoordinateregion')],
 sig='func regionFor(_ points: [[Double]], padding: Double) -> [Double]',
 statement="""Compute the `MKCoordinateRegion` that fits all annotations: center = midpoint of min/max latitude and longitude; span = (max − min) × padding, with a minimum span of 0.01° each way. Return `[centerLat, centerLon, latDelta, lonDelta]` rounded to 4 decimals (build a real `MKCoordinateRegion` and read it back). Empty input → `[]`.""",
 compare='float:1e-9',
 solution="""
 import MapKit

 func regionFor(_ points: [[Double]], padding: Double) -> [Double] {
     guard !points.isEmpty else { return [] }
     let lats = points.map { $0[0] }, lons = points.map { $0[1] }
     let center = CLLocationCoordinate2D(latitude: (lats.min()! + lats.max()!) / 2, longitude: (lons.min()! + lons.max()!) / 2)
     let span = MKCoordinateSpan(
         latitudeDelta: max((lats.max()! - lats.min()!) * padding, 0.01),
         longitudeDelta: max((lons.max()! - lons.min()!) * padding, 0.01)
     )
     let region = MKCoordinateRegion(center: center, span: span)
     return [region.center.latitude, region.center.longitude, region.span.latitudeDelta, region.span.longitudeDelta]
         .map { ($0 * 10_000).rounded() / 10_000 }
 }
 """,
 explain="""A region is a center plus a span in **degrees**. Padding the span keeps pins off the screen edges; a minimum span prevents zooming absurdly far in on a single pin. (Crossing the antimeridian at ±180° needs extra care in real apps.)""",
 hints=("Find the min and max latitude and longitude.","Center = midpoints; span = (max − min) × padding, with a 0.01° floor.","Build `MKCoordinateRegion(center:span:)` and read its fields back."),
 tests=[({'points':[[51.5,-0.12],[48.85,2.35]],'padding':1.2},[50.175,1.115,3.18,2.964]), {'points':[],'padding':1}, {'points':[[10,10]],'padding':2}]))
P.append(dict(id='notificationcenter-async', title='NotificationCenter as an AsyncSequence', topic='Foundation essentials', diff='medium', platforms=MAC, concepts=['async-await','delegation'], docs=[('NotificationCenter', F+'notificationcenter'), ('NotificationCenter.notifications(named:object:)', F+'notificationcenter/notifications(named:object:)')],
 sig='func broadcast(_ messages: [String]) async -> [String]',
 statement="""Broadcast messages through a **private** `NotificationCenter()` with name `Notification.Name("chat.message")`, putting each message in `userInfo["text"]`. A listener task consumes `center.notifications(named:)` with `for await`, collecting texts until it receives `"bye"`. Post each message with a `Task.yield()` in between (after the listener has started) and return what the listener collected.""",
 solution="""
 import Foundation

 extension Notification.Name {
     static let chatMessage = Notification.Name("chat.message")
 }

 actor Inbox {
     private(set) var texts: [String] = []
     func add(_ t: String) { texts.append(t) }
 }

 func broadcast(_ messages: [String]) async -> [String] {
     let center = NotificationCenter()
     let inbox = Inbox()
     let ready = AsyncStream<Void>.makeStream()
     let listener = Task {
         let stream = center.notifications(named: .chatMessage)
         ready.continuation.yield()
         for await note in stream {
             let text = note.userInfo?["text"] as? String ?? ""
             if text == "bye" { break }
             await inbox.add(text)
         }
     }
     for await _ in ready.stream { break }
     for m in messages + ["bye"] {
         center.post(name: .chatMessage, object: nil, userInfo: ["text": m])
         try? await Task.sleep(for: .milliseconds(5))
     }
     await listener.value
     return await inbox.texts
 }
 """,
 explain="""`NotificationCenter` is a process-wide publish/subscribe bus (like an `EventEmitter`). The async `notifications(named:)` sequence replaces selector-based observers and removes itself when the loop ends. Waiting for a "ready" signal before posting avoids missing early notifications — the same subscribe-before-publish timing issue as with Combine subjects.""",
 hints=("`center.notifications(named:)` is an async sequence of notifications.","Start the listener, wait until it has created its sequence, then post.","Read `note.userInfo?[\"text\"]` and stop at `\"bye\"`."),
 tests=[({'messages':['hi','how are you']},['hi','how are you']), {'messages':[]}], hidden=0))
P.append(dict(id='file-persistence-versioned', title='Saving Codable Data to Disk (with Versions)', topic='Persistence & caching', diff='medium', platforms=MAC, concepts=['codable','file-manager','error-handling'], docs=[('Data.write(to:options:)', F+'data/write(to:options:)'), ('FileManager', F+'filemanager')],
 sig='func persistTodos(_ sessions: [[String]]) -> [String]',
 statement="""Swiftful's *Save data to FileManager*. Store `struct Store: Codable { var version: Int; var todos: [String] }` as JSON in a temporary directory, writing with `.atomic` so a crash mid-write can't corrupt the file. Each session loads the file (or starts at version 1 with no todos if missing/corrupt), applies actions `add <t>` / `done <t>` (remove), bumps `version` if anything changed, saves, and logs `"v<version>: <todos joined by ,>"`. The special action `corrupt` writes garbage to the file at the end of that session.""",
 solution="""
 import Foundation

 struct Store: Codable {
     var version: Int
     var todos: [String]
 }

 func persistTodos(_ sessions: [[String]]) -> [String] {
     let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
     try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
     defer { try? FileManager.default.removeItem(at: dir) }
     let file = dir.appendingPathComponent("store.json")
     var log: [String] = []
     for actions in sessions {
         var store = (try? JSONDecoder().decode(Store.self, from: Data(contentsOf: file))) ?? Store(version: 1, todos: [])
         var changed = false
         var corrupt = false
         for action in actions {
             let p = action.split(separator: " ", maxSplits: 1).map(String.init)
             switch p[0] {
             case "add" where p.count == 2: store.todos.append(p[1]); changed = true
             case "done" where p.count == 2:
                 if let i = store.todos.firstIndex(of: p[1]) { store.todos.remove(at: i); changed = true }
             case "corrupt": corrupt = true
             default: break
             }
         }
         if changed { store.version += 1 }
         try? JSONEncoder().encode(store).write(to: file, options: .atomic)
         log.append("v\\(store.version): \\(store.todos.joined(separator: ","))")
         if corrupt { try? Data("{not json".utf8).write(to: file) }
     }
     return log
 }
 """,
 explain="""`.atomic` writes to a temporary file and renames it into place, so readers see either the old or the new file — never half of one. Treating a corrupt or missing file as "empty" keeps the app launching; real apps also migrate old `version`s. For large or relational data, prefer SwiftData/Core Data.""",
 hints=("Encode to JSON `Data` and write it with `.atomic`.","On load, fall back to a default `Store` if the file is missing or can't be decoded.","Bump `version` only when something actually changed."),
 tests=[({'sessions':[['add milk','add eggs'],['done milk'],['corrupt'],['add jam']]},['v2: milk,eggs','v3: eggs','v3: eggs','v2: jam']), {'sessions':[]}]))
P.append(dict(id='cryptokit-hmac-aes', title='CryptoKit: HMAC Signatures & AES-GCM', topic='Security', diff='medium', platforms=MAC, concepts=['hashing','error-handling'], docs=[('CryptoKit', AD+'cryptokit'), ('HMAC', AD+'cryptokit/hmac'), ('AES.GCM', AD+'cryptokit/aes/gcm')],
 sig='func secureMessages(_ messages: [String], tamperIndex: Int) -> [String]',
 statement="""With a `SymmetricKey` derived deterministically from a password via `HKDF<SHA256>.deriveKey(inputKeyMaterial:salt:info:outputByteCount:)`:
 1. For each message, compute an HMAC-SHA256 signature and verify it with `HMAC.isValidAuthenticationCode` — log `"sig ok"` / `"sig bad"`; the message at `tamperIndex` is modified before verification.
 2. Seal each message with `AES.GCM.seal`, then open it; log the decrypted text, or `"decrypt failed"` if the sealed box was tampered (flip one byte of the combined data at `tamperIndex`).""",
 solution="""
 import CryptoKit
 import Foundation

 func secureMessages(_ messages: [String], tamperIndex: Int) -> [String] {
     let key = HKDF<SHA256>.deriveKey(
         inputKeyMaterial: SymmetricKey(data: Data("correct horse battery staple".utf8)),
         salt: Data("swift-judge".utf8),
         info: Data("demo".utf8),
         outputByteCount: 32
     )
     var log: [String] = []
     for (i, message) in messages.enumerated() {
         let signature = HMAC<SHA256>.authenticationCode(for: Data(message.utf8), using: key)
         let received = i == tamperIndex ? message + "!" : message
         log.append(HMAC<SHA256>.isValidAuthenticationCode(signature, authenticating: Data(received.utf8), using: key) ? "sig ok" : "sig bad")

         guard let sealed = try? AES.GCM.seal(Data(message.utf8), using: key), var combined = sealed.combined else { continue }
         if i == tamperIndex { combined[combined.count - 1] ^= 0xFF }
         if let box = try? AES.GCM.SealedBox(combined: combined), let plain = try? AES.GCM.open(box, using: key) {
             log.append(String(decoding: plain, as: UTF8.self))
         } else {
             log.append("decrypt failed")
         }
     }
     return log
 }
 """,
 explain="""An **HMAC** proves a message came from someone with the key and wasn't altered; **AES-GCM** encrypts *and* authenticates, so any flipped byte makes `open` fail instead of returning garbage. Derive keys with HKDF (never use a raw password), compare MACs with the constant-time helper, and store real keys in the Keychain.""",
 hints=("Derive a `SymmetricKey` with `HKDF<SHA256>.deriveKey`.","Sign with `HMAC<SHA256>.authenticationCode`; verify with `isValidAuthenticationCode`.","Seal with `AES.GCM.seal`, tamper with `combined`, then `AES.GCM.open` fails."),
 tests=[({'messages':['hello','transfer $100','bye'],'tamperIndex':1},['sig ok','hello','sig bad','decrypt failed','sig ok','bye']), {'messages':[],'tamperIndex':0}]))
P.append(dict(id='attributed-string-runs', title='AttributedString: Styling Runs', topic='Foundation essentials', diff='medium', platforms=MAC, concepts=['strings-are-collections','string-interpolation'], docs=[('AttributedString', F+'attributedstring')],
 sig='func highlight(_ text: String, terms: [String]) -> [String]',
 statement="""Paul's *Special Effects with SwiftUI Text* uses `AttributedString`. Highlight every case-insensitive occurrence of each term by setting `.inlinePresentationIntent = .stronglyEmphasized` on its range (`ranges(of:options:)`-style search via `text.range(of:options:range:)` in a loop). Then walk `attributed.runs` and return each run as `"<text>|<bold|plain>"`.""",
 solution="""
 import Foundation

 func highlight(_ text: String, terms: [String]) -> [String] {
     var attributed = AttributedString(text)
     for term in terms where !term.isEmpty {
         var searchStart = attributed.startIndex
         while searchStart < attributed.endIndex,
               let range = attributed[searchStart...].range(of: term, options: .caseInsensitive) {
             attributed[range].inlinePresentationIntent = .stronglyEmphasized
             searchStart = range.upperBound
         }
     }
     return attributed.runs.map { run in
         let piece = String(attributed[run.range].characters)
         return "\\(piece)|\\(run.inlinePresentationIntent == .stronglyEmphasized ? "bold" : "plain")"
     }
 }
 """,
 explain="""`AttributedString` is a Swift value type (unlike `NSAttributedString`) where styles are typed attributes on ranges. `runs` groups consecutive characters with identical attributes — exactly what `Text(attributed)` renders. Markdown in `Text("**bold**")` produces the same attribute.""",
 hints=("Create `AttributedString(text)` and find ranges with `range(of:options:)`.","Set `attributed[range].inlinePresentationIntent = .stronglyEmphasized`; continue searching after the range.","Map `attributed.runs` to `(text, isBold)` strings."),
 tests=[({'text':'Swift makes swift apps','terms':['swift']},['Swift|bold',' makes |plain','swift|bold',' apps|plain']), {'text':'','terms':['a']}, {'text':'no match','terms':['zzz','']}]))
P.append(dict(id='repository-pattern', title='Repository Pattern with Caching', topic='Architecture', diff='medium', platforms=MAC, concepts=['dependency-injection','protocols','caching'], docs=[('Protocols', 'https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/')],
 sig='func repositoryDemo(_ requests: [String]) async -> [String]',
 statement="""Separate **where** data comes from from **how** it's used. `protocol ArticleRemote: Sendable { func fetch(_ id: Int) async throws -> String }`. `actor ArticleRepository` takes a remote, caches successful results, and offers `func article(_ id: Int, forceRefresh: Bool) async -> Result<String, Error>`.

 A mock remote returns `"article <id> v<call#>"` and throws for id 0. Requests are `<id>` or `<id>!` (force refresh). Log each result (`"err"` for failures) then `"remote calls <n>"`.""",
 solution="""
 struct NotFound: Error {}

 protocol ArticleRemote: Sendable {
     func fetch(_ id: Int) async throws -> String
 }

 actor MockRemote: ArticleRemote {
     private(set) var calls = 0
     func fetch(_ id: Int) async throws -> String {
         calls += 1
         if id == 0 { throw NotFound() }
         return "article \\(id) v\\(calls)"
     }
 }

 actor ArticleRepository {
     private let remote: any ArticleRemote
     private var cache: [Int: String] = [:]

     init(remote: any ArticleRemote) { self.remote = remote }

     func article(_ id: Int, forceRefresh: Bool) async -> Result<String, Error> {
         if !forceRefresh, let cached = cache[id] { return .success(cached) }
         do {
             let value = try await remote.fetch(id)
             cache[id] = value
             return .success(value)
         } catch {
             return .failure(error)
         }
     }
 }

 func repositoryDemo(_ requests: [String]) async -> [String] {
     let remote = MockRemote()
     let repo = ArticleRepository(remote: remote)
     var log: [String] = []
     for r in requests {
         let force = r.hasSuffix("!")
         let id = Int(r.replacingOccurrences(of: "!", with: "")) ?? 0
         switch await repo.article(id, forceRefresh: force) {
         case .success(let a): log.append(a)
         case .failure: log.append("err")
         }
     }
     log.append("remote calls \\(await remote.calls)")
     return log
 }

 import Foundation
 """,
 explain="""A repository hides the data source (network, cache, database) behind one API, so view models don't care — and tests inject a mock remote. Making it an actor keeps the cache thread-safe. Failures aren't cached, so the next request retries.""",
 hints=("The repository depends on a protocol, not a concrete network client.","Return the cached value unless `forceRefresh`; cache only successes.","An actor keeps the cache dictionary safe under concurrency."),
 tests=[({'requests':['1','1','2','1!','0','1']},['article 1 v1','article 1 v1','article 2 v2','article 1 v3','err','article 1 v3','remote calls 4']), {'requests':[]}]))
P.append(dict(id='coordinator-router', title='Coordinator / Router for Navigation Logic', topic='Architecture', diff='medium', platforms=MAC, concepts=['enums','delegation','dependency-injection'], docs=[('NavigationStack', AD+'swiftui/navigationstack')],
 sig='func appFlow(_ events: [String]) -> [String]',
 statement="""Swiftful's *SwiftfulRouting* and SwiftUI Advanced Architecture move navigation decisions out of views. Build an `@Observable final class AppRouter` holding `var stack: [Screen]` and `var sheet: Screen?`, with `enum Screen: Hashable { case login, home, product(Int), cart, checkout, receipt }`.

 Handle events: `loggedIn` (stack = [home]), `tapProduct <id>`, `openCart` (sheet), `checkout` (dismiss sheet; push checkout — only if the cart sheet is showing), `paid` (replace stack with [home, receipt]), `back` (pop, never below 1), `logout` (stack = [login], sheet nil). Log the stack (and sheet) after each event.""",
 solution="""
 import Observation

 enum Screen: Hashable, CustomStringConvertible {
     case login, home, product(Int), cart, checkout, receipt
     var description: String {
         switch self {
         case .login: "login"
         case .home: "home"
         case .product(let id): "product\\(id)"
         case .cart: "cart"
         case .checkout: "checkout"
         case .receipt: "receipt"
         }
     }
 }

 @Observable
 final class AppRouter {
     var stack: [Screen] = [.login]
     var sheet: Screen?

     func handle(_ event: String) {
         let p = event.split(separator: " ").map(String.init)
         switch p[0] {
         case "loggedIn": stack = [.home]
         case "tapProduct": if let id = Int(p.count > 1 ? p[1] : "") { stack.append(.product(id)) }
         case "openCart": sheet = .cart
         case "checkout":
             guard sheet == .cart else { return }
             sheet = nil
             stack.append(.checkout)
         case "paid": stack = [.home, .receipt]
         case "back": if stack.count > 1 { stack.removeLast() }
         case "logout": stack = [.login]; sheet = nil
         default: break
         }
     }

     var summary: String { stack.map(\\.description).joined(separator: ">") + (sheet.map { " [\\($0)]" } ?? "") }
 }

 func appFlow(_ events: [String]) -> [String] {
     let router = AppRouter()
     return events.map { router.handle($0); return router.summary }
 }
 """,
 explain="""Centralising navigation in a router makes flows testable without UI and keeps views dumb: a view calls `router.handle(.checkout)` and a `NavigationStack(path: $router.stack)` renders the result. Rules like "checkout only from the cart" live in one place.""",
 hints=("Model screens as an enum; the router owns the stack array and the sheet.","Each event mutates the stack/sheet according to one rule.","Guard `checkout` on `sheet == .cart`."),
 tests=[({'events':['loggedIn','tapProduct 7','openCart','checkout','paid','back','back','logout']},['home','home>product7','home>product7 [cart]','home>product7>checkout','home>receipt','home','home','login']), {'events':[]}, {'events':['checkout','back']}]))
P.append(dict(id='dependency-container', title='A Tiny Dependency Container', topic='Architecture', diff='hard', platforms=MAC, concepts=['dependency-injection','generics','type-casting'], docs=[('ObjectIdentifier', 'https://developer.apple.com/documentation/swift/objectidentifier')],
 sig='func containerDemo(useMocks: Bool) -> [String]',
 statement="""Build `final class Container` that registers factories by **protocol type**: `func register<T>(_ type: T.Type, lifetime: Lifetime, factory: @escaping () -> T)` and `func resolve<T>(_ type: T.Type) -> T?`, where `Lifetime` is `.transient` (new instance each time) or `.singleton` (cached). Key the registry by `ObjectIdentifier(type)`.

 Register `AnalyticsService` (singleton) and `APIClient` (transient) — real or mock implementations depending on `useMocks`. Resolve each twice and return `[analytics name, "analytics same:<Bool>", api name, "api same:<Bool>", resolve(Unregistered.self) == nil ? "missing" : "found"]`.""",
 solution="""
 enum Lifetime { case transient, singleton }

 final class Container {
     private var factories: [ObjectIdentifier: (lifetime: Lifetime, make: () -> Any)] = [:]
     private var singletons: [ObjectIdentifier: Any] = [:]

     func register<T>(_ type: T.Type, lifetime: Lifetime, factory: @escaping () -> T) {
         factories[ObjectIdentifier(type)] = (lifetime, { factory() })
     }

     func resolve<T>(_ type: T.Type) -> T? {
         let key = ObjectIdentifier(type)
         guard let entry = factories[key] else { return nil }
         if entry.lifetime == .singleton {
             if let existing = singletons[key] as? T { return existing }
             let made = entry.make()
             singletons[key] = made
             return made as? T
         }
         return entry.make() as? T
     }
 }

 protocol AnalyticsService: AnyObject { var name: String { get } }
 protocol APIClient: AnyObject { var name: String { get } }
 protocol Unregistered {}

 final class LiveAnalytics: AnalyticsService { let name = "live analytics" }
 final class MockAnalytics: AnalyticsService { let name = "mock analytics" }
 final class LiveAPI: APIClient { let name = "live api" }
 final class MockAPI: APIClient { let name = "mock api" }

 func containerDemo(useMocks: Bool) -> [String] {
     let c = Container()
     c.register(AnalyticsService.self, lifetime: .singleton) { useMocks ? MockAnalytics() as any AnalyticsService : LiveAnalytics() }
     c.register(APIClient.self, lifetime: .transient) { useMocks ? MockAPI() as any APIClient : LiveAPI() }
     let a1 = c.resolve(AnalyticsService.self)!, a2 = c.resolve(AnalyticsService.self)!
     let p1 = c.resolve(APIClient.self)!, p2 = c.resolve(APIClient.self)!
     return [a1.name, "analytics same:\\(a1 === a2)", p1.name, "api same:\\(p1 === p2)", c.resolve(Unregistered.self) == nil ? "missing" : "found"]
 }
 """,
 explain="""Keying by `ObjectIdentifier(T.self)` lets a dictionary hold one factory per protocol; the generic `resolve` casts back. Lifetimes decide sharing. Compile-time injection (initialisers) is still preferable — containers trade type safety for convenience, which is why `resolve` returns an optional.""",
 hints=("Use `ObjectIdentifier(type)` as the dictionary key for each protocol type.","Store factories as `() -> Any` and cast back with `as? T` in `resolve`.","For singletons, cache the first instance per key."),
 tests=[({'useMocks':False},['live analytics','analytics same:true','live api','api same:false','missing']), {'useMocks':True}]))
P.append(dict(id='feature-flags', title='Feature Flags & Remote Config', topic='Architecture', platforms=MAC, concepts=['codable','enums','nil-coalescing'], docs=[('JSONDecoder', F+'jsondecoder')],
 sig='func flags(remoteJSON: String, overrides: [String], userBucket: Int) -> [String]',
 statement="""Decide feature availability with layered config: **defaults** in code, then **remote config** JSON (`{"newCheckout": {"enabled": true, "rolloutPercent": 30}, …}`), then **local overrides** (`name=on|off`, e.g. for QA). A flag with a rollout is on only if `userBucket < rolloutPercent`. Flags: `newCheckout` (default off), `darkIcons` (default on), `aiSearch` (default off). Invalid JSON means "use defaults". Return `"<flag>=<on|off> (<source>)"` for each flag in that order, source being `default`, `remote` or `override`.""",
 solution="""
 import Foundation

 enum Flag: String, CaseIterable { case newCheckout, darkIcons, aiSearch }

 struct RemoteFlag: Decodable {
     let enabled: Bool
     let rolloutPercent: Int?
 }

 func flags(remoteJSON: String, overrides: [String], userBucket: Int) -> [String] {
     let defaults: [Flag: Bool] = [.newCheckout: false, .darkIcons: true, .aiSearch: false]
     let remote = (try? JSONDecoder().decode([String: RemoteFlag].self, from: Data(remoteJSON.utf8))) ?? [:]
     let local = Dictionary(overrides.compactMap { o -> (String, Bool)? in
         let p = o.split(separator: "=").map(String.init)
         guard p.count == 2, p[1] == "on" || p[1] == "off" else { return nil }
         return (p[0], p[1] == "on")
     }, uniquingKeysWith: { _, last in last })
     return Flag.allCases.map { flag in
         if let o = local[flag.rawValue] { return "\\(flag.rawValue)=\\(o ? "on" : "off") (override)" }
         if let r = remote[flag.rawValue] {
             let on = r.enabled && userBucket < (r.rolloutPercent ?? 100)
             return "\\(flag.rawValue)=\\(on ? "on" : "off") (remote)"
         }
         return "\\(flag.rawValue)=\\(defaults[flag]! ? "on" : "off") (default)"
     }
 }
 """,
 explain="""Layering (override > remote > default) lets you ship code dark, roll out gradually, and let QA force states. Deterministic bucketing (a stable per-user number) keeps a user's experience consistent between launches. Decoding failures must degrade to safe defaults, never crash.""",
 hints=("Resolve each flag in order: local override, then remote, then default.","Decode remote config as `[String: RemoteFlag]`; invalid JSON means an empty dictionary.","Rollout: on only when `enabled && userBucket < rolloutPercent`."),
 tests=[({'remoteJSON':'{"newCheckout":{"enabled":true,"rolloutPercent":30},"darkIcons":{"enabled":false}}','overrides':['aiSearch=on'],'userBucket':12},['newCheckout=on (remote)','darkIcons=off (remote)','aiSearch=on (override)']), {'remoteJSON':'oops','overrides':[],'userBucket':50}, {'remoteJSON':'{"newCheckout":{"enabled":true,"rolloutPercent":30}}','overrides':['darkIcons=maybe'],'userBucket':30}]))
P.append(dict(id='test-doubles-spy', title='Test Doubles: Stub, Spy & Fake', topic='Testing', diff='medium', platforms=MAC, concepts=['dependency-injection','protocols'], docs=[('Swift Testing', AD+'testing'), ('XCTest', AD+'xctest')],
 sig='func checkoutTests() async -> [String]',
 statement="""Swiftful's *Unit Testing a SwiftUI application*. `final class CheckoutViewModel` depends on `protocol PaymentService { func charge(cents: Int) async throws -> String }` and `protocol Analytics { func track(_ event: String) }`. `pay(cents:)` rejects amounts ≤ 0 (tracks `"invalid_amount"`), otherwise charges, sets `receipt`, and tracks `"paid"`; on error sets `errorMessage` and tracks `"payment_failed"`.

 Write a **stub** payment service (returns a fixed receipt or throws) and a **spy** analytics (records events). Run three "tests" — success, failure, invalid — and return `"<test>: <pass|fail>"` for each, asserting on state *and* on the spy's recorded events.""",
 solution="""
 struct Declined: Error {}

 protocol PaymentService: Sendable { func charge(cents: Int) async throws -> String }
 protocol Analytics: AnyObject { func track(_ event: String) }

 @MainActor
 final class CheckoutViewModel {
     private let payments: any PaymentService
     private let analytics: any Analytics
     private(set) var receipt: String?
     private(set) var errorMessage: String?

     init(payments: any PaymentService, analytics: any Analytics) {
         self.payments = payments
         self.analytics = analytics
     }

     func pay(cents: Int) async {
         guard cents > 0 else { analytics.track("invalid_amount"); return }
         do {
             receipt = try await payments.charge(cents: cents)
             analytics.track("paid")
         } catch {
             errorMessage = "Payment failed"
             analytics.track("payment_failed")
         }
     }
 }

 struct StubPayments: PaymentService {
     let shouldFail: Bool
     func charge(cents: Int) async throws -> String {
         if shouldFail { throw Declined() }
         return "rcpt-\\(cents)"
     }
 }

 final class SpyAnalytics: Analytics {
     private(set) var events: [String] = []
     func track(_ event: String) { events.append(event) }
 }

 @MainActor func runTests() async -> [String] {
     var results: [String] = []
     do {
         let spy = SpyAnalytics()
         let vm = CheckoutViewModel(payments: StubPayments(shouldFail: false), analytics: spy)
         await vm.pay(cents: 500)
         results.append("success: \\(vm.receipt == "rcpt-500" && vm.errorMessage == nil && spy.events == ["paid"] ? "pass" : "fail")")
     }
     do {
         let spy = SpyAnalytics()
         let vm = CheckoutViewModel(payments: StubPayments(shouldFail: true), analytics: spy)
         await vm.pay(cents: 500)
         results.append("failure: \\(vm.receipt == nil && vm.errorMessage != nil && spy.events == ["payment_failed"] ? "pass" : "fail")")
     }
     do {
         let spy = SpyAnalytics()
         let vm = CheckoutViewModel(payments: StubPayments(shouldFail: false), analytics: spy)
         await vm.pay(cents: 0)
         results.append("invalid: \\(vm.receipt == nil && spy.events == ["invalid_amount"] ? "pass" : "fail")")
     }
     return results
 }

 func checkoutTests() async -> [String] {
     await runTests()
 }
 """,
 explain="""A **stub** returns canned answers (controls inputs); a **spy** records calls (lets you assert on side effects); a **fake** is a lightweight working implementation (e.g. in-memory repository). Protocol-based injection makes all three trivial — no mocking framework needed, unlike typical JS test setups.""",
 hints=("Inject protocols so tests can supply doubles.","The stub decides success or failure; the spy stores tracked events in an array.","Assert on the view model's state *and* on `spy.events` for each scenario."),
 tests=[({},['success: pass','failure: pass','invalid: pass'])], hidden=0))
P.append(dict(id='local-notification-triggers', title='Scheduling Logic for Local Notifications', topic='Platform features', diff='medium', platforms=MAC, concepts=['fundamental-types','optionals'], docs=[('UNCalendarNotificationTrigger', AD+'usernotifications/uncalendarnotificationtrigger'), ('Calendar.nextDate(after:matching:matchingPolicy:repeatedTimePolicy:direction:)', F+'calendar/nextdate(after:matching:matchingpolicy:repeatedtimepolicy:direction:)')],
 sig='func nextReminders(now: String, rules: [String]) -> [String]',
 statement="""Swiftful's *local Push Notifications*. A calendar trigger fires at the next date matching some `DateComponents`. Compute (in UTC, Gregorian) the next fire date after `now` (ISO 8601) for each rule — what `UNCalendarNotificationTrigger(dateMatching:repeats:)` would do:
 - `daily HH:mm` → hour + minute
 - `weekly <weekday 1-7> HH:mm` (1 = Sunday)
 - `monthly <day> HH:mm` (skip months without that day, e.g. the 31st)

 Return ISO 8601 dates or `"invalid"`.""",
 solution="""
 import Foundation

 func nextReminders(now: String, rules: [String]) -> [String] {
     var calendar = Calendar(identifier: .gregorian)
     calendar.timeZone = TimeZone(identifier: "UTC")!
     guard let start = try? Date(now, strategy: .iso8601) else { return rules.map { _ in "invalid" } }
     return rules.map { rule in
         let p = rule.split(separator: " ").map(String.init)
         guard let time = p.last?.split(separator: ":").compactMap({ Int($0) }), time.count == 2 else { return "invalid" }
         var components = DateComponents(hour: time[0], minute: time[1], second: 0)
         switch (p.first ?? "", p.count) {
         case ("daily", 2): break
         case ("weekly", 3): components.weekday = Int(p[1])
         case ("monthly", 3): components.day = Int(p[1])
         default: return "invalid"
         }
         guard let next = calendar.nextDate(after: start, matching: components, matchingPolicy: .strict) else { return "invalid" }
         return next.ISO8601Format()
     }
 }
 """,
 explain="""Calendar triggers match **components**, not intervals, so "every day at 9" survives DST changes. `.strict` matching skips months that lack day 31 — other policies would move to the next or previous valid day. Computing the date yourself lets you show "Next reminder: …" in the UI.""",
 hints=("Build `DateComponents` with hour/minute and optionally weekday or day.","`calendar.nextDate(after:matching:matchingPolicy:)` finds the next occurrence.","Use `.strict` so day 31 skips shorter months."),
 tests=[({'now':'2024-01-30T10:00:00Z','rules':['daily 09:00','weekly 2 08:30','monthly 31 07:00','hourly 5']},['2024-01-31T09:00:00Z','2024-02-05T08:30:00Z','2024-01-31T07:00:00Z','invalid']), {'now':'2024-02-29T23:59:00Z','rules':['monthly 30 00:00','daily 23:59']}, {'now':'bad','rules':['daily 01:00']}]))
P.append(dict(id='widget-timeline', title='WidgetKit Timeline Entries', topic='Platform features', diff='medium', platforms=MAC, concepts=['fundamental-types','higher-order-functions'], docs=[('WidgetKit', AD+'widgetkit'), ('Timeline', AD+'widgetkit/timeline')],
 sig='func timeline(now: String, events: [[String]], hours: Int) -> [String]',
 statement="""A widget can't run code on demand; you hand WidgetKit a **timeline** of entries up front. For a "next event" widget, create an entry at `now` and at every hour boundary for the next `hours` hours; each entry shows the next upcoming event (`[title, ISO date]`) at that moment, or `"free"`. Collapse consecutive entries showing the same content (keep the earlier one). Return `"<HH:mm> <title|free>"` (UTC) plus a final `"reload after <HH:mm>"` = time of the last entry + 1 hour (the `.after` reload policy).""",
 solution="""
 import Foundation

 func timeline(now: String, events: [[String]], hours: Int) -> [String] {
     var calendar = Calendar(identifier: .gregorian)
     calendar.timeZone = TimeZone(identifier: "UTC")!
     guard let start = try? Date(now, strategy: .iso8601) else { return ["invalid"] }
     let upcoming = events.compactMap { e -> (String, Date)? in
         (try? Date(e[1], strategy: .iso8601)).map { (e[0], $0) }
     }.sorted { $0.1 < $1.1 }
     let f = DateFormatter()
     f.timeZone = calendar.timeZone
     f.locale = Locale(identifier: "en_US_POSIX")
     f.dateFormat = "HH:mm"
     let firstHour = calendar.nextDate(after: start, matching: DateComponents(minute: 0), matchingPolicy: .strict) ?? start
     var moments = [start]
     for h in 0..<max(hours, 0) { moments.append(calendar.date(byAdding: .hour, value: h, to: firstHour)!) }
     var entries: [(Date, String)] = []
     for m in moments {
         let title = upcoming.first { $0.1 > m }?.0 ?? "free"
         if entries.last?.1 != title { entries.append((m, title)) }
     }
     var out = entries.map { "\\(f.string(from: $0.0)) \\($0.1)" }
     out.append("reload after \\(f.string(from: calendar.date(byAdding: .hour, value: 1, to: moments.last!)!))")
     return out
 }
 """,
 explain="""Widgets are **pre-rendered snapshots**: your `TimelineProvider` returns entries with dates, and WidgetKit swaps them in without running your app. Fewer, meaningful entries save the widget's refresh budget, and the reload policy says when to ask for more.""",
 hints=("Generate the moments: now, then each whole hour.","For each moment, the entry shows the first event still in the future.","Drop consecutive duplicates; the reload time is one hour after the last moment."),
 tests=[{'now':'2024-05-01T09:20:00Z','events':[['Standup','2024-05-01T10:00:00Z'],['Lunch','2024-05-01T12:30:00Z']],'hours':4}, {'now':'2024-05-01T09:20:00Z','events':[],'hours':2}]))
P.append(dict(id='storekit-entitlements', title='StoreKit: Subscription Entitlement Logic', topic='Platform features', diff='medium', platforms=MAC, concepts=['enums','optionals','sort-custom'], docs=[('StoreKit', AD+'storekit'), ('Transaction', AD+'storekit/transaction')],
 sig='func entitlement(now: Int, transactions: [[String]]) -> [String]',
 statement="""StoreKit 2's `Transaction.currentEntitlements` gives you verified transactions; your app decides access. Transactions are `[productID, purchasedDay, expiresDay or "-", revoked "y"/"n"]` (days as integers). A product is active if not revoked and (non-expiring or expires after `now`). Products: `pro.monthly`, `pro.yearly` (tier `pro`), `lifetime` (tier `lifetime`, non-expiring). Return the highest active tier (`lifetime` > `pro` > `free`), then the active product ids sorted, then `"renews <day>"` for the latest-expiring active subscription (or `"no renewal"`).""",
 solution="""
 enum Tier: Int, Comparable {
     case free, pro, lifetime
     static func < (a: Tier, b: Tier) -> Bool { a.rawValue < b.rawValue }
 }

 func entitlement(now: Int, transactions: [[String]]) -> [String] {
     let active = transactions.filter { t in
         guard t.count == 4, t[3] == "n" else { return false }
         return t[2] == "-" || (Int(t[2]) ?? 0) > now
     }
     let tier = active.map { t -> Tier in
         switch t[0] {
         case "lifetime": .lifetime
         case "pro.monthly", "pro.yearly": .pro
         default: .free
         }
     }.max() ?? .free
     let renew = active.compactMap { Int($0[2]) }.max()
     return ["\\(tier)", active.map { $0[0] }.sorted().joined(separator: ","), renew.map { "renews \\($0)" } ?? "no renewal"]
 }
 """,
 explain="""StoreKit verifies purchases (signed JWS); **your** code maps verified transactions to features. Checking revocation (refunds, Family Sharing changes) and expiry on every launch — and listening to `Transaction.updates` — keeps access correct without a server.""",
 hints=("Filter out revoked and expired transactions first.","Map product ids to tiers and take the maximum (`Comparable` enum).","The renewal date is the latest expiry among active subscriptions."),
 tests=[({'now':100,'transactions':[['pro.monthly','90','120','n'],['pro.yearly','10','95','n'],['lifetime','50','-','y']]},['pro','pro.monthly','renews 120']), {'now':0,'transactions':[]}, {'now':500,'transactions':[['lifetime','1','-','n'],['pro.monthly','480','510','n']]}]))
P.append(dict(id='apns-payload', title='Parsing Push Notification Payloads', topic='Platform features', diff='medium', platforms=MAC, concepts=['codable','codable-keys','optionals'], docs=[('Generating a remote notification', AD+'usernotifications/generating-a-remote-notification')],
 sig='func handlePush(_ payloads: [String]) -> [String]',
 statement="""Remote notifications arrive as JSON like `{"aps": {"alert": {"title": …, "body": …}, "badge": 3, "content-available": 1}, "deeplink": "myapp://order/42"}` — but `alert` may also be a plain **string**. Decode into a model handling both alert shapes, `content-available` (silent push when 1 and no alert), and the custom `deeplink`. Return `"<title|-> | <body|-> | badge <n|-> | <silent|visible> | <deeplink|->"` or `"invalid"`.""",
 solution="""
 import Foundation

 struct Push: Decodable {
     struct APS: Decodable {
         let title: String?
         let body: String?
         let badge: Int?
         let contentAvailable: Int?

         enum CodingKeys: String, CodingKey { case alert, badge, contentAvailable = "content-available" }
         enum AlertKeys: String, CodingKey { case title, body }

         init(from decoder: Decoder) throws {
             let c = try decoder.container(keyedBy: CodingKeys.self)
             badge = try c.decodeIfPresent(Int.self, forKey: .badge)
             contentAvailable = try c.decodeIfPresent(Int.self, forKey: .contentAvailable)
             if let text = try? c.decode(String.self, forKey: .alert) {
                 title = nil
                 body = text
             } else if let alert = try? c.nestedContainer(keyedBy: AlertKeys.self, forKey: .alert) {
                 title = try alert.decodeIfPresent(String.self, forKey: .title)
                 body = try alert.decodeIfPresent(String.self, forKey: .body)
             } else {
                 title = nil
                 body = nil
             }
         }
     }

     let aps: APS
     let deeplink: String?

     var isSilent: Bool { aps.contentAvailable == 1 && aps.title == nil && aps.body == nil }
 }

 func handlePush(_ payloads: [String]) -> [String] {
     payloads.map { json in
         guard let p = try? JSONDecoder().decode(Push.self, from: Data(json.utf8)) else { return "invalid" }
         return "\\(p.aps.title ?? "-") | \\(p.aps.body ?? "-") | badge \\(p.aps.badge.map(String.init) ?? "-") | \\(p.isSilent ? "silent" : "visible") | \\(p.deeplink ?? "-")"
     }
 }
 """,
 explain="""APNs payloads are loosely typed: `alert` can be a string or a dictionary, and keys contain hyphens. A custom `init(from:)` that tries one shape then another keeps the model strict elsewhere. Silent pushes (`content-available`, no alert) wake the app for background refresh.""",
 hints=("Try decoding `alert` as a `String` first, then as a nested container.","Map `content-available` with a custom `CodingKeys` raw value.","Silent = `content-available == 1` with no title or body."),
 tests=[({'payloads':['{"aps":{"alert":{"title":"Order","body":"Shipped"},"badge":2},"deeplink":"myapp://order/42"}','{"aps":{"alert":"Hi there"}}','{"aps":{"content-available":1}}','nope']},['Order | Shipped | badge 2 | visible | myapp://order/42','- | Hi there | badge - | visible | -','- | - | badge - | silent | -','invalid']), {'payloads':[]}]))
P.append(dict(id='firestore-cursor-paging', title='Cursor-Based Pagination (Firestore-style)', topic='Cloud & backend', diff='medium', platforms=MAC, concepts=['sort-custom','optionals'], docs=[('Firebase: Paginate data with query cursors', 'https://firebase.google.com/docs/firestore/query-data/query-cursors')],
 sig='func pagesByCursor(_ posts: [[String]], pageSize: Int) -> [String]',
 statement="""Swiftful's *Firestore Pagination*. Offsets break when new items arrive; **cursors** don't. Posts are `[id, createdAt]` (integers). Sort by `createdAt` descending then id ascending, and page with a cursor: each page takes up to `pageSize` items strictly **after** the last item of the previous page (compare the `(createdAt, id)` key). Return pages as ids joined by `,`, then `"end"`.

 To prove cursor stability, after producing the first page insert a **new** post `["new", <max createdAt + 1>]` (it sorts first) — later pages must not repeat or skip items.""",
 solution="""
 struct Post { let id: String; let createdAt: Int }

 func pagesByCursor(_ posts: [[String]], pageSize: Int) -> [String] {
     var all = posts.map { Post(id: $0[0], createdAt: Int($0[1]) ?? 0) }
     func sorted() -> [Post] { all.sorted { ($1.createdAt, $0.id) < ($0.createdAt, $1.id) } }
     func isAfter(_ p: Post, _ cursor: Post) -> Bool { (cursor.createdAt, p.id) < (p.createdAt, cursor.id) ? false : (p.createdAt < cursor.createdAt || (p.createdAt == cursor.createdAt && p.id > cursor.id)) }
     guard pageSize > 0 else { return ["end"] }
     var cursor: Post?
     var pages: [String] = []
     var inserted = false
     while true {
         let page = Array(sorted().filter { p in cursor.map { isAfter(p, $0) } ?? true }.prefix(pageSize))
         if page.isEmpty { break }
         pages.append(page.map(\\.id).joined(separator: ","))
         cursor = page.last
         if !inserted {
             inserted = true
             all.append(Post(id: "new", createdAt: (all.map(\\.createdAt).max() ?? 0) + 1))
         }
     }
     return pages + ["end"]
 }
 """,
 explain="""With offsets, inserting an item at the top shifts everything down, so page 2 repeats an item. A cursor ("start after this document") is anchored to data, not position — which is why Firestore, GraphQL connections and most feeds use it. Ties need a secondary key (here the id) to make the order total.""",
 hints=("Order by `(createdAt desc, id asc)` so the order is total.","Each page takes items strictly after the previous page's last item.","Insert the new post after page 1 and check nothing repeats."),
 tests=[({'posts':[['a','5'],['b','9'],['c','5'],['d','7'],['e','1']],'pageSize':2},['b,d','a,c','e','end']), {'posts':[],'pageSize':3}, {'posts':[['x','1']],'pageSize':0}]))
P.append(dict(id='auth-state-machine', title='Authentication State Machine', topic='Cloud & backend', diff='medium', platforms=MAC, concepts=['enums','associated-values','switch-statement'], docs=[('Firebase Authentication for Apple platforms', 'https://firebase.google.com/docs/auth/ios/start'), ('Sign in with Apple', AD+'sign_in_with_apple')],
 sig='func authFlow(_ events: [String]) -> [String]',
 statement="""Swiftful's Firebase Authentication series. Model `enum AuthState { case signedOut, signingIn(method: String), signedIn(userID: String, isAnonymous: Bool), failed(String) }` with a transition function. Events: `start <email|google|apple|anonymous>`, `success <uid>`, `failure <reason>`, `link <uid>` (upgrade an anonymous user to a permanent account, keeping the same uid — only valid when anonymous), `signOut`, `delete` (only when signed in → signedOut). Invalid transitions leave the state unchanged and log `"ignored"`. Log the state after each event.""",
 solution="""
 enum AuthState: CustomStringConvertible {
     case signedOut
     case signingIn(method: String)
     case signedIn(userID: String, isAnonymous: Bool)
     case failed(String)

     var description: String {
         switch self {
         case .signedOut: "signedOut"
         case .signingIn(let m): "signingIn(\\(m))"
         case let .signedIn(uid, anon): "signedIn(\\(uid)\\(anon ? ", anonymous" : ""))"
         case .failed(let r): "failed(\\(r))"
         }
     }

     func handling(_ event: String) -> AuthState? {
         let p = event.split(separator: " ").map(String.init)
         let arg = p.count > 1 ? p[1] : ""
         switch (self, p.first ?? "") {
         case (.signedOut, "start"), (.failed, "start"): return .signingIn(method: arg)
         case (.signingIn(let method), "success"): return .signedIn(userID: arg, isAnonymous: method == "anonymous")
         case (.signingIn, "failure"): return .failed(arg)
         case (.signedIn(let uid, true), "link"): return .signedIn(userID: uid, isAnonymous: false)
         case (.signedIn, "signOut"), (.signedIn, "delete"), (.failed, "signOut"): return .signedOut
         default: return nil
         }
     }
 }

 func authFlow(_ events: [String]) -> [String] {
     var state = AuthState.signedOut
     return events.map { event in
         guard let next = state.handling(event) else { return "ignored" }
         state = next
         return state.description
     }
 }
 """,
 explain="""Auth is a state machine; modelling it as an enum with associated values makes illegal states (signed in *and* failed) unrepresentable, and a pattern-matching `switch` over `(state, event)` documents every legal transition. Anonymous → linked accounts keep the same user id, so their data survives the upgrade.""",
 hints=("Switch on `(currentState, eventName)` and return the next state or nil.","Pattern-match associated values: `case (.signedIn(let uid, true), \"link\")`.","Log `\"ignored\"` when the transition isn't legal."),
 tests=[({'events':['start anonymous','success u1','link x','signOut','start google','failure cancelled','start email','success u2','delete','delete']},['signingIn(anonymous)','signedIn(u1, anonymous)','signedIn(u1)','signedOut','signingIn(google)','failed(cancelled)','signingIn(email)','signedIn(u2)','signedOut','ignored']), {'events':[]}, {'events':['success x','link y']}]))
P.append(dict(id='health-step-aggregation', title='Aggregating Samples by Day (HealthKit-style)', topic='Platform features', diff='medium', platforms=MAC, concepts=['dictionary-basics','fundamental-types'], docs=[('HealthKit', AD+'healthkit'), ('HKStatisticsCollectionQuery', AD+'healthkit/hkstatisticscollectionquery')],
 sig='func dailySteps(_ samples: [[String]], timeZone: String) -> [String]',
 statement="""HealthKit returns step samples as intervals; charts need **per-day totals in the user's time zone**. Each sample is `[startISO, count]`. Group by calendar day in the given zone (not UTC!), sum counts, and fill missing days between the first and last with 0. Return `"yyyy-MM-dd <total>"` lines. This is what `HKStatisticsCollectionQuery` does with an anchor date and a 1-day interval.""",
 solution="""
 import Foundation

 func dailySteps(_ samples: [[String]], timeZone: String) -> [String] {
     var calendar = Calendar(identifier: .gregorian)
     guard let zone = TimeZone(identifier: timeZone) else { return ["invalid zone"] }
     calendar.timeZone = zone
     var totals: [Date: Int] = [:]
     for s in samples {
         guard let date = try? Date(s[0], strategy: .iso8601), let n = Int(s[1]) else { continue }
         totals[calendar.startOfDay(for: date), default: 0] += n
     }
     guard let first = totals.keys.min(), let last = totals.keys.max() else { return [] }
     let f = DateFormatter()
     f.calendar = calendar
     f.timeZone = zone
     f.locale = Locale(identifier: "en_US_POSIX")
     f.dateFormat = "yyyy-MM-dd"
     var out: [String] = []
     var day = first
     while day <= last {
         out.append("\\(f.string(from: day)) \\(totals[day] ?? 0)")
         day = calendar.date(byAdding: .day, value: 1, to: day)!
     }
     return out
 }
 """,
 explain=""""Which day did this happen?" depends on the time zone: a 23:30 UTC walk is *tomorrow* in Kolkata. `startOfDay(for:)` in the user's calendar is the right bucket key; filling gaps with zero keeps charts honest.""",
 hints=("Bucket each sample by `calendar.startOfDay(for:)` in the given time zone.","Sum counts per bucket in a dictionary.","Walk day by day from the first to the last bucket, filling missing days with 0."),
 tests=[({'samples':[['2024-05-01T23:30:00Z','100'],['2024-05-02T08:00:00Z','50'],['2024-05-04T10:00:00Z','20']],'timeZone':'Asia/Kolkata'},['2024-05-02 150','2024-05-03 0','2024-05-04 20']), {'samples':[['2024-05-01T23:30:00Z','100'],['2024-05-02T08:00:00Z','50']],'timeZone':'UTC'}, {'samples':[],'timeZone':'UTC'}]))
P.append(dict(id='chart-binning', title='Binning Data for Swift Charts', topic='Platform features', platforms=MAC, concepts=['dictionary-basics','higher-order-functions'], docs=[('Swift Charts', AD+'charts')],
 sig='func histogram(_ values: [Double], binWidth: Double) -> [String]',
 statement="""Swift Charts draws what you give it — preparing data is your job. Bin values into half-open buckets `[k×w, (k+1)×w)` and return `"<start>-<end>: <count>"` for every bucket from the lowest to the highest non-empty one (including empty buckets in between), with bounds formatted without trailing `.0` for whole numbers.""",
 solution="""
 func histogram(_ values: [Double], binWidth w: Double) -> [String] {
     guard w > 0, !values.isEmpty else { return [] }
     var counts: [Int: Int] = [:]
     for v in values { counts[Int((v / w).rounded(.down)), default: 0] += 1 }
     let lo = counts.keys.min()!, hi = counts.keys.max()!
     func fmt(_ x: Double) -> String { x == x.rounded() ? String(Int(x)) : String(x) }
     return (lo...hi).map { k in "\\(fmt(Double(k) * w))-\\(fmt(Double(k + 1) * w)): \\(counts[k] ?? 0)" }
 }
 """,
 explain="""Charts should show empty bins (a gap *is* information). `floor(v / w)` assigns the bucket; negative values work too because `.down` rounds toward −∞. In Swift Charts you'd feed these as `BarMark(x: .value("Range", label), y: .value("Count", n))`.""",
 hints=("Bucket index = `floor(value / width)`.","Count per bucket, then emit every bucket from min to max.","Format whole-number bounds without `.0`."),
 tests=[({'values':[1,2.5,7,9.9,10],'binWidth':5},['0-5: 2','5-10: 2','10-15: 1']), {'values':[],'binWidth':1}, {'values':[-1.5,0.2],'binWidth':0.5}]))
P.append(dict(id='image-cache-two-tier', title='Two-Tier Image Cache: Memory + Disk', topic='Persistence & caching', diff='hard', platforms=MAC, concepts=['caching','file-manager','actors'], docs=[('NSCache', F+'nscache'), ('FileManager', F+'filemanager')],
 sig='func twoTierCache(_ requests: [String]) async -> [String]',
 statement="""Swiftful's *Save and cache images in a SwiftUI app* + Crypto App's image service. `actor ImageStore` checks **memory** (`NSCache`), then **disk** (files in a temp folder named by the key), then **network** (a fake downloader returning `"img:<key>"`), filling the faster tiers on the way back. Requests: `get <key>`, `purge-memory` (simulates an app relaunch — memory empty, disk intact), `purge-disk`. Log the tier that served each `get` (`memory`/`disk`/`network`), then `"downloads <n>"`.""",
 solution="""
 import Foundation

 final class Box { let value: String; init(_ v: String) { value = v } }

 actor ImageStore {
     private let memory = NSCache<NSString, Box>()
     private let folder: URL
     private(set) var downloads = 0

     init() {
         folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
         try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
     }

     func image(_ key: String) async -> (String, String) {
         if let hit = memory.object(forKey: key as NSString) { return (hit.value, "memory") }
         let file = folder.appendingPathComponent(key)
         if let data = try? Data(contentsOf: file) {
             let value = String(decoding: data, as: UTF8.self)
             memory.setObject(Box(value), forKey: key as NSString)
             return (value, "disk")
         }
         downloads += 1
         let value = "img:\\(key)"
         try? Data(value.utf8).write(to: file, options: .atomic)
         memory.setObject(Box(value), forKey: key as NSString)
         return (value, "network")
     }

     func purgeMemory() { memory.removeAllObjects() }
     func purgeDisk() {
         try? FileManager.default.removeItem(at: folder)
         try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
     }
     func cleanup() { try? FileManager.default.removeItem(at: folder) }
 }

 func twoTierCache(_ requests: [String]) async -> [String] {
     let store = ImageStore()
     var log: [String] = []
     for r in requests {
         let p = r.split(separator: " ").map(String.init)
         switch p[0] {
         case "get" where p.count == 2: log.append(await store.image(p[1]).1)
         case "purge-memory": await store.purgeMemory()
         case "purge-disk": await store.purgeDisk()
         default: break
         }
     }
     log.append("downloads \\(await store.downloads)")
     await store.cleanup()
     return log
 }
 """,
 explain="""Memory is fastest but lost on relaunch or pressure; disk survives relaunches; the network is slowest. Checking tiers in order and back-filling faster tiers on a miss is the classic image-loading design (Kingfisher and SDWebImage, from Swiftful's package videos, do exactly this).""",
 hints=("Check memory, then disk, then the network, in that order.","On a disk hit, put the value into memory; on a network hit, write to both.","Purging memory simulates a relaunch: the next `get` should hit disk."),
 tests=[({'requests':['get a','get a','purge-memory','get a','get b','purge-disk','purge-memory','get a']},['network','memory','disk','network','network','downloads 3']), {'requests':[]}]))
P.append(dict(id='accessibility-labels', title='Accessibility Labels from Data', topic='Accessibility', platforms=MAC, concepts=['string-interpolation','optionals'], docs=[('Accessibility for SwiftUI', AD+'swiftui/view-accessibility'), ('accessibilityLabel(_:)', AD+'swiftui/view/accessibilitylabel(_:)-1d7jv')],
 sig='func a11yLabels(_ rows: [[String]]) -> [String]',
 statement="""Swiftful's *Accessibility: Voice Over*. A product row visually shows `★★★★☆ 4.2`, `$19.99` and a `🔥` badge — VoiceOver would read that as gibberish. Build a spoken label: `"<name>, <price> dollars, rated <rating> out of 5 stars<, bestseller>"`. Rows are `[name, priceCents, rating, isBestseller "y"/"n"]`; ratings render with one decimal; prices say `"<dollars> dollars <cents> cents"` (omit cents when 0, singular `dollar`/`cent` for 1).""",
 solution="""
 func a11yLabels(_ rows: [[String]]) -> [String] {
     rows.map { r in
         let cents = Int(r[1]) ?? 0
         let d = cents / 100, c = cents % 100
         var price = "\\(d) \\(d == 1 ? "dollar" : "dollars")"
         if c > 0 { price += " \\(c) \\(c == 1 ? "cent" : "cents")" }
         let rating = ((Double(r[2]) ?? 0) * 10).rounded() / 10
         return "\\(r[0]), \\(price), rated \\(rating) out of 5 stars\\(r[3] == "y" ? ", bestseller" : "")"
     }
 }
 """,
 explain="""Accessibility labels describe **meaning**, not visuals: combine a row's pieces with `.accessibilityElement(children: .combine)` or give it one `.accessibilityLabel`. Pluralisation and number reading matter — `Text` with `inflect: true` markdown can pluralise automatically in localised apps.""",
 hints=("Describe meaning, not symbols: stars → \"rated 4.2 out of 5\".","Split cents into dollars and cents, handling singular and zero cents.","Append \", bestseller\" only when flagged."),
 tests=[({'rows':[['Mug','1999','4.24','y'],['Pen','100','5','n'],['Card','101','0','n']]},['Mug, 19 dollars 99 cents, rated 4.2 out of 5 stars, bestseller','Pen, 1 dollar, rated 5.0 out of 5 stars','Card, 1 dollar 1 cent, rated 0.0 out of 5 stars']), {'rows':[]}]))
write_all(P, 'frameworks', 500)
