func visibleColumns(_ states: [[String]]) -> [String] {
    states.map { s in
        let selection: String? = s[1] == "-" ? nil : s[1]
        if s[0] == "compact" {
            return selection.map { "detail(\($0))" } ?? "list"
        }
        if s[2] == "detailOnly", let selection { return "detail(\(selection))" }
        return "list+detail(\(selection ?? "Choose a game"))"
    }
}
