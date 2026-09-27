func reviewPrompts(_ events: [[String]]) -> [String] {
    var successes = 0
    var lastCrash: Int?
    var prompts: [Int] = []
    var out: [String] = []
    for e in events {
        guard e.count == 2, let day = Int(e[0]) else { continue }
        switch e[1] {
        case "crash": lastCrash = day
        case "success":
            successes += 1
            let noRecentCrash = lastCrash.map { day - $0 > 7 } ?? true
            let spaced = prompts.last.map { day - $0 >= 60 } ?? true
            let yearly = prompts.count(where: { day - $0 < 365 }) < 3
            if successes >= 3 && noRecentCrash && spaced && yearly {
                prompts.append(day)
                out.append("prompt day \(day)")
            }
        default: break
        }
    }
    return out
}
