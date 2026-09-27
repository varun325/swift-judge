struct Guess {
    let choices: [String]
    var pegs: [String?]

    mutating func changeGuessPeg(at index: Int) {
        guard pegs.indices.contains(index), !choices.isEmpty else { return }
        if let current = pegs[index], let i = choices.firstIndex(of: current) {
            pegs[index] = choices[(i + 1) % choices.count]
        } else {
            pegs[index] = choices.first
        }
    }
}

func cyclePegs(choices: [String], slots: Int, taps: [Int]) -> [String] {
    var guess = Guess(choices: choices, pegs: Array(repeating: nil, count: max(slots, 0)))
    taps.forEach { guess.changeGuessPeg(at: $0) }
    return guess.pegs.map { $0 ?? "-" }
}
