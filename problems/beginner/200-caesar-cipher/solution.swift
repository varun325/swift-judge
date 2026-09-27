func caesar(_ text: String, shift: Int) -> String {
    let k = ((shift % 26) + 26) % 26
    return String(text.map { ch -> Character in
        guard let ascii = ch.asciiValue, ch.isLetter else { return ch }
        let base: UInt8 = ch.isUppercase ? 65 : 97
        return Character(UnicodeScalar((Int(ascii - base) + k) % 26 + Int(base))!)
    })
}
