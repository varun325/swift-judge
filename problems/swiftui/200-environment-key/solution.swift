import SwiftUI

extension EnvironmentValues {
    @Entry var accentName: String = "blue"
    @Entry var cornerStyle: Int = 8
}

@MainActor func run(_ overrides: [String]) -> [String] {
    var env = EnvironmentValues()
    let before = "\(env.accentName) \(env.cornerStyle)"
    for o in overrides {
        let p = o.split(separator: "=").map(String.init)
        if p[0] == "accent" { env.accentName = p[1] }
        if p[0] == "corner", let n = Int(p[1]) { env.cornerStyle = n }
    }
    return [before, "\(env.accentName) \(env.cornerStyle)"]
}

func environmentDemo(_ overrides: [String]) async -> [String] {
    await run(overrides)
}
