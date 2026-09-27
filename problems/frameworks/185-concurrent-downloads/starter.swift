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

 func loadProfiles(_ ids: [Int], failing: [Int]) async -> [String] {
     MockURLProtocol.routes = [:]
     for id in ids { MockURLProtocol.routes["GET /users/\(id)"] = failing.contains(id) ? (500, "{}") : (200, "{\"name\": \"user\(id)\"}") }
     let session = mockSession()
     // fetch all concurrently, keep input order
     return []
 }
