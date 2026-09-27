struct Profile {
    var name = "anon"
    var age = 0
    var city = "?"
}

func update<T, V>(_ value: inout T, _ keyPath: WritableKeyPath<T, V>, to newValue: V) {
    value[keyPath: keyPath] = newValue
}

func applyUpdates(_ updates: [String]) -> [String] {
    var profile = Profile()
    for u in updates {
        let parts = u.split(separator: "=", maxSplits: 1).map(String.init)
        guard parts.count == 2 else { continue }
        switch parts[0] {
        case "name": update(&profile, \.name, to: parts[1])
        case "age": if let a = Int(parts[1]) { update(&profile, \.age, to: a) }
        case "city": update(&profile, \.city, to: parts[1])
        default: break
        }
    }
    let fields: [PartialKeyPath<Profile>] = [\.name, \.age, \.city]
    return fields.map { "\(profile[keyPath: $0])" }
}
