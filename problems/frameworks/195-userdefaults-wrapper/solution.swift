import Foundation

// A suite named by an absolute path is a private plist file: one per process, in the temp
// directory, so parallel runs never clobber each other and ~/Library/Preferences stays clean.
let suiteName = NSTemporaryDirectory() + "swift-judge-stored-\(ProcessInfo.processInfo.processIdentifier)"

@propertyWrapper
struct Stored<Value: Codable> {
    let key: String
    let defaultValue: Value
    let store: UserDefaults

    init(_ key: String, default defaultValue: Value, store: UserDefaults = UserDefaults(suiteName: suiteName)!) {
        self.key = key
        self.defaultValue = defaultValue
        self.store = store
    }

    var wrappedValue: Value {
        get {
            guard let data = store.data(forKey: key), let value = try? JSONDecoder().decode(Value.self, from: data) else { return defaultValue }
            return value
        }
        set { store.set(try? JSONEncoder().encode(newValue), forKey: key) }
    }
}

struct Preferences {
    @Stored("theme", default: "system") var theme: String
    @Stored("fontSize", default: 14) var fontSize: Int
    @Stored("recent", default: []) var recent: [String]
}

func settingsRoundTrip(_ writes: [String]) -> [String] {
    UserDefaults(suiteName: suiteName)!.removePersistentDomain(forName: suiteName)
    var prefs = Preferences()
    for w in writes {
        let p = w.split(separator: "=", maxSplits: 1).map(String.init)
        guard p.count == 2 else { continue }
        switch p[0] {
        case "theme": prefs.theme = p[1]
        case "font": if let n = Int(p[1]) { prefs.fontSize = n }
        case "recent": prefs.recent = Array(([p[1]] + prefs.recent).prefix(3))
        default: break
        }
    }
    let relaunched = Preferences()
    let out = [relaunched.theme, String(relaunched.fontSize), relaunched.recent.joined(separator: ",")]
    UserDefaults(suiteName: suiteName)!.removePersistentDomain(forName: suiteName)
    try? FileManager.default.removeItem(atPath: suiteName + ".plist")
    return out
}
