protocol Greeter {
    var name: String { get }
    func greet() -> String
}

extension Greeter {
    func greet() -> String { "Hello, I'm \(name)" }
    func greetTwice() -> String { greet() + " " + greet() }
}

struct English: Greeter { let name: String }

struct Pirate: Greeter {
    let name: String
    func greet() -> String { "Ahoy! \(name) here" }
}

func greetings(_ kinds: [String]) -> [String] {
    kinds.map { kind -> String in
        let g: any Greeter = kind == "pirate" ? Pirate(name: "Jack") : English(name: "Ann")
        return g.greetTwice()
    }
}
