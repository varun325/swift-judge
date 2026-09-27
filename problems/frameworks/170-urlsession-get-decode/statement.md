Swiftful's *Download JSON from API*. Write `func fetchUsers(session: URLSession) async throws -> [User]` calling `GET https://api.example.com/users`, checking the response is an `HTTPURLResponse` with a 2xx status (else throw `APIError.badStatus(code)`), and decoding `[User]` (`id`, `name`).

 The judge wires a **mock `URLProtocol`** (given in the starter) so no real network is used. Return user names, or `"error <APIError or decoding>"`.
