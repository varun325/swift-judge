enum TrafficLight: String {
    case red, green, yellow

    mutating func next() {
        self = switch self {
        case .red: .green
        case .green: .yellow
        case .yellow: .red
        }
    }
}

func lightSequence(steps: Int) -> [String] {
    var light = TrafficLight.red
    var seen: [String] = []
    for _ in 0..<steps {
        light.next()
        seen.append(light.rawValue)
    }
    return seen
}
