func djb2(_ text: String) -> Int {
    var hash = 5381
    for byte in text.utf8 {
        hash = hash &* 33 &+ Int(byte)
    }
    return hash
}
