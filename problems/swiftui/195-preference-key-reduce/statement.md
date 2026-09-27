Swiftful's *PreferenceKey*: children report values up the tree and SwiftUI combines them with the key's `static func reduce(value: inout Value, nextValue: () -> Value)`.

 Implement `MaxHeightKey` (default 0, keeps the max) and `TitlesKey` (default `[]`, concatenates). Simulate SwiftUI's fold: start from `defaultValue` and call `reduce` once per child value. Return `["max <h>", "titles <joined by ,>"]`.
