func lengths(_ text: String) -> [Int] {
    [text.count, text.unicodeScalars.count, text.utf16.count, text.utf8.count]
}
