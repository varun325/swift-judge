func character(in text: String, at offset: Int) -> String? {
    guard offset >= 0,
          let index = text.index(text.startIndex, offsetBy: offset, limitedBy: text.endIndex),
          index < text.endIndex
    else { return nil }
    return String(text[index])
}
