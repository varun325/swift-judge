# Swift Judge

A local, LeetCode-style Electron app for learning Swift from beginner to advanced. Every submission
is compiled with your real `swiftc` and judged against test cases; expected outputs come from each
problem's reference solution, so adding a problem never requires hand-computing answers.

- **225 problems · 2,545 test cases** across beginner / intermediate / advanced tracks
- **Four judge modes**: implement a function · stdin→stdout programs · make-the-compiler-say-X
  diagnostics · predict-the-output (checked by actually running the code)
- **Three hints per problem**, unlocked one at a time: a nudge toward the right Swift feature, then
  the approach, then nearly the key line of code. Hints used are saved with your progress.
- **Learn tab** per problem: the matching section of your `swift-notes.md`, the relevant chapter of
  *The Swift Programming Language* (offline), and the interview questions it drills
- **Concepts** view (166 interview questions from five sources, each linked to problems),
  **Quiz** (40 quick-recall MCQs) and an offline **Swift Book** reader

## Requirements

- macOS with Xcode or the Swift toolchain (`xcrun --find swiftc`) — built against Swift 6.4
- Node 20+ (tested with 24)

## Run

```bash
npm install          # if npm blocks install scripts: npm approve-scripts electron esbuild
npm run dev          # launch the app with hot reload
npm run build && npm start   # production build
```

Keyboard: **⌘↵** Run (visible tests) · **⌘⇧↵** Submit (all tests, incl. hidden).
Progress and drafts are stored in the app's userData folder (`~/Library/Application Support/swift-judge/`).

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
  ]
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
| `npm run validate [-- filter]` | compiles every reference solution, runs all tests, checks starters, hints and concept ids |
| `npm run e2e [-- filter]` | builds the app and drives the real window: every problem's starter must be rejected and reference accepted, plus UI scenario checks |
| `npm run new-problem -- <track> <slug> [mode]` | scaffolds a problem folder |
| `npm run vendor-docs` | refreshes `docs/swift-book` and `docs/interview` from GitHub |
| `npm run typecheck` | TypeScript check |

## Layout

```
src/main/judge/     toolchain (swiftc + SDK), harness generator, runner (timeouts, output caps),
                    compare, diagnostics, judge orchestration + reference cache
src/main/content/   problem loader, notes splitter, book reader
src/renderer/       React UI (Monaco editor, results, Learn/Concepts/Quiz/Book views)
problems/           the problem bank          content/   concepts, quiz, notes copy, sources
docs/               vendored Swift book + interview questions
```
