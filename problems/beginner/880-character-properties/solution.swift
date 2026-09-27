func strength(_ password: String) -> String {
    let checks = [
        password.count >= 8,
        password.contains(where: \.isUppercase),
        password.contains(where: \.isLowercase),
        password.contains(where: \.isNumber),
        password.contains { !$0.isLetter && !$0.isNumber },
    ]
    switch checks.filter { $0 }.count {
    case 0...2: return "weak"
    case 3...4: return "medium"
    default: return "strong"
    }
}
