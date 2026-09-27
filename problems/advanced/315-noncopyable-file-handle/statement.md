Model a file handle that must have exactly **one owner**: `struct FileHandle: ~Copyable` with a `name`, a `Log`, a private `closed` flag and:
 - `mutating func write(_:)` — logs `"write <text>"`
 - **`consuming func close()`** — logs `"close <name>"` and marks itself closed; since it *consumes* `self`, the caller can't use the handle afterwards
 - `deinit` — logs `"auto-close <name>"` **only if** it wasn't closed explicitly

 Also write `func inspect(_ h: borrowing FileHandle) -> String` returning `"inspect <name>"`.

 In the demo: create the handle, `inspect` it (append to log), write each string, then call `close()` if `closeEarly`, else let it go out of scope. Log `"done"` last.
