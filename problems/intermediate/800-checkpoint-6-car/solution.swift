struct Car {
    let model: String
    let seats: Int
    let maxGears: Int
    private(set) var gear = 1

    mutating func changeGear(by delta: Int) -> Bool {
        let next = gear + delta
        guard (1...maxGears).contains(next) else { return false }
        gear = next
        return true
    }
}

func driveCar(maxGears: Int, changes: [Int]) -> [String] {
    var car = Car(model: "Swiftmobile", seats: 4, maxGears: maxGears)
    return changes.map { car.changeGear(by: $0) ? "gear \(car.gear)" : "refused at \(car.gear)" }
}
