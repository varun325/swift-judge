`struct School` should have a **type-level** `static let capacity = 3` and a `static func enroll(_ roster: inout [String], _ name: String) -> String` that returns `"enrolled <name> (<n>/3)"` or `"full"` once capacity is reached.

 (Swift 6 forbids a global or `static var` of mutable shared state without isolation — so the roster is passed `inout` rather than stored in a `static var`.)
