import Combine

func combine(_ events: [String], mode: String) -> [String] {
    let a = PassthroughSubject<Int, Never>()
    let b = PassthroughSubject<String, Never>()
    var log: [String] = []
    let cancellable: AnyCancellable
    switch mode {
    case "combineLatest": cancellable = a.combineLatest(b).sink { log.append("\($0)-\($1)") }
    case "zip": cancellable = a.zip(b).sink { log.append("\($0)-\($1)") }
    default: cancellable = a.map { "a\($0)" }.merge(with: b.map { "b\($0)" }).sink { log.append($0) }
    }
    for e in events {
        let p = e.split(separator: " ", maxSplits: 1).map(String.init)
        if p[0] == "a" { a.send(Int(p.count > 1 ? p[1] : "") ?? 0) } else { b.send(p.count > 1 ? p[1] : "") }
    }
    _ = cancellable
    return log
}
