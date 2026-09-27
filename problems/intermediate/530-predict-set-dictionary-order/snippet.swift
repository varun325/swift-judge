let a: Set = [3, 1, 4, 1, 5, 9, 2, 6]
let b: Set = [2, 7, 1, 8, 2, 8]
print(a.count, b.count)
print(a.intersection(b).sorted())
print(a.isSuperset(of: [1, 9]), b.isDisjoint(with: [3, 4]))
var counts: [Character: Int] = [:]
for ch in "mississippi" { counts[ch, default: 0] += 1 }
print(counts.sorted { $0.key < $1.key }.map { "\($0.key)\($0.value)" }.joined())
print(counts["z"] as Any, counts["s", default: 0])
