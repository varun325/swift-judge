protocol Animal {
    func describe() -> String
}

extension Animal {
    func describe() -> String { "some animal" }
    func nickname() -> String { "critter" }
}

struct Cat: Animal {
    func describe() -> String { "a cat" }
    func nickname() -> String { "kitty" }
}

let cat = Cat()
let animal: any Animal = cat
print(cat.describe(), "|", cat.nickname())
print(animal.describe(), "|", animal.nickname())
