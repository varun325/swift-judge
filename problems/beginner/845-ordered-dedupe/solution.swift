func dedupe(_ values: [Int]) -> [Int] {
    var seen = Set<Int>()
    return values.filter { seen.insert($0).inserted }
}
