enum PasswordError: Error {
    case short, obvious
}

func checkPassword(_ password: String) throws -> String {
    if password.count < 5 { throw PasswordError.short }
    if ["12345", "password"].contains(password) { throw PasswordError.obvious }
    return password.count < 10 ? "OK" : "Good"
}
