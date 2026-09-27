import re
# (topic id, area, label, regex) — first match wins; order from specific to general.
T = [
 ('lang-evolution','Swift language',"What's new in Swift (evolution)", r"(what'?s new in swift|swift \d\.\d+|swift 6|swift evolution|swift 5)"),
 ('lang-concurrency','Swift language','Concurrency: async/await, tasks, actors, Sendable', r'\b(async|await|concurrency|actors?|task ?groups?|tasks?\b|sendable|mainactor|continuations?|asyncstream|asyncsequence|isolation|data races?|gcd|grand central|dispatch|threads?|multi-threading)\b'),
 ('fw-combine','Frameworks','Combine: publishers & subscribers', r'\b(combine|publishers?|subscribers?|@published|sink|futures?|promises?|passthrough|currentvalue)\b'),
 ('fw-persistence','Frameworks','Persistence: UserDefaults, FileManager, Core Data, SwiftData', r'\b(userdefaults|core ?data|swiftdata|filemanager|file manager|persist\w*|save data|saving|keychain|documents directory|nscache|cache)\b'),
 ('fw-networking','Frameworks','Networking: URLSession, APIs, downloading', r'\b(urlsession|network\w*|apis?\b|download\w*|http|rest|fetch\w*|urlrequest|webview|websocket)\b'),
 ('fw-cloud','Frameworks','CloudKit, Firebase & backend services', r'\b(cloudkit|firebase|firestore|supabase|backend|server|vapor|authentication|sign in with)\b'),
 ('fw-uikit','Frameworks','UIKit & AppKit', r'\b(uikit|uiview|uiviewcontroller|table ?view|collection ?view|storyboards?|auto ?layout|interface builder|programmatic|appkit|uihostingcontroller|representable|delegate)\b'),
 ('fw-platform','Frameworks','Platform frameworks: MapKit, notifications, widgets, charts, HealthKit, StoreKit, ML…', r'\b(mapkit|maps?|locations?|core location|notifications?|widgets?|widgetkit|live activit|charts?|healthkit|storekit|in-app purchases?|subscriptions?|core ml|create ml|machine learning|vision\b|arkit|realitykit|avfoundation|camera|audio|sound|video|spritekit|scenekit|gameplaykit|app intents|siri|shortcuts|tipkit|core haptics|biometric|face id|touch id|local ?authentication|contacts|eventkit|photos|share ?sheet|sharelink|document|pdfkit|visionos|watchos|tvos|macos|spatial)\b'),
 ('eng-accessibility','Engineering practice','Accessibility & localization', r'\b(accessib\w*|voiceover|dynamic type|locali[sz]\w*|internationali[sz]\w*)\b'),
 ('eng-testing','Engineering practice','Testing: XCTest, Swift Testing, UI tests, debugging', r'\b(test\w*|xctest|swift testing|tdd|debug\w*|breakpoints?|lldb|instruments|profil\w*|performance|crash\w*|bugs?)\b'),
 ('eng-architecture','Engineering practice','Architecture: MVVM, MVC, dependency injection, modularization', r'\b(mvvm|mvc|viper|tca|architecture|dependency injection|coordinators?|modular\w*|clean code|solid|design patterns?|singletons?|refactor\w*|code review)\b'),
 ('eng-tooling','Engineering practice','Tooling: Xcode, SPM, Git, CI, AI assistants', r'\b(xcode|swift package|spm|packages?|git|github|source control|ci\b|xcode cloud|fastlane|playgrounds?|terminal|ai\b|agents?|chatgpt|copilot|llm|linters?|swiftlint|swiftformat|previews?)\b'),
 ('lang-advanced','Swift language','Advanced features: property wrappers, result builders, key paths, macros, operators, subscripts', r'\b(property wrappers?|result builders?|keypaths?|key paths?|macros?|custom operators?|subscripts?|dynamic member|callasfunction|variadic generics|parameter packs|@main|attributes?)\b'),
 ('lang-codable','Swift language','Codable & JSON', r'\b(codable|decodable|encodable|json|decod|encod)\b'),
 ('lang-memory','Swift language','Memory management, ARC & ownership', r'\b(memory|arc\b|retain cycles?|weak|unowned|strong reference|leaks?|noncopyable|~copyable|ownership|consume)\b'),
 ('lang-generics','Swift language','Generics, opaque & existential types', r'\b(generics?|some\b|any\b|opaque|existential|associated types?|type erasure|primary associated|phantom)\b'),
 ('lang-protocols','Swift language','Protocols, extensions & POP', r'\b(protocols?|extensions?|protocol[- ]oriented|equatable|hashable|comparable|identifiable|customstringconvertible)\b'),
 ('lang-enums','Swift language','Enums & pattern matching', r'\b(enums?|enumerations?|associated values?|pattern matching|caseiterable|raw values?)\b'),
 ('lang-errors','Swift language','Error handling', r'\b(errors?|throws?|do, try|try\b|catch|result type|typed throws)\b'),
 ('lang-optionals','Swift language','Optionals & unwrapping', r'\b(optionals?|unwrap|nil|if[- ]let|guard let|optional chaining|nil coalescing)\b'),
 ('lang-closures','Swift language','Closures & higher-order functions', r'\b(closures?|escaping|autoclosure|map|filter|reduce|compactmap|flatmap|sort(ing|ed)?|higher[- ]order|functional programming|trailing closure)\b'),
 ('lang-functions','Swift language','Functions & parameters', r'\b(functions?|parameters?|variadic|inout|default values?|return values?|argument labels?)\b'),
 ('lang-control','Swift language','Conditions, loops & switch', r'\b(if[- ]statements?|if-else|conditions?|conditional|loops?|for[- ]in|while|switch|ternary|guard\b)'),
 ('lang-collections','Swift language','Arrays, sets, dictionaries & tuples', r'\b(arrays?|sets?\b|dictionar|tuples?|collections?|ranges?|sequence)\b'),
 ('lang-strings','Swift language','Strings, characters & regex', r'\b(strings?|characters?|substring|regex|regular expression|attributedstring|unicode)\b'),
 ('lang-structs-classes','Swift language','Structs, classes, inheritance & initialisers', r'\b(structs?|class(es)?\b|inheritance|initiali[sz]ers?|inits?\b|deinit|value types?|reference types?|object oriented|oop|copy on write)\b'),
 ('lang-properties','Swift language','Properties, observers & access control', r'\b(propert(y|ies)|computed|lazy|didset|willset|observers?|access control|private|public|static)\b'),
 ('lang-stdlib','Swift language','Standard library internals & algorithms', r'\b(standard library|stdlib|algorithms?|data structures?|big o|complexity|linked list|binary search|recursion)\b'),
 ('ui-state','SwiftUI','State & data flow: @State, @Binding, @Observable, environment', r'(@state|@binding|@observable|observableobject|stateobject|observedobject|environmentobject|@environment|environment|@appstorage|@scenestorage|@bindable|data flow|bindings?|observation)'),
 ('ui-navigation','SwiftUI','Navigation, sheets, alerts & presentation', r'\b(navigation|navigationstack|navigationlink|navigationsplitview|sheets?|alerts?|popovers?|fullscreencover|confirmation dialog|actionsheet|tabview|tab bar|toolbar|menus?|deep links?)\b'),
 ('ui-lists','SwiftUI','Lists, ForEach, scroll views & search', r'\b(lists?|foreach|scrollview|scroll|searchable|refreshable|swipe actions?|sections?|lazy)\b'),
 ('ui-controls','SwiftUI','Controls & input: buttons, text fields, pickers, forms', r'\b(buttons?|textfield|texteditor|toggle|picker|stepper|slider|datepicker|colorpicker|forms?|focusstate|keyboard|photospicker|controls?)\b'),
 ('ui-animation','SwiftUI','Animations, transitions & gestures', r'\b(animat\w*|transitions?|matchedgeometry|gestures?|drag|magnification|rotation|phaseanimator|keyframe|springs?|haptics?)\b'),
 ('ui-drawing','SwiftUI','Drawing: shapes, paths, Canvas, gradients, effects', r'\b(shapes?|paths?|canvas|gradients?|drawing|metal shaders?|shaders?|masks?|blur|materials?|visual ?effects?|sf symbols|colors?|images?|text effects?|fonts?)\b'),
 ('ui-layout','SwiftUI','Layout: stacks, frames, grids, GeometryReader, Layout protocol', r'\b(vstack|hstack|zstack|stacks?|frames?|alignment|padding|spacer|grid|lazyvgrid|lazyhgrid|geometryreader|layout|safe ?area|viewthatfits|anylayout|containerrelativeframe)\b'),
 ('ui-modifiers','SwiftUI','View composition: modifiers, ViewBuilder, preferences, custom styles', r'\b(view ?modifiers?|modifiers?|viewbuilder|preferencekey|button ?styles?|custom styles?|subviews|extract|reusable|components?)\b'),
 ('lang-basics','Swift language','Variables, constants, types & operators', r'\b(variables?|constants?|basic types|type annotation|let vs var|integers?|doubles?|booleans?|type inference|how to code in swift|complete beginners|swift basics|string interpolation|comments?)\b'),
 ('ui-general','SwiftUI','SwiftUI apps & projects (general)', r'\b(swiftui)\b'),
 ('career','Career & community','Career, interviews, portfolios, indie business, news & events', r'.'),
]
COMPILED = [(tid, area, label, re.compile(rx, re.I)) for tid, area, label, rx in T]
NONTECH = re.compile(r"(?i)\b(news|career|jobs?|salary|interview|portfolio|reviews?|q&a|live\b|podcast|freelanc\w*|money|indie|marketing|app store (optimi|rating|review)|keynote|announce\w*|events?|reaction|vlog|desk setup|macbook|iphone \d+|chronicles?|creator|profit|monetiz\w*|burnout|motivation|roadmap|advice|conference|wwdc|trip|q and a|ask me|stream|giveaway|sponsor|merch|book|course launch|thank you|milestone|subscribers? special|resume|linkedin|startup|founder|mvp)\b")

def classify(title):
    # Interview-question videos are technical content: keep them in technical topics when they match one.
    for tid, area, label, rx in COMPILED[:-1]:
        if rx.search(title):
            if NONTECH.search(title) and not re.search(r'(?i)swift|swiftui|xcode|code|coding', title):
                return 'career'
            return tid
    return 'career'
