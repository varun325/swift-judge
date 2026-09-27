Use `import RegexBuilder` to parse lines like `"[ERROR] 2024-05-01 disk full (code 28)"`: level (`INFO|WARN|ERROR`), date, message, and a numeric code captured with `TryCapture` transforming to `Int`.

 Return `"<level>|<code>|<message>"` for lines that match the **whole** line, and `"skip"` otherwise.
