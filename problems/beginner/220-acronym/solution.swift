func acronym(_ phrase: String) -> String {
    String(phrase.split(whereSeparator: { $0 == " " || $0 == "-" }).compactMap(\.first)).uppercased()
}
