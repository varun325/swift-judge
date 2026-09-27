func greet(_ name: String, greeting: String = "Hello", punctuation: String = "!") -> String {
    "\(greeting), \(name)\(punctuation)"
}

func greetAll(_ names: [String]) -> [String] {
    names.enumerated().map { i, name in
        switch i {
        case 0: greet(name)
        case 1: greet(name, greeting: "Hi")
        default: greet(name, punctuation: ".")
        }
    }
}
