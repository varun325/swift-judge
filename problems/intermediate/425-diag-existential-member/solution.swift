protocol Vehicle { func travel() }

struct Car: Vehicle {
    func travel() {}
    func openSunroof() {}
}

func commute(_ vehicle: any Vehicle) {
    vehicle.openSunroof()
}
