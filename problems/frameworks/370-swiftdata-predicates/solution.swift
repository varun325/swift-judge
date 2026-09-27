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

@MainActor func run(_ books: [[String]], _ queries: [String]) throws -> [String] {
    let container = try ModelContainer(for: Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    for b in books { context.insert(Book(title: b[0], author: b[1], rating: Int(b[2]) ?? 0)) }
    return try queries.map { q in
        let p = q.split(separator: " ").map(String.init)
        let predicate: Predicate<Book>
        switch p[0] {
        case "author":
            let text = p.count > 1 ? p[1] : ""
            predicate = #Predicate { $0.author.localizedStandardContains(text) }
        case "min":
            let n = Int(p.count > 1 ? p[1] : "") ?? 0
            predicate = #Predicate { $0.rating >= n }
        default:
            let lo = Int(p.count > 1 ? p[1] : "") ?? 0
            let hi = Int(p.count > 2 ? p[2] : "") ?? 0
            predicate = #Predicate { $0.rating >= lo && $0.rating <= hi && !$0.title.isEmpty }
        }
        let descriptor = FetchDescriptor<Book>(predicate: predicate, sortBy: [SortDescriptor(\.title)])
        let titles = try context.fetch(descriptor).map(\.title)
        return "\(titles.joined(separator: ",")) (\(try context.fetchCount(descriptor)))"
    }
}

func findBooks(_ books: [[String]], queries: [String]) async -> [String] {
    (try? await run(books, queries)) ?? ["error"]
}
