class Employee {
    let hours: Int
    init(hours: Int) { self.hours = hours }
    func summary() -> String { "I work \(hours) hours a day." }
}

final class Developer: Employee {
    override func summary() -> String { "I spend \(hours) hours a day fighting over tabs vs spaces" }
}

final class Manager: Employee {
    override func summary() -> String { "I schedule meetings for \(hours) hours, then " + super.summary() }
}

func summaries(_ roles: [String], hours: Int) -> [String] {
    let staff: [Employee] = roles.map {
        switch $0 {
        case "dev": Developer(hours: hours)
        case "mgr": Manager(hours: hours)
        default: Employee(hours: hours)
        }
    }
    return staff.map { $0.summary() }
}
