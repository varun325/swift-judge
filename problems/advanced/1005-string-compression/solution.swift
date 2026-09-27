func compress(_ s: String) -> String {
    var out = ""
    var previous: Character?
    var count = 0
    for ch in s {
        if ch == previous {
            count += 1
        } else {
            if let p = previous { out += "\(p)\(count)" }
            previous = ch
            count = 1
        }
    }
    if let p = previous { out += "\(p)\(count)" }
    return out.count < s.count ? out : s
}
