import Foundation

struct Profile: Encodable {
    let name: String
    let followerCount: Int
    let isVerified: Bool
    let nickname: String?
}

func encodeProfile(name: String, followerCount: Int, isVerified: Bool, nickname: String?) -> String {
    let encoder = JSONEncoder()
    encoder.keyEncodingStrategy = .convertToSnakeCase
    encoder.outputFormatting = [.sortedKeys, .withoutEscapingSlashes]
    let data = (try? encoder.encode(Profile(name: name, followerCount: followerCount, isVerified: isVerified, nickname: nickname))) ?? Data()
    return String(decoding: data, as: UTF8.self)
}
