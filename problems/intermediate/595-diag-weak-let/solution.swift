final class Owner {}

final class Pet {
    weak let owner: Owner
    init(owner: Owner) { self.owner = owner }
}
