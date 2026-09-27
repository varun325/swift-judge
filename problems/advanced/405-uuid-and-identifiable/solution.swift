import Foundation

struct Todo: Identifiable {
    let id = UUID()
    let title: String
}

func uuidChecks(_ strings: [String]) -> [String] {
    var out = strings.map { s in UUID(uuidString: s).map { "valid \($0.uuidString)" } ?? "invalid" }
    out.append(UUID() != UUID() ? "unique" : "collision")
    out.append("\(UUID().uuidString.count)")
    out.append(Todo(title: "x").id != Todo(title: "x").id ? "ids differ" : "same")
    return out
}
