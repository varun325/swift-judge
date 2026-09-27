import SwiftData
import Foundation

@Model
final class Author {
    var name: String
    @Relationship(deleteRule: .cascade, inverse: \Book.author) var books: [Book] = []
    init(name: String) { self.name = name }
}

@Model
final class Book {
    var title: String
    var author: Author?
    init(title: String) { self.title = title }
}

@MainActor func run(_ ops: [String]) throws -> [String] {
    let container = try ModelContainer(for: Author.self, Book.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    var log: [String] = []
    func author(_ name: String) throws -> Author? { try context.fetch(FetchDescriptor<Author>(predicate: #Predicate { $0.name == name })).first }
    func book(_ title: String) throws -> Book? { try context.fetch(FetchDescriptor<Book>(predicate: #Predicate { $0.title == title })).first }
    for op in ops {
        let p = op.split(separator: " ").map(String.init)
        switch (p.first ?? "", p.count) {
        case ("author", 2): context.insert(Author(name: p[1]))
        case ("book", 3):
            guard let a = try author(p[2]) else { break }
            let b = Book(title: p[1])
            context.insert(b)
            a.books.append(b)
        case ("delete-author", 2): if let a = try author(p[1]) { context.delete(a) }
        case ("delete-book", 2): if let b = try book(p[1]) { context.delete(b) }
        case ("report", 1):
            for a in try context.fetch(FetchDescriptor<Author>(sortBy: [SortDescriptor(\.name)])) { log.append("\(a.name):\(a.books.count)") }
            log.append("books \(try context.fetchCount(FetchDescriptor<Book>()))")
        default: break
        }
        try context.save()
    }
    return log
}

func libraryGraph(_ ops: [String]) async -> [String] {
    (try? await run(ops)) ?? ["error"]
}
