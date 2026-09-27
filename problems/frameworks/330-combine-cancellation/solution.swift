import Combine

func lifetimes(_ steps: [String]) -> [String] {
    let subject = PassthroughSubject<Int, Never>()
    var log: [String] = []
    var kept = Set<AnyCancellable>()
    var counter = 0
    for step in steps {
        let p = step.split(separator: " ").map(String.init)
        switch p[0] {
        case "sub":
            counter += 1
            let k = counter
            subject.sink { log.append("s\(k):\($0)") }.store(in: &kept)
        case "temp":
            counter += 1
            let k = counter
            _ = subject.sink { log.append("s\(k):\($0)") }
        case "send": subject.send(Int(p.count > 1 ? p[1] : "") ?? 0)
        default:
            kept.forEach { $0.cancel() }
            kept.removeAll()
        }
    }
    return log.sorted()   // delivery order between subscribers isn't guaranteed
}
