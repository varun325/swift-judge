import CryptoKit
import Foundation

func digests(_ inputs: [String]) -> [String] {
    inputs.map { input in
        SHA256.hash(data: Data(input.utf8)).map { String(format: "%02x", $0) }.joined()
    }
}
