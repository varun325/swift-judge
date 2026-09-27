import Foundation

 /// Offline test server: URLSession requests are answered by `routes` instead of the network.
 final class MockURLProtocol: URLProtocol, @unchecked Sendable {
     nonisolated(unsafe) static var routes: [String: (status: Int, body: String)] = [:]
     nonisolated(unsafe) static var requests: [String] = []
     override class func canInit(with request: URLRequest) -> Bool { true }
     override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
     override func startLoading() {
         let url = request.url!
         let key = "\(request.httpMethod ?? "GET") \(url.path)\(url.query.map { "?" + $0 } ?? "")"
         MockURLProtocol.requests.append(key)
         let route = MockURLProtocol.routes[key] ?? (404, "{}")
         let response = HTTPURLResponse(url: url, statusCode: route.status, httpVersion: nil, headerFields: ["Content-Type": "application/json"])!
         client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
         client?.urlProtocol(self, didLoad: Data(route.body.utf8))
         client?.urlProtocolDidFinishLoading(self)
     }
     override func stopLoading() {}
 }

 func mockSession() -> URLSession {
     let config = URLSessionConfiguration.ephemeral
     config.protocolClasses = [MockURLProtocol.self]
     return URLSession(configuration: config)
 }

 struct User: Decodable { let id: Int; let name: String }
 enum APIError: Error { case badStatus(Int) }

 func fetchUsers(session: URLSession) async throws -> [User] {
     let url = URL(string: "https://api.example.com/users")!
     let (data, response) = try await session.data(from: url)
     guard let http = response as? HTTPURLResponse else { throw APIError.badStatus(-1) }
     guard (200..<300).contains(http.statusCode) else { throw APIError.badStatus(http.statusCode) }
     return try JSONDecoder().decode([User].self, from: data)
 }

 func loadUsers(status: Int, body: String) async -> [String] {
     MockURLProtocol.routes = ["GET /users": (status, body)]
     do {
         return try await fetchUsers(session: mockSession()).map(\.name)
     } catch let error as APIError {
         return ["error \(error)"]
     } catch {
         return ["error decoding"]
     }
 }
