import Foundation
 let header = readLine()?.split(separator: ",", omittingEmptySubsequences: false).map(String.init) ?? []
 var sums = Array(repeating: 0.0, count: header.count)
 while let line = readLine() {
     let cells = line.split(separator: ",", omittingEmptySubsequences: false)
     for (i, cell) in cells.enumerated() where i < sums.count {
         if let v = Double(cell.trimmingCharacters(in: .whitespaces)) { sums[i] += v }
     }
 }
 for (name, sum) in zip(header, sums) {
     let text = sum == sum.rounded() ? String(Int(sum)) : String(sum)
     print("\(name): \(text)")
 }
