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

 struct Profile: Decodable { let name: String }

 func fetchProfile(_ id: Int, session: URLSession) async -> String? {
     guard let (data, response) = try? await session.data(from: URL(string: "https://api.example.com/users/\(id)")!),
           let http = response as? HTTPURLResponse, http.statusCode < 400,
           let profile = try? JSONDecoder().decode(Profile.self, from: data) else { return nil }
     return profile.name
 }

 func loadProfiles(_ ids: [Int], failing: [Int]) async -> [String] {
     MockURLProtocol.routes = [:]
     for id in ids { MockURLProtocol.routes["GET /users/\(id)"] = failing.contains(id) ? (500, "{}") : (200, "{\"name\": \"user\(id)\"}") }
     let session = mockSession()
     let names = await withTaskGroup(of: (Int, String?).self) { group in
         for (i, id) in ids.enumerated() {
             group.addTask { (i, await fetchProfile(id, session: session)) }
         }
         var results = [String?](repeating: nil, count: ids.count)
         for await (i, name) in group { results[i] = name }
         return results
     }
     return zip(ids, names).map { "\($0): \($1 ?? "failed")" }
 }
