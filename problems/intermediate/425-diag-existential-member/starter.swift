protocol Vehicle { func travel() }

struct Car: Vehicle {
    func travel() {}
    func openSunroof() {}
}

func commute(_ vehicle: any Vehicle) {
    vehicle.travel()
    if let car = vehicle as? Car { car.openSunroof() }
}
