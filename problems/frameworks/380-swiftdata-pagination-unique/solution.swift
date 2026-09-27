import SwiftData
import Foundation

@Model
final class Tag {
    @Attribute(.unique) var slug: String
    var uses: Int
    init(slug: String, uses: Int) {
        self.slug = slug
        self.uses = uses
    }
}

@MainActor func run(_ incoming: [String], _ pageSize: Int) throws -> [String] {
    let container = try ModelContainer(for: Tag.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
    let context = container.mainContext
    for slug in incoming {
        let existing = try context.fetch(FetchDescriptor<Tag>(predicate: #Predicate { $0.slug == slug })).first
        context.insert(Tag(slug: slug, uses: (existing?.uses ?? 0) + 1))
        try context.save()
    }
    guard pageSize > 0 else { return [] }
    var pages: [String] = []
    var offset = 0
    while true {
        var d = FetchDescriptor<Tag>(sortBy: [SortDescriptor(\.slug)])
        d.fetchLimit = pageSize
        d.fetchOffset = offset
        let page = try context.fetch(d)
        if page.isEmpty { break }
        pages.append(page.map { "\($0.slug)=\($0.uses)" }.joined(separator: ","))
        offset += pageSize
    }
    return pages
}

func syncTags(_ incoming: [String], pageSize: Int) async -> [String] {
    (try? await run(incoming, pageSize)) ?? ["error"]
}
