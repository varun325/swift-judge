import Foundation

 final class EchoURLProtocol: URLProtocol, @unchecked Sendable {
     nonisolated(unsafe) static var last: URLRequest?
     nonisolated(unsafe) static var lastBody = Data()
     override class func canInit(with request: URLRequest) -> Bool { true }
     override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
     override func startLoading() {
         EchoURLProtocol.last = request
         if let stream = request.httpBodyStream {
             stream.open(); var data = Data(); var buffer = [UInt8](repeating: 0, count: 1024)
             while stream.hasBytesAvailable { let n = stream.read(&buffer, maxLength: 1024); if n <= 0 { break }; data.append(buffer, count: n) }
             stream.close(); EchoURLProtocol.lastBody = data
         } else { EchoURLProtocol.lastBody = request.httpBody ?? Data() }
         let response = HTTPURLResponse(url: request.url!, statusCode: 201, httpVersion: nil, headerFields: nil)!
         client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
         client?.urlProtocol(self, didLoad: Data("{\"id\": 42}".utf8))
         client?.urlProtocolDidFinishLoading(self)
     }
     override func stopLoading() {}
 }

 struct NewTodo: Encodable { let title: String; let done: Bool }
 struct Created: Decodable { let id: Int }

 func createTodo(title: String, token: String) async -> [String] {
     let config = URLSessionConfiguration.ephemeral
     config.protocolClasses = [EchoURLProtocol.self]
     let session = URLSession(configuration: config)

     var request = URLRequest(url: URL(string: "https://api.example.com/todos")!)
     request.httpMethod = "POST"
     request.setValue("application/json", forHTTPHeaderField: "Content-Type")
     request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
     let encoder = JSONEncoder()
     encoder.outputFormatting = .sortedKeys
     request.httpBody = try? encoder.encode(NewTodo(title: title, done: false))

     guard let (data, _) = try? await session.data(for: request),
           let created = try? JSONDecoder().decode(Created.self, from: data),
           let sent = EchoURLProtocol.last else { return ["failed"] }
     return [
         sent.httpMethod ?? "",
         sent.value(forHTTPHeaderField: "Content-Type") ?? "",
         sent.value(forHTTPHeaderField: "Authorization") ?? "",
         String(decoding: EchoURLProtocol.lastBody, as: UTF8.self),
         "id \(created.id)",
     ]
 }
