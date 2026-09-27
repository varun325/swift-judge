var people: [(first: String, last: String)] = []
while let line = readLine() {
    let parts = line.split(separator: " ")
    guard parts.count == 2 else { continue }
    people.append((String(parts[0]), String(parts[1])))
}
for p in people.sorted(by: { ($0.last.lowercased(), $0.first.lowercased()) < ($1.last.lowercased(), $1.first.lowercased()) }) {
    print("\(p.last.uppercased()), \(p.first)")
}
