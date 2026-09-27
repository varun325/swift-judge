`AsyncThrowingStream` bridges push-based producers into `for try await`. `finish(throwing:)` ends the stream with an error that surfaces at the loop; `finish()` ends it normally.
