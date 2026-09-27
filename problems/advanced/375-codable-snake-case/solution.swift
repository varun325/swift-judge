import Foundation

struct User: Codable {
    let userId: Int
    let firstName: String
    let isAdmin: Bool
    let email: String?

    enum CodingKeys: String, CodingKey {
        case userId, firstName, isAdmin
        case email = "e-mail"
    }
}

func decodeUsers(_ json: String) -> [String] {
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    guard let users = try? decoder.decode([User].self, from: Data(json.utf8)) else { return ["invalid"] }
    return users.map { "\($0.userId):\($0.firstName):\($0.isAdmin ? "admin" : "user"):\($0.email ?? "none")" }
}
