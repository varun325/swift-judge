`TabView(selection:)` binds to a `Hashable` value — an enum is ideal. `.badge(count)` hides itself at 0. Keeping badge counts in a dictionary keyed by the tab enum keeps the view declarative.
