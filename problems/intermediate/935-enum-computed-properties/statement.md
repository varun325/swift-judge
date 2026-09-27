`enum Planet: String, CaseIterable` with cases `mercury…neptune`. Add computed `index` (1-based order), `isInner` (first four), a `static var giants: [Planet]` (jupiter, saturn, uranus, neptune) and a `static func named(_:) -> Planet?` that's case-insensitive.

 For each name return `"<name> #<index> inner:<Bool> giant:<Bool>"` or `"unknown"`.
