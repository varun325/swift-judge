import SwiftData
import Foundation

@Model
final class Book {
    var title: String
    var author: String
    var rating: Int
    init(title: String, author: String, rating: Int) {
        self.title = title
        self.author = author
        self.rating = rating
    }
}

@MainActor func run(_ ops: [String]) throws -> [String] {
    let container = try ModelContainer(for: Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    var log: [String] = []
    func find(_ title: String) throws -> Book? {
        var d = FetchDescriptor<Book>(predicate: #Predicate { $0.title == title })
        d.fetchLimit = 1
        return try context.fetch(d).first
    }
    for op in ops {
        let p = op.split(separator: " ", maxSplits: 1).map(String.init)
        let arg = p.count > 1 ? p[1] : ""
        switch p[0] {
        case "add":
            let f = arg.split(separator: "|").map(String.init)
            if f.count == 3 { context.insert(Book(title: f[0], author: f[1], rating: Int(f[2]) ?? 0)) }
        case "rate":
            let f = arg.split(separator: " ").map(String.init)
            if f.count == 2, let book = try find(f[0]) { book.rating = Int(f[1]) ?? book.rating }
        case "delete":
            if let book = try find(arg) { context.delete(book) }
        default:
            let d = FetchDescriptor<Book>(sortBy: [SortDescriptor(\.rating, order: .reverse), SortDescriptor(\.title)])
            log.append(try context.fetch(d).map { "\($0.title)(\($0.rating))" }.joined(separator: ","))
        }
    }
    return log
}

func booksCRUD(_ ops: [String]) async -> [String] {
    (try? await run(ops)) ?? ["error"]
}
