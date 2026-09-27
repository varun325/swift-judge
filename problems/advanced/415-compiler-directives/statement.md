Return facts about **this** build using compile-time conditions, one per line:
 1. `"swift>=6"` or `"swift<6"` via `#if swift(>=6.0)`
 2. `"macOS"`, `"Linux"` or `"other"` via `#if os(...)`
 3. `"arm64"` or `"x86_64"` via `#if arch(...)`
 4. `"has Foundation"` via `#if canImport(Foundation)`
 5. `"debug"` or `"release"` — the judge compiles with `-Onone` and **without** `-D DEBUG`, so check `#if DEBUG`
 6. `"macOS 13+"` if `#available(macOS 13, *)`, else `"older"`
