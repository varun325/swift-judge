struct Employee {
    let name: String
    var vacationAllowed = 14
    var vacationTaken = 0

    var vacationRemaining: Int {
        get { vacationAllowed - vacationTaken }
        set { vacationAllowed = vacationTaken - newValue }
    }
}

func vacationRoundTrip(taken: Int, remaining: Int) -> [Int] {
    var e = Employee(name: "varun")
    e.vacationTaken = taken
    e.vacationRemaining = remaining
    return [e.vacationAllowed, e.vacationRemaining]
}
