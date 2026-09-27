let flag = "🇮🇳"
let word = "cafe\u{301}"
print(flag.count, flag.unicodeScalars.count, flag.utf8.count)
print(word, word.count, word == "café")
let s = "Hello, Swift"
let i = s.firstIndex(of: ",")!
print(s[..<i], s[s.index(after: i)...].trimmingPrefix(" "))
print(s.prefix(4), s.suffix(3), s.dropFirst(7).uppercased())
print(String(s.reversed()))
let words: [Substring] = s.split(separator: " ")
print(words.map { $0.count })
