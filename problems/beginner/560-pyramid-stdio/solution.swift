let h = Int(readLine() ?? "") ?? 0
for i in stride(from: 1, through: h, by: 1) {
    print(String(repeating: " ", count: h - i) + String(repeating: "*", count: 2 * i - 1))
}
