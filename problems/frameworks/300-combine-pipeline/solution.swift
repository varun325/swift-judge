import Combine

func runningTotals(_ readings: [Int]) -> [Int] {
    var out: [Int] = []
    let cancellable = readings.publisher
        .filter { $0 >= 0 }
        .removeDuplicates()
        .scan(0, +)
        .sink { out.append($0) }
    _ = cancellable
    return out
}
