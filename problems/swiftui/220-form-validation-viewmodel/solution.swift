import Observation

@Observable
final class SignUpModel {
    var email = ""
    var password = ""
    var confirm = ""
    var agreed = false

    var errors: [String] {
        var e: [String] = []
        let parts = email.split(separator: "@")
        if parts.count != 2 || !parts[1].contains(".") { e.append("email") }
        if password.count < 8 { e.append("short password") }
        if password != confirm { e.append("mismatch") }
        if !agreed { e.append("terms") }
        return e
    }

    var canSubmit: Bool { errors.isEmpty }
}

func signUpStates(_ edits: [String]) -> [String] {
    let model = SignUpModel()
    return edits.map { edit in
        let p = edit.split(separator: "=", maxSplits: 1).map(String.init)
        switch p[0] {
        case "email": model.email = p.count > 1 ? p[1] : ""
        case "password": model.password = p.count > 1 ? p[1] : ""
        case "confirm": model.confirm = p.count > 1 ? p[1] : ""
        default: model.agreed = true
        }
        return "\(model.canSubmit) [\(model.errors.joined(separator: ","))]"
    }
}
