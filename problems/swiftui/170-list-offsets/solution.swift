import SwiftUI

func editList(_ items: [String], _ edits: [String]) async -> [String] {
    var list = items
    for edit in edits {
        let p = edit.split(separator: " ")
        let numbers = p.dropFirst().compactMap { Int($0) }
        if p[0] == "del" {
            list.remove(atOffsets: IndexSet(numbers.filter { list.indices.contains($0) }))
        } else if let destination = numbers.last, numbers.count >= 2 {
            let sources = IndexSet(numbers.dropLast().filter { list.indices.contains($0) })
            list.move(fromOffsets: sources, toOffset: min(destination, list.count))
        }
    }
    return list
}
