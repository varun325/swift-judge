func fnv1a(_ s: String) -> UInt32 {
    var hash: UInt32 = 2_166_136_261
    for byte in s.utf8 {
        hash ^= UInt32(byte)
        hash = hash &* 16_777_619
    }
    return hash
}

func assignVariants(userIDs: [String], experiment: String, splits: [Int]) -> [String] {
    userIDs.map { user in
        let bucket = Int(fnv1a("\(experiment):\(user)") % 100)
        var cumulative = 0
        var variant = "control"
        for (i, pct) in splits.enumerated() {
            cumulative += pct
            if bucket < cumulative {
                variant = String(UnicodeScalar(UInt8(65 + i)))
                break
            }
        }
        return "\(user): \(variant) (bucket \(bucket))"
    }
}
