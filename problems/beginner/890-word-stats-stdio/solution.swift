var text = ""
while let line = readLine() { text += line + "\n" }
let words = text.split(whereSeparator: \.isWhitespace)
print("words: \(words.count)")
let longest = words.reduce(nil as Substring?) { best, w in (best == nil || w.count > best!.count) ? w : best }
print("longest: \(longest.map(String.init) ?? "-")")
var counts: [Character: Int] = [:]
for ch in text.lowercased() where ch.isLetter { counts[ch, default: 0] += 1 }
let top = counts.min { ($1.value, $0.key) < ($0.value, $1.key) }
print("top: \(top.map { String($0.key) } ?? "-")")
