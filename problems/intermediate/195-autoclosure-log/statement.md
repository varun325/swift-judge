Write `func debugLog(_ message: @autoclosure () -> String, level: Int, into log: Log)` that only **evaluates** `message` when `level >= 2`.

 In `loggingDemo`, call `debugLog(expensive("A"), level: level, into: log)` and `debugLog(expensive("B"), level: 3, into: log)`, where `expensive(_:)` appends `"computed <x>"` to the log before returning `"msg <x>"`, and logged messages are appended as `"LOG msg <x>"`. Return the log.
