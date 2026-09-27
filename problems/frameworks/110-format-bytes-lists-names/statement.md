Return three strings (locale `en_US`):
 1. `files.formatted(.list(type: .and))` — e.g. `"a.txt, b.txt, and c.txt"`
 2. total size with `.byteCount(style: .file)`
 3. the uploader's name from `PersonNameComponents(givenName:familyName:)` formatted `.name(style: .abbreviated)` (initials) — `fullName` is `[given, family]`
