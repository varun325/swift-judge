func make(_ label: String) -> String { print("making", label); return label }

enum Config {
    static let apiURL = make("apiURL")
    static let timeout = make("timeout")
}

print("program start")
print(Config.timeout)
print(Config.timeout)
print(Config.apiURL)
