func vowelCount(_ text: String) -> Int {
    let vowels: Set<Character> = ["a", "e", "i", "o", "u"]
    return text.lowercased().filter { vowels.contains($0) }.count
}
