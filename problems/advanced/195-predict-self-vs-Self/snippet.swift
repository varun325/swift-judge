class Animal {
    required init() {}
    class var kind: String { "animal" }
    func clone() -> Self { Self() }
    func describe() -> String { "\(type(of: self)) is a \(Self.kind)" }
}
final class Dog: Animal {
    override class var kind: String { "dog" }
}

let pet: Animal = Dog()
print(pet.describe())
print(type(of: pet.clone()))
print(pet is Dog, type(of: pet) == Animal.self)
print(Animal().describe())
