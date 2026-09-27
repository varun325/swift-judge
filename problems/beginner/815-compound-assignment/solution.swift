func scoreboard(_ events: [String]) -> [String] {
    var score = 10
    var title = "Game"
    for event in events {
        guard let op = event.first else { continue }
        let rest = String(event.dropFirst())
        if op == "!" { title += " " + rest; continue }
        guard let n = Int(rest) else { continue }
        switch op {
        case "+": score += n
        case "-": score -= n
        case "*": score *= n
        case "/": if n != 0 { score /= n }
        default: break
        }
    }
    return [title, "\(score)"]
}
