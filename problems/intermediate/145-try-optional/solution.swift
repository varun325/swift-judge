enum DivisionError: Error { case byZero, overflow }

func divide(_ a: Int, by b: Int) throws -> Int {
    guard b != 0 else { throw DivisionError.byZero }
    let (q, overflow) = a.dividedReportingOverflow(by: b)
    guard !overflow else { throw DivisionError.overflow }
    return q
}

func safeDivisions(_ pairs: [[Int]]) -> [Int?] {
    pairs.map { try? divide($0[0], by: $0[1]) }
}
