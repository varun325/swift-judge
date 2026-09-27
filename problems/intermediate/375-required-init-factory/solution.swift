class Enemy {
    let level: Int
    required init(level: Int) { self.level = level }
    class func make(level: Int) -> Self { Self(level: level) }
    func describe() -> String { "enemy L\(level)" }
}

final class Goblin: Enemy {
    override func describe() -> String { "goblin L\(level)" }
}

final class Dragon: Enemy {
    required init(level: Int) { super.init(level: level * 2) }
    override func describe() -> String { "dragon L\(level)" }
}

func spawnAll(_ kinds: [String]) -> [String] {
    kinds.map { spec in
        let parts = spec.split(separator: " ")
        let type: Enemy.Type = switch parts[0] {
        case "goblin": Goblin.self
        case "dragon": Dragon.self
        default: Enemy.self
        }
        return type.make(level: Int(parts[1])!).describe()
    }
}
