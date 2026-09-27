Swiftful's *Filtering data based on search bar text using Combine*. A view model has `@Published var query = ""` and `@Published private(set) var results: [String] = []`. In `init`, subscribe to `$query`: trim, lowercase, `removeDuplicates()`, `dropFirst()` (skip the initial value), and map to the matching items from a fixed list (`["apple", "apricot", "banana", "blueberry", "cherry"]`, prefix match; empty query → all). Assign into `results` with `assign(to: &$results)`.

 Set each typed string and log `results` joined by `,` after each.
