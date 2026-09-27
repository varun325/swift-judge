import Combine

func subjectsDemo(_ events: [String]) -> [String] {
    let messages = PassthroughSubject<String, Never>()
    let score = CurrentValueSubject<Int, Never>(0)
    var early: [String] = []
    var late: [String] = []
    var bag = Set<AnyCancellable>()
    messages.sink { early.append("early:\($0)") }.store(in: &bag)
    score.sink { early.append("early:\($0)") }.store(in: &bag)
    for e in events {
        let p = e.split(separator: " ", maxSplits: 1).map(String.init)
        switch p[0] {
        case "emit": messages.send(p.count > 1 ? p[1] : "")
        case "score": score.send(Int(p.count > 1 ? p[1] : "") ?? 0)
        case "subscribe":
            messages.sink { late.append("late:\($0)") }.store(in: &bag)
            score.sink { late.append("late:\($0)") }.store(in: &bag)
        default:
            messages.send(completion: .finished)
            score.send(completion: .finished)
        }
    }
    return early + ["--"] + late
}
