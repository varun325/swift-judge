struct CodeBreaker {
    let master: [String]
    let maxAttempts: Int
    private(set) var attempts: [[String]] = []

    var isSolved: Bool { attempts.last == master }
    var isOver: Bool { isSolved || attempts.count >= maxAttempts }
    var masterDisplay: String { isOver ? master.joined() : String(repeating: "?", count: master.count) }

    mutating func attempt(_ guess: [String]) -> Bool {
        guard !isOver, guess.count == master.count, !attempts.contains(guess) else { return false }
        attempts.append(guess)
        return true
    }

    mutating func restart() { attempts = [] }
}

func playRound(master: [String], guesses: [[String]], maxAttempts: Int) -> [String] {
    var game = CodeBreaker(master: master, maxAttempts: maxAttempts)
    return guesses.map { g in
        var status: String
        if g == ["restart"] {
            game.restart()
            status = "playing"
        } else if !game.attempt(g) {
            status = "rejected"
        } else {
            status = game.isSolved ? "solved" : game.isOver ? "lost" : "playing"
        }
        return "\(game.attempts.count) \(game.masterDisplay) \(status)"
    }
}
