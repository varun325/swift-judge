Swiftful's *Custom Errors and Alerts*: `enum UploadError: LocalizedError` with cases `emptyFile`, `tooLarge(limitMB: Int)`, `offline`, providing `errorDescription` (user-facing) and `recoverySuggestion`.

 `func upload(sizeMB: Int) throws -> String` throws `.emptyFile` for 0, `.tooLarge(limitMB: 25)` above 25, `.offline` for negative sizes, else returns `"uploaded <n>MB"`. For each size return the result or `"<errorDescription> — <recoverySuggestion>"` using `error.localizedDescription` where possible.
