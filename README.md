# Swift Judge

A local, LeetCode-style Electron app for learning Swift from beginner to advanced. Every submission
is compiled with your real `swiftc` and judged against test cases; expected outputs come from each
problem's reference solution, so adding a problem never requires hand-computing answers.

- **466 problems · 3,192 test cases** across six tracks: beginner, intermediate, advanced, SwiftUI,
  Apple frameworks, and Stanford CS193p (2025). SwiftUI / framework problems run on macOS.
- **Four judge modes**: implement a function · stdin→stdout programs · make-the-compiler-say-X
  diagnostics · predict-the-output (checked by actually running the code)
- **Three hints per problem**, unlocked one at a time: a nudge toward the right Swift feature, then
  the approach, then nearly the key line of code. Hints used are saved with your progress.
- **80/20 tags**: every problem is *Core 20%* (the topics that carry most of a senior iOS engineer's
  day-to-day impact) or *Edge 80%* (the long tail); filter the list to Core only.
- **Coming from JavaScript**: a collapsed note per problem comparing the idea with JS/TS (open it
  when you want the hint).
- **Confusion Compass**: questions per problem that poke at practical app use, JS (and Java)
  comparisons, contrasts with neighbouring concepts, and edge cases. **Answer in Playground** opens
  a notes page pre-filled with them; your answers are never overwritten.
- **Learn tab** per problem: your `swift-notes.md` section, *The Swift Programming Language*
  (offline), Apple developer documentation, Swift book / Evolution articles, and videos from
  Swiftful Thinking, Paul Hudson, Sean Allen and Stanford CS193p that **jump to the moment the idea
  is taught** (timestamps found from the transcripts, with the quote shown). Every link is verified.
- **Revisit today**: Fibonacci spaced repetition. A solved problem comes back after 1, 1, 2, 3, 5, 8,
  13… days; an on-time re-solve climbs the ladder, a failed one drops a rung. The app greets you with
  what's due.
- **Playground** for free-form Swift with an output panel and Markdown notes saved as plain files
- **Concepts** view (166 interview questions from five sources, each linked to problems),
  **Quiz** (149 MCQs by topic, including CS193p lectures and things a compiler can't judge: UIKit,
  Xcode, Instruments, SPM, shipping, security, testing, accessibility) and an offline **Swift Book** reader
- [`content/TOPICS.md`](content/TOPICS.md): every topic the three YouTube creators cover, with video
  counts and the problems and quiz topics that teach it.

## Download

Prebuilt apps are on the [Releases page](https://github.com/varun325/swift-judge/releases): a macOS
Apple Silicon `.dmg`, and Windows x64 installer and portable `.exe`s. You still need Swift installed
(see Requirements); the app uses your `swiftc` to judge.

## Requirements

- **macOS**: Xcode or the Command Line Tools (`xcrun --find swiftc`) — built against Swift 6.4
- **Windows 10/11 x64**: [Swift for Windows](https://www.swift.org/install/windows/) — its installer
  also needs the Visual Studio Build Tools with the "Desktop development with C++" workload.
  `swiftc` must be on `PATH` (the installer does this); or set `SWIFTC` to its full path.
- Node 20+ to build from source (tested with 24)

## Install

| Platform | Build | Result |
|---|---|---|
| macOS (Apple Silicon) | `npm run install-app` | builds, ad-hoc signs and copies **Swift Judge.app** to `/Applications` |
| macOS disk image | `npm run package:dmg` | `dist/Swift Judge-0.1.0-arm64.dmg` |
| Windows x64 | `npm run package:win` (on the Mac; needs Rosetta 2 for NSIS) | `dist/Swift Judge Setup 0.1.0.exe` (installer) and `dist/Swift Judge 0.1.0 Portable.exe` |

The builds aren't signed with a paid certificate. macOS opens the locally built app normally;
on Windows, SmartScreen shows "Windows protected your PC" the first time — choose **More info → Run anyway**.

Where content comes from: the Mac app reads problems, notes and docs **live from this project
folder**, so problems you add here show up in the installed app. If the folder is missing (e.g. on
Windows) the app uses the copy bundled inside it. Progress lives in the app's userData folder
(`~/Library/Application Support/swift-judge/`, or `%APPDATA%\swift-judge\` on Windows).

## Develop

```bash
npm install          # if npm blocks install scripts: npm approve-scripts electron esbuild
npm run dev          # launch with hot reload
```

Keyboard: **⌘↵ / Ctrl+Enter** Run (visible tests) · **⌘⇧↵ / Ctrl+Shift+Enter** Submit (all tests, incl. hidden).

## Playground

A scratch Swift editor (⌘↵ / Ctrl+Enter compiles and runs it, with optional stdin), an output
panel, and Markdown notes with a live preview you can minimise. **Append run to notes** records the
code and its output. Each page is two plain files — `<name>.swift` and `<name>.md` — in
`varun_notes/playground/` (next to `swift-notes.md`), or in the app's userData folder when that
isn't available. Deleting a page moves both files to the Trash / Recycle Bin.

## Adding a problem (the plug-in contract)

```bash
npm run new-problem -- intermediate my-slug function   # or stdio | diagnostic | predict
# edit the files, then
npm run validate -- my-slug
```

The app watches `problems/` and picks up new folders without a restart. A problem is a folder
`problems/<track>/<NNN>-<slug>/` — the number only orders the list:

| File | Purpose |
|---|---|
| `problem.json` | metadata (below) |
| `statement.md` | the task, with examples |
| `starter.swift` | what the editor opens with |
| `solution.swift` | reference solution (unlocked after Accepted) |
| `tests.json` | `[{ "name"?, "input", "expected"?, "hidden"? }]` |
| `explanation.md` | the concept write-up shown after solving |
| `snippet.swift` | *predict mode*: the program whose output you predict |
| `harness.swift` | *optional*: custom driver for class/protocol "design" problems |

**Omit `expected` and the judge runs `solution.swift` on the same input** and compares your output
with it (cached by content hash). Give `expected` explicitly when you want to pin a value — the
validator checks it agrees with the reference.

### `problem.json`

```jsonc
{
  "id": "two-sum",                    // unique, used for progress
  "title": "Two Sum with a Dictionary",
  "track": "beginner",                // beginner | intermediate | advanced
  "difficulty": "easy",               // easy | medium | hard
  "topic": "Dictionaries",            // sidebar grouping
  "concepts": ["dictionary-basics"],  // ids from content/concepts.json
  "mode": "function",                 // function | stdio | diagnostic | predict
  "notesRef": "7",                    // "## 7." section of swift-notes.md
  "docs": [{ "title": "Collection Types", "book": "LanguageGuide/CollectionTypes" },
           { "title": "Apple docs", "url": "https://developer.apple.com/…" }],
  "signature": {                      // function mode (unless harness.swift is used)
    "name": "twoSum",
    "params": [{ "label": "_", "name": "nums", "type": "[Int]" },
               { "name": "target", "type": "Int" }],   // "inout": true supported
    "returns": "[Int]",               // any Encodable; "Void" + one inout param returns that param
    "throws": false, "async": false   // thrown errors are reported as {"$error": "<case>"}
  },
  "compare": "json",                  // json | json-unordered | json-unordered-deep | float:1e-9
                                      // stdio/predict: trimmed (default) | exact | unorderedLines | float:<eps>
  "timeLimitMs": 2000,
  "swiftVersion": "6",
  "starterFails": false,              // true for fix-the-compile-error problems
  "hints": [                          // exactly 3 (validate enforces it), each more revealing
    "Nudge: which Swift feature applies?",
    "Approach: how to structure the solution.",
    "Almost there: the key line or expression."
  ],
  "impact": "core",                   // core | edge (80/20)                     — required
  "jsBridge": "Markdown comparing it with JS/TS",                                // required
  "compass": [{ "kind": "js", "q": "…" }],   // ≥ 3; kinds: practice | js | java | contrast | edge,
                                      // at least one "js"                           — required
  "platforms": ["darwin"],            // omit unless it needs Apple frameworks
  "videos": [{ "title": "…", "url": "https://www.youtube.com/watch?v=…&t=95s", "channel": "…",
               "start": 95, "moment": "transcript quote at that time" }],
  "articles": [{ "title": "…", "url": "https://…", "source": "swift.org" }]
}
```

### Modes

- **function** — the learner's code is compiled as `user.swift` next to a generated `main.swift`
  driver that decodes each test's `input` (an object keyed by parameter name) with `Codable`, calls
  the function and JSON-encodes the result. All tests run in one process; a crash or timeout is
  isolated to its test and the rest continue.
- **custom harness** — for design problems, `harness.swift` defines
  `struct __Input: Decodable` and `func __run(_ __i: __Input) async throws -> some Encodable`
  (e.g. an ops/args list like LeetCode's design problems).
- **stdio** — the program is `main.swift`; each test's `input` string is piped to stdin and stdout is compared.
- **diagnostic** — code is compiled through SIL mandatory passes (so definite-initialisation,
  exclusivity and ownership errors are reported); each test has `pattern` (regex) and optional
  `severity` (`error` | `warning` | `none` = must compile cleanly).
- **predict** — the learner types the output of `snippet.swift`; the judge runs the snippet and diffs.

## Scripts

| Command | What it does |
|---|---|
| `npm test` | judge unit tests (compare modes, harness, crash isolation, timeouts, every mode end-to-end) |
| `npm run validate [-- filter]` | compiles every reference solution, runs all tests, checks starters, hints, concept ids, 80/20 tags, JS notes, Compass questions and references |
| `npm run check-links` | verifies every reference link (YouTube via oEmbed, everything else must return 200) |
| `npm run stress -- <filter> [rounds] [parallel]` | judges reference solutions many times in parallel to flush out load-dependent crashes |
| `npm run e2e [-- filter]` | builds the app and drives the real window: every problem's starter must be rejected and reference accepted, plus UI scenario checks |
| `npm run new-problem -- <track> <slug> [mode]` | scaffolds a problem folder |
| `npm run package` / `npm run install-app` | build the macOS app / build and install it into `/Applications` |
| `npm run package:win` | build the Windows x64 installer and portable `.exe` |
| `npm run package:dmg` | build the macOS `.dmg` |
| `npm run vendor-docs` | refreshes `docs/swift-book` and `docs/interview` from GitHub |
| `npm run typecheck` | TypeScript check |

## Layout

```
src/main/judge/     toolchain (swiftc + SDK), harness generator, runner (timeouts, output caps),
                    compare, diagnostics, judge orchestration + reference cache
src/main/content/   problem loader, notes splitter, book reader
src/renderer/       React UI (Monaco editor, results, Learn/Concepts/Quiz/Book views)
problems/           the problem bank          content/   concepts, quiz, notes copy, sources, TOPICS.md
docs/               vendored Swift book + interview questions
authoring/          how the bank was built: problem batches (problems/), learning content
                    (enrichment/: 80/20, JS notes, Compass → apply.py), references (references/:
                    registry + build.py with transcript timestamps), quiz (quiz/build.py), video
                    research data (research/), and topics.py → content/TOPICS.md
```

Judged programs catch fatal signals and exit with 128 + signal, so crashes you trigger on purpose
(force-unwrapping nil, out-of-range indices) don't file macOS crash reports; the judge still reports
them as runtime errors with Swift's message and your line numbers.
