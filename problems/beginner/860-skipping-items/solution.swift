func sumValidReadings(_ readings: [String]) -> [Int] {
    var sum = 0, used = 0
    for reading in readings {
        if reading == "END" { break }
        guard let value = Int(reading), value >= 0 else { continue }
        sum += value
        used += 1
    }
    return [sum, used]
}
