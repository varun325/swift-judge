class Animal {
    let legs: Int
    init(legs: Int) { self.legs = legs }
    func speak() -> String { "..." }
}

class Dog: Animal {
    init() { super.init(legs: 4) }
    override func speak() -> String { "Woof" }
}
final class Corgi: Dog { override func speak() -> String { "Yip" } }
final class Poodle: Dog { override func speak() -> String { "Bark bark" } }

class Cat: Animal {
    let isTame: Bool
    init(isTame: Bool) {
        self.isTame = isTame
        super.init(legs: 4)
    }
    override func speak() -> String { isTame ? "Meow" : "Hiss" }
}
final class Persian: Cat { init() { super.init(isTame: true) } }
final class Lion: Cat {
    init() { super.init(isTame: false) }
    override func speak() -> String { "Roar" }
}

func zoo(_ specs: [String]) -> [String] {
    let animals: [Animal] = specs.compactMap {
        switch $0 {
        case "corgi": Corgi()
        case "poodle": Poodle()
        case "dog": Dog()
        case "persian": Persian()
        case "lion": Lion()
        case "wildcat": Cat(isTame: false)
        default: nil
        }
    }
    return animals.map { "\($0.speak()) (\($0.legs) legs)" }
}
