func swapPair(_ pair: inout [Int]) {
    let temp = pair[0]
    pair[0] = pair[1]
    pair[1] = temp
}
