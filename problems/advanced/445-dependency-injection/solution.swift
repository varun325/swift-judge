import Foundation

protocol Clock { var hour: Int { get } }

struct FixedClock: Clock { let hour: Int }

final class SystemClock: Clock, Sendable {
    static let shared = SystemClock()
    private init() {}
    var hour: Int { Calendar.current.component(.hour, from: Date()) }
}

struct Greeter {
    let clock: any Clock
    init(clock: any Clock = SystemClock.shared) { self.clock = clock }

    func greeting() -> String {
        switch clock.hour {
        case ..<12: "Good morning"
        case ..<18: "Good afternoon"
        default: "Good evening"
        }
    }
}

func greetingsAt(_ hours: [Int], useLive: Bool) -> [String] {
    if useLive {
        let g = Greeter().greeting()
        return ["Good morning", "Good afternoon", "Good evening"].contains(g) ? ["live ok"] : ["bad"]
    }
    return hours.map { Greeter(clock: FixedClock(hour: $0)).greeting() }
}
