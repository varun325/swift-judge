# Topic catalogue

Every topic covered by **Swiftful Thinking**, **Paul Hudson** (Hacking with Swift) and **Sean Allen** on YouTube (2254 videos classified), how many videos each made, and where Swift Judge teaches it. Problems link to the exact moment in those videos (Learn tab). Topics a compiler can't judge are covered in the Quiz.

Regenerate with `python3 authoring/topics.py`.


## Swift language

| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |
|---|---:|---:|---:|---|---|
| What's new in Swift (evolution) | 0 | 40 | 26 | 31 (3 core): `async-throwing-stream`, `builtin-macros`, `check-cancellation`, `custom-async-sequence`, `custom-subscript-matrix`, `diag-captured-var-mutation` +25 more | — |
| Concurrency: async/await, tasks, actors, Sendable | 22 | 8 | 10 | 56 (31 core): `actor-bank`, `actor-nonisolated`, `actor-request-coalescing`, `async-await-basics`, `async-let`, `async-sequence` +50 more | — |
| Advanced features: property wrappers, result builders, key paths, macros, operators, subscripts | 8 | 7 | 4 | 17 (6 core): `custom-operator-vector`, `custom-subscript-matrix`, `keypath-member-lookup`, `keypath-writable`, `property-wrapper-clamped`, `array-safe-subscript` +11 more | — |
| Codable & JSON | 1 | 23 | 0 | 14 (7 core): `associated-type-container`, `codable-custom-init`, `codable-round-trip`, `codable-snake-case`, `conditional-conformance-pair`, `diag-existential-equatable` +8 more | — |
| Memory management, ARC & ownership | 1 | 1 | 1 | 9 (5 core): `closure-retain-cycle`, `linked-list-cycle`, `predict-self-vs-Self`, `retain-cycle-parent-child`, `unowned-customer-card`, `weak-self-task` +3 more | — |
| Generics, opaque & existential types | 1 | 9 | 1 | 11 (5 core): `conditional-conformance-pair`, `generic-constraints-max`, `generic-swap-and-stack`, `opaque-some-return`, `phantom-types-ids`, `primary-associated-types` +5 more | — |
| Protocols, extensions & POP | 3 | 19 | 1 | 18 (11 core): `associated-type-container`, `equatable-hashable-custom`, `array-safe-subscript`, `hashable-point-set`, `range-clamp`, `abstract-class-emulation` +12 more | — |
| Enums & pattern matching | 2 | 12 | 1 | 18 (4 core): `indirect-enum-expression`, `indirect-linked-list`, `diag-exhaustive-switch`, `enum-associated-shapes`, `enum-case-iterable`, `enum-methods-state` +12 more | — |
| Error handling | 1 | 8 | 3 | 15 (8 core): `assert-precondition`, `diag-error-directive`, `checkpoint-4-integer-sqrt`, `check-password-throws`, `defer-order`, `do-catch-patterns` +9 more | — |
| Optionals & unwrapping | 2 | 21 | 3 | 24 (13 core): `missing-number`, `caesar-cipher`, `character-count`, `dictionary-default-lookup`, `if-expression`, `nil-coalescing-chains` +18 more | — |
| Closures & higher-order functions | 1 | 24 | 5 | 21 (8 core): `merge-intervals`, `reverse-string-ways`, `sort-names-stdio`, `top-k-frequent`, `acronym`, `merge-sorted` +15 more | — |
| Functions & parameters | 2 | 22 | 1 | 11 (5 core): `argument-labels`, `default-parameters`, `nested-functions`, `overloading-describe`, `swap-values`, `variadic-average` +5 more | — |
| Conditions, loops & switch | 6 | 32 | 3 | 19 (2 core): `diag-exhaustive-switch`, `fallthrough-description`, `fix-can-vote`, `fix-infinite-while`, `fizzbuzz-stdio`, `grade-letter` +13 more | — |
| Arrays, sets, dictionaries & tuples | 2 | 14 | 3 | 24 (4 core): `custom-collection-ring`, `custom-sequence-fibonacci`, `dedupe-sorted-inplace`, `lcs`, `majority-element`, `product-except-self` +18 more | — |
| Strings, characters & regex | 1 | 18 | 1 | 20 (5 core): `bool-toggle-xor`, `caesar-cipher`, `character-count`, `character-properties`, `diag-type-annotation`, `interpolation-receipt` +14 more | — |
| Structs, classes, inheritance & initialisers | 3 | 32 | 7 | 24 (14 core): `predict-struct-class-actor`, `predict-array-copy`, `predict-struct-vs-class`, `checkpoint-6-car`, `checkpoint-7-animals`, `class-copying-predict` +18 more | — |
| Properties, observers & access control | 2 | 19 | 5 | 10 (4 core): `copy-on-write`, `custom-sequence-fibonacci`, `access-control-module`, `diag-private-access`, `predict-lazy-order`, `predict-observers-init` +4 more | — |
| Standard library internals & algorithms | 0 | 2 | 4 | 13 (0 core): `binary-tree-level-order`, `coin-change`, `design-trie`, `dijkstra`, `generic-binary-search`, `longest-unique-substring` +7 more | — |
| Variables, constants, types & operators | 5 | 25 | 1 | 10 (6 core): `bool-toggle-xor`, `diag-let-reassign`, `diag-type-annotation`, `fahrenheit`, `first-unique-char`, `float-compare` +4 more | — |

## SwiftUI

| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |
|---|---:|---:|---:|---|---|
| State & data flow: @State, @Binding, @Observable, environment | 6 | 40 | 1 | 15 (11 core): `sha256-hash`, `ab-test-bucketing`, `combine-async-bridge`, `combine-published-sink`, `infinite-scroll`, `offline-sync-queue` +9 more | — |
| Navigation, sheets, alerts & presentation | 17 | 51 | 4 | 9 (5 core): `type-inference-describe`, `typealias-grid`, `design-min-stack`, `deep-link-router`, `navigation-path`, `predict-modifier-order` +3 more | — |
| Lists, ForEach, scroll views & search | 13 | 44 | 6 | 8 (2 core): `skipping-items`, `custom-string-convertible`, `list-offsets`, `paging-target`, `scroll-parallax`, `scroll-reader-target` +2 more | — |
| Controls & input: buttons, text fields, pickers, forms | 12 | 44 | 7 | 8 (1 core): `digit-sum`, `numeric-literals`, `wrapping-hash`, `iso8601-timezones`, `notificationcenter-async`, `animatable-shape` +2 more | — |
| Animations, transitions & gestures | 9 | 37 | 6 | 9 (0 core): `animatable-pair`, `animatable-shape`, `long-press-progress`, `magnification-clamp`, `phase-animator-sequence`, `shape-star` +3 more | — |
| Drawing: shapes, paths, Canvas, gradients, effects | 10 | 48 | 5 | 3 (0 core): `color-hex-resolve`, `shape-triangle`, `view-that-fits` | — |
| Layout: stacks, frames, grids, GeometryReader, Layout protocol | 10 | 34 | 1 | 5 (0 core): `valid-parentheses`, `validate-bst`, `queue-two-stacks`, `adaptive-grid-columns`, `view-that-fits` | — |
| View composition: modifiers, ViewBuilder, preferences, custom styles | 8 | 19 | 1 | 7 (5 core): `result-builder-html`, `date-components-math`, `diag-opaque-mismatch`, `predict-modifier-order`, `predict-text-concatenation`, `predict-viewbuilder-types` +1 more | — |
| SwiftUI apps & projects (general) | 45 | 162 | 21 | 20 (9 core): `enum-methods-state`, `predict-empty-collections`, `ab-test-bucketing`, `date-interval-overlap`, `days-between`, `infinite-scroll` +14 more | — |

## Frameworks

| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |
|---|---:|---:|---:|---|---|
| Combine: publishers & subscribers | 7 | 5 | 3 | 9 (5 core): `combine-cancellation`, `combine-combinelatest-zip`, `combine-error-handling`, `combine-future`, `combine-pipeline`, `combine-subjects` +3 more | — |
| Persistence: UserDefaults, FileManager, Core Data, SwiftData | 10 | 58 | 3 | 24 (11 core): `file-manager-listing`, `lru-cache`, `memoization`, `sha256-hash`, `uuid-and-identifiable`, `checkpoint-5-lucky-numbers` +18 more | — |
| Networking: URLSession, APIs, downloading | 11 | 16 | 5 | 24 (16 core): `codable-round-trip`, `codable-snake-case`, `coin-change`, `codable-dates-strategies`, `codable-encode-snake-sorted`, `codable-nested-unkeyed` +18 more | — |
| CloudKit, Firebase & backend services | 26 | 2 | 3 | 7 (4 core): `custom-collection-ring`, `apns-payload`, `auth-state-machine`, `firestore-cursor-paging`, `health-step-aggregation`, `storekit-entitlements` +1 more | Cloud & backend (6) |
| UIKit & AppKit | 3 | 27 | 18 | 5 (3 core): `pattern-match-operator`, `builder-pattern-copy`, `protocol-composition-delegate`, `flow-layout-rows`, `navigation-path` | UIKit (12) |
| Platform frameworks: MapKit, notifications, widgets, charts, HealthKit, StoreKit, ML… | 16 | 66 | 43 | 23 (10 core): `max-subarray`, `sort-names-stdio`, `checkpoint-5-lucky-numbers`, `apns-payload`, `chart-binning`, `corelocation-distances` +17 more | App lifecycle (6) |

## Engineering practice

| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |
|---|---:|---:|---:|---|---|
| Accessibility & localization | 3 | 23 | 2 | 6 (2 core): `group-anagrams`, `accessibility-labels`, `color-hex-resolve`, `contrast-ratio`, `dynamic-type-sizes`, `inflection-pluralization` | Accessibility & localisation (5) |
| Testing: XCTest, Swift Testing, UI tests, debugging | 6 | 47 | 10 | 5 (2 core): `fix-can-vote`, `predict-interpolation`, `pyramid-stdio`, `image-downsampling`, `test-doubles-spy` | Testing (6) |
| Architecture: MVVM, MVC, dependency injection, modularization | 6 | 9 | 5 | 9 (5 core): `dependency-injection`, `mvvm-async-viewmodel`, `pattern-match-operator`, `coordinator-router`, `dependency-container`, `feature-flags` +3 more | — |
| Tooling: Xcode, SPM, Git, CI, AI assistants | 26 | 47 | 65 | 27 (7 core): `csv-column-sums-stdio`, `custom-collection-ring`, `diag-main-attribute`, `matrix-transpose-stdio`, `regex-builder-log`, `regex-extract` +21 more | Xcode & tooling (10) |

## Career & community

| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |
|---|---:|---:|---:|---|---|
| Career, interviews, portfolios, indie business, news & events | 25 | 274 | 244 | 58 (15 core): `array-intersection-counts`, `binary-tree-level-order`, `course-schedule`, `custom-operator-vector`, `custom-subscript-matrix`, `dedupe-sorted-inplace` +52 more | Senior engineering (5) |
