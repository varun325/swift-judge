import Observation

@Observable
final class GameConfig {
    var name: String
    var pegChoices: [String]
    init(name: String, pegChoices: [String]) {
        self.name = name
        self.pegChoices = pegChoices
    }
    func copy() -> GameConfig { GameConfig(name: name, pegChoices: pegChoices) }

    var validationError: String? {
        if name.isEmpty { return "name" }
        if !(2...6).contains(pegChoices.count) { return "peg count" }
        if Set(pegChoices).count != pegChoices.count { return "duplicates" }
        return nil
    }
}

func editGames(_ actions: [String]) -> [String] {
    var games = [GameConfig(name: "Mastermind", pegChoices: ["R", "G", "B", "Y"])]
    var draft: GameConfig?
    var editing: GameConfig?
    var log: [String] = []
    for action in actions {
        let p = action.split(separator: " ", maxSplits: 1).map(String.init)
        let arg = p.count > 1 ? p[1] : ""
        switch p[0] {
        case "new": editing = nil; draft = GameConfig(name: "", pegChoices: [])
        case "edit": editing = games.first { $0.name == arg }; draft = editing?.copy()
        case "name": draft?.name = arg
        case "addPeg": draft?.pegChoices.append(arg)
        case "removePeg": if let i = draft?.pegChoices.firstIndex(of: arg) { draft?.pegChoices.remove(at: i) }
        case "cancel": draft = nil; editing = nil
        case "save":
            guard let d = draft else { break }
            if let error = d.validationError { log.append("invalid: \(error)"); break }
            if let original = editing {
                original.name = d.name
                original.pegChoices = d.pegChoices
            } else {
                games.append(d)
            }
            log.append("saved")
            draft = nil
            editing = nil
        default: break
        }
    }
    return log + games.map { "\($0.name)(\($0.pegChoices.joined()))" }
}
