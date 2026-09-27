var scores: [String: [Int]] = [:]
while let line = readLine() {
    let parts = line.split(separator: " ")
    guard parts.count == 2, let score = Int(parts[1]), (0...100).contains(score) else { continue }
    scores[String(parts[0]), default: []].append(score)
}
func roundedAverage(_ xs: [Int]) -> Int { Int((Double(xs.reduce(0, +)) / Double(xs.count)).rounded()) }
for (name, list) in scores.sorted(by: { $0.key < $1.key }) {
    print("\(name) avg=\(roundedAverage(list)) best=\(list.max()!) n=\(list.count)")
}
let all = scores.values.flatMap { $0 }
print("class avg=\(all.isEmpty ? "n/a" : String(roundedAverage(all)))")
