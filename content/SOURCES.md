# Question-bank sources

Interview questions were collected from these pages, deduplicated into `concepts.json`, and
answered with **original** short explanations (nothing is copied verbatim). SwiftUI, UIKit and
platform-framework topics are excluded.

| Source | Used for | Excluded |
|---|---|---|
| [Devinterview-io/swift-interview-questions](https://github.com/Devinterview-io/swift-interview-questions) (vendored in `docs/interview/`) | 70 conceptual Q&As (15 public) | — |
| [fullstack.cafe — Swift](https://www.fullstack.cafe/interview-questions/swift) | 38 questions | GCD serial queue / QoS internals, `@objc` |
| [turing.com — Swift](https://www.turing.com/interview-questions/swift) | ~98 basic/intermediate/advanced questions | view transitions, dynamic frameworks, NotificationCenter, KVO |
| [hackingwithswift.com — interview questions](https://www.hackingwithswift.com/interview-questions) | Swift, Data, language-level Design Patterns; Foundation-only items (cache, singleton, UUID, hashing, FileManager) | Accessibility, iOS, SwiftUI, UIKit, misc, MVC/MVVM, other frameworks |
| [naukri.com Code360 — Swift](https://www.naukri.com/code360/library/swift-interview-questions) (pasted by the user; the site blocks automated fetches) | 100 questions + 10 MCQs (MCQs → `quiz.json`) | plist, responder chain, KVO, method swizzling, NSArray, `@frozen`/library evolution |
| [The Swift Programming Language](https://github.com/swiftlang/swift-book) (vendored in `docs/swift-book/`, Apache-2.0) | Learn-tab chapters, problem doc links | — |
| `swift-notes.md` (your notes) | Learn-tab sections via `notesRef`, fix-the-bug problems | — |
