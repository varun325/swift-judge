Build a `final class EventBus` with `func subscribe(_ handler: @escaping (String) -> Void)` that **stores** handlers, and `func publish(_ event: String)` that calls every stored handler.

 `eventBus` subscribes two handlers that append `"A:<event>"` and `"B:<event>"` to a log (a class instance), publishes each event, and returns the log. Try removing `@escaping` and read the error.
