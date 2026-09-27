typealias Peg = String

enum Match { case nomatch, exact, inexact }

struct Code {
    enum Kind {
        case master(isHidden: Bool)
        case guess
        case attempt([Match])
        case unknown
    }
    var kind: Kind
    var pegs: [Peg]

    var isHidden: Bool {
        if case .master(let hidden) = kind { return hidden }
        return false
    }

    func match(against other: Code) -> [Match] {
        let exact = zip(pegs, other.pegs).map { $0 == $1 }
        var remaining = other.pegs.enumerated().filter { !exact[$0.offset] }.map(\.element)
        return pegs.indices.map { i in
            if exact[i] { return .exact }
            if let j = remaining.firstIndex(of: pegs[i]) { remaining.remove(at: j); return .inexact }
            return .nomatch
        }
    }
}

func codeBoard(master: [String], attempts: [[String]]) -> [String] {
    var masterCode = Code(kind: .master(isHidden: true), pegs: master)
    var lines: [String] = []
    var won = false
    for pegs in attempts {
        let matches = Code(kind: .guess, pegs: pegs).match(against: masterCode)
        lines.append("attempt:\(pegs.joined()) \(matches.count(where: { $0 == .exact }))E\(matches.count(where: { $0 == .inexact }))I")
        if !matches.isEmpty && matches.allSatisfy({ $0 == .exact }) { won = true }
    }
    if won { masterCode.kind = .master(isHidden: false) }
    return ["master:\(masterCode.isHidden ? String(repeating: "?", count: master.count) : master.joined())"] + lines + [won ? "won" : "playing"]
}
