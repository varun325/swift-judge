import CryptoKit
import Foundation

func secureMessages(_ messages: [String], tamperIndex: Int) -> [String] {
    let key = HKDF<SHA256>.deriveKey(
        inputKeyMaterial: SymmetricKey(data: Data("correct horse battery staple".utf8)),
        salt: Data("swift-judge".utf8),
        info: Data("demo".utf8),
        outputByteCount: 32
    )
    var log: [String] = []
    for (i, message) in messages.enumerated() {
        let signature = HMAC<SHA256>.authenticationCode(for: Data(message.utf8), using: key)
        let received = i == tamperIndex ? message + "!" : message
        log.append(HMAC<SHA256>.isValidAuthenticationCode(signature, authenticating: Data(received.utf8), using: key) ? "sig ok" : "sig bad")

        guard let sealed = try? AES.GCM.seal(Data(message.utf8), using: key), var combined = sealed.combined else { continue }
        if i == tamperIndex { combined[combined.count - 1] ^= 0xFF }
        if let box = try? AES.GCM.SealedBox(combined: combined), let plain = try? AES.GCM.open(box, using: key) {
            log.append(String(decoding: plain, as: UTF8.self))
        } else {
            log.append("decrypt failed")
        }
    }
    return log
}
