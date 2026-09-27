Decode JSON like:
 ```json
 [{"user_id": 1, "first_name": "Ana", "is_admin": true, "e-mail": "a@x.io"}]
 ```
 into `struct User: Codable { let userId: Int; let firstName: String; let isAdmin: Bool; let email: String? }` using `keyDecodingStrategy = .convertFromSnakeCase` **plus** a `CodingKeys` enum to map `"e-mail"` (which snake case conversion can't handle).

 Return `"<id>:<name>:<admin|user>:<email or none>"` per user, or `["invalid"]` if decoding fails.
