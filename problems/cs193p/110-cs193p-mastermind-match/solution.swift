func match(_ guess: [String], against master: [String]) -> (exact: Int, inexact: Int) {
    let pairs = zip(guess, master)
    let exact = pairs.count(where: { $0 == $1 && !$0.isEmpty })
    // Count remaining (non-exact) pegs of each colour on both sides; inexact = overlap.
    var masterLeft: [String: Int] = [:], guessLeft: [String: Int] = [:]
    for (g, m) in pairs where g != m || g.isEmpty {
        if !m.isEmpty { masterLeft[m, default: 0] += 1 }
        if !g.isEmpty { guessLeft[g, default: 0] += 1 }
    }
    let inexact = guessLeft.reduce(0) { $0 + min($1.value, masterLeft[$1.key] ?? 0) }
    return (exact, inexact)
}

func score(master: [String], guesses: [[String]]) -> [String] {
    guesses.map { guess in
        let r = match(guess, against: master)
        return "\(r.exact)E \(r.inexact)I"
    }
}
