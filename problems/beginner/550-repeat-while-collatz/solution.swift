func collatzSteps(_ n: Int) -> Int {
    var value = n
    var steps = 0
    while value != 1 {
        value = value.isMultiple(of: 2) ? value / 2 : 3 * value + 1
        steps += 1
    }
    return steps
}
