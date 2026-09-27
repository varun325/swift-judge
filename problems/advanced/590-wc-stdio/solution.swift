var lines = 0, words = 0, chars = 0
while let line = readLine() {
    lines += 1
    words += line.split(whereSeparator: \.isWhitespace).count
    chars += line.count
}
print(lines, words, chars)
