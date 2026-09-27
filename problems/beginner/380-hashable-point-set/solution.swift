struct Point: Hashable {
    let x: Int
    let y: Int
}

func uniquePointCount(_ coords: [[Int]]) -> Int {
    Set(coords.map { Point(x: $0[0], y: $0[1]) }).count
}
