Swiftful's *Accessibility: Dynamic Text*. `DynamicTypeSize` is `Comparable` and `CaseIterable`, with `isAccessibilitySize` for the largest five. A common pattern: switch from `HStack` to `VStack` layout when `size >= .accessibility1` (use `ViewThatFits` or `AnyLayout`).

 Map each size name (e.g. `large`, `xxxLarge`, `accessibility2`) to `"<name>: <HStack|VStack>"` (`unknown` for invalid names). Finally append `"accessibility sizes: <count>"`.
