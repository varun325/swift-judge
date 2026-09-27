func inlineDemo(_ values: [Int]) -> [Int] {
    var board = InlineArray<4, Int>(repeating: 0)
    for i in board.indices where i < values.count { board[i] = values[i] }
    for i in board.indices { board[i] *= 2 }
    var copy = board
    copy[0] = -1
    var sum = 0
    for i in board.indices { sum += board[i] }
    return [sum, board[0], copy[0], MemoryLayout<InlineArray<4, Int>>.size]
}
