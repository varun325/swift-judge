func validateSignup(username: String?, age: String?, email: String?) -> String {
    guard let username, (3...16).contains(username.count) else { return "bad username" }
    guard let age, let years = Int(age), years >= 13 else { return "bad age" }
    guard let email else { return "bad email" }
    let parts = email.split(separator: "@", omittingEmptySubsequences: false)
    guard parts.count == 2, !parts[0].isEmpty, !parts[1].isEmpty else { return "bad email" }
    return "welcome \(username)"
}
