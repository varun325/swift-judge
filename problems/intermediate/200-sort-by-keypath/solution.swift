extension Sequence {
    func sorted<V: Comparable>(by keyPath: KeyPath<Element, V>) -> [Element] {
        sorted { $0[keyPath: keyPath] < $1[keyPath: keyPath] }
    }
}

struct Person {
    let name: String
    let age: Int
    let city: String
}

func sortPeople(_ rows: [[String]], by key: String) -> [String] {
    let people = rows.map { Person(name: $0[0], age: Int($0[1])!, city: $0[2]) }
    let sorted: [Person] = switch key {
    case "age": people.sorted(by: \.age)
    case "city": people.sorted(by: \.city)
    default: people.sorted(by: \.name)
    }
    return sorted.map(\.name)
}
