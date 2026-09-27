Paul's *Using alert() and sheet() with optionals*: instead of several `Bool`s, drive presentation with one optional `Identifiable` enum: `enum ActiveSheet: Identifiable { case settings, profile(Int), share(String) }` whose `id` is a string.

 Actions: `open settings`, `open profile 7`, `open share url`, `dismiss`. SwiftUI can show one sheet at a time: opening while one is presented **replaces** it (logs `"replace <old> with <new>"`), otherwise logs `"present <id>"`; dismiss logs `"dismiss <id>"` or `"nothing to dismiss"`.
