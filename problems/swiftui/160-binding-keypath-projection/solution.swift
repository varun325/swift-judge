import SwiftUI

struct Profile {
    var name = "anon"
    var age = 0
}

final class Box: @unchecked Sendable {
    var profile = Profile()
    var writes = 0
}

@MainActor func run(_ edits: [String]) -> [String] {
    let box = Box()
    let root = Binding<Profile>(
        get: { box.profile },
        set: { box.profile = $0; box.writes += 1 }
    )
    let nameBinding: Binding<String> = root.name
    let ageBinding: Binding<Int> = root.age
    for edit in edits {
        let p = edit.split(separator: "=").map(String.init)
        if p[0] == "name" { nameBinding.wrappedValue = p[1] }
        if p[0] == "age", let a = Int(p[1]) { ageBinding.wrappedValue = a }
    }
    return ["\(box.profile.name) \(box.profile.age)", "writes \(box.writes)"]
}

func projectionDemo(_ edits: [String]) async -> [String] {
    await run(edits)
}
