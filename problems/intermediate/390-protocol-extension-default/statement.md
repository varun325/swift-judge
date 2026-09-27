`protocol Greeter { var name: String { get }; func greet() -> String }` with a **protocol extension** providing a default `greet()` returning `"Hello, I'm <name>"` and an extra method `func greetTwice() -> String` (the greeting twice, joined by `" "`).

 `English(name: "Ann")` uses the default; `Pirate(name: "Jack")` implements `greet()` as `"Ahoy! <name> here"`. Kinds are `"en"`/`"pirate"` — return `greetTwice()` for each.
