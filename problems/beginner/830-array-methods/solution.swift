func playlist(_ commands: [String]) -> [String] {
    var songs: [String] = []
    for command in commands {
        let parts = command.split(separator: " ", maxSplits: 1).map(String.init)
        switch (parts[0], parts.count) {
        case ("add", 2): songs.append(parts[1])
        case ("front", 2): songs.insert(parts[1], at: 0)
        case ("remove", 2):
            if let i = songs.firstIndex(of: parts[1]) { songs.remove(at: i) }
        case ("swap", 1): if songs.count >= 2 { songs.swapAt(0, songs.count - 1) }
        case ("reverse", 1): songs.reverse()
        case ("sort", 1): songs.sort()
        default: break
        }
    }
    return songs
}
