import Foundation

let words = ["apple", "Banana", "cherry", "date", "Elder"]
print(words.count(where: { $0.first?.isUppercase == true }))
print(words.firstIndex(where: { $0.count > 5 }) ?? -1)
print(words.min(by: { $0.count < $1.count }) ?? "-")
print(words.split(whereSeparator: { $0 == "cherry" }).map(\.count))
print(words.allSatisfy { $0.count >= 4 }, words.contains { $0.hasSuffix("y") })
print(Array(words.prefix(while: { $0.first?.isLowercase == true })))
print(words.sorted(using: KeyPathComparator(\.count)).first!)
