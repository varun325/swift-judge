final class ParkingLot {
    enum Size: Int { case big = 1, medium, small }
    private var free: [Size: Int]

    init(big: Int, medium: Int, small: Int) {
        free = [.big: big, .medium: medium, .small: small]
    }

    func park(_ carType: Int) -> Bool {
        guard let size = Size(rawValue: carType), let slots = free[size], slots > 0 else { return false }
        free[size] = slots - 1
        return true
    }
}
