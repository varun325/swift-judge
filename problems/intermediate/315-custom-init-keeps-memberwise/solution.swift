struct Player {
    let name: String
    let number: Int
}

extension Player {
    init(name: String) {
        self.name = name
        self.number = name.unicodeScalars.reduce(0) { $0 + Int($1.value) } % 100
    }
}

func players(_ names: [String]) -> [String] {
    names.enumerated().map { i, name in
        let p = i == 0 ? Player(name: name, number: 10) : Player(name: name)
        return "\(p.name)#\(p.number)"
    }
}
