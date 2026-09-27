enum EmailError: Error { case missingAt, emptyUser, emptyDomain }

struct Email {
    let value: String

    init(validating raw: String) throws {
        let parts = raw.split(separator: "@", omittingEmptySubsequences: false)
        guard parts.count == 2 else { throw EmailError.missingAt }
        guard !parts[0].isEmpty else { throw EmailError.emptyUser }
        guard !parts[1].isEmpty else { throw EmailError.emptyDomain }
        value = raw.lowercased()
    }

    init?(_ raw: String) {
        guard let email = try? Email(validating: raw) else { return nil }
        self = email
    }
}

func makeEmails(_ inputs: [String]) -> [String] {
    inputs.map { raw in
        if let email = Email(raw) { return "\(email.value) ok" }
        do { _ = try Email(validating: raw); return "?" } catch { return "\(error)" }
    }
}
