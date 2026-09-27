func captureDemo(start: Int) -> [Int] {
    var x = start
    let byRef = { x }
    let bySnapshot = { [x] in x }
    x += 5
    return [byRef(), bySnapshot()]
}
