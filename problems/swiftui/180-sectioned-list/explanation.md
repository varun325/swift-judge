`Dictionary(grouping:by:)` produces the sections; sorting keys with a tuple puts `#` last. In SwiftUI you'd `ForEach(keys, id: \.self) { Section(key) { ForEach(grouped[key]!) … } }`.
