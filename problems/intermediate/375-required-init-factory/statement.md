`class Enemy` has `required init(level: Int)` and `class func make(level: Int) -> Self { Self(level: level) }`, plus `func describe() -> String` (`"enemy L<level>"`). Subclasses `Goblin` and `Dragon` override `describe()` (`"goblin L…"`, `"dragon L…"`) and must provide the `required` init.

 Inputs are `"goblin 3"`, `"dragon 10"` or `"enemy 1"`: call `make(level:)` on the right metatype and return `describe()`.
