func stepper(backward: Bool, start: Int, steps: Int) -> [Int] {
    func stepForward(_ x: Int) -> Int { x + 1 }
    func stepBackward(_ x: Int) -> Int { x - 1 }
    let step: (Int) -> Int = backward ? stepBackward : stepForward
    var current = start
    var visited: [Int] = []
    for _ in 0..<max(0, steps) {
        current = step(current)
        visited.append(current)
    }
    return visited
}
