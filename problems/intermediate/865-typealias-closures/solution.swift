typealias Validator = @Sendable (String) -> String?

let validators: [Validator] = [
    { $0.isEmpty ? "empty" : nil },
    { $0.count > 10 ? "too long" : nil },
    { $0.contains(" ") ? "has spaces" : nil },
]

func validateAll(_ inputs: [String]) -> [String] {
    inputs.map { input in validators.lazy.compactMap { $0(input) }.first ?? "ok" }
}
