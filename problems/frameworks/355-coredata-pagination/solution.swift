import CoreData

/// Built once and shared by every container: building a model is relatively expensive.
nonisolated(unsafe) let sharedNotesModel: NSManagedObjectModel = {
    func attribute(_ name: String, _ type: NSAttributeType, optional: Bool = false) -> NSAttributeDescription {
        let a = NSAttributeDescription()
        a.name = name
        a.attributeType = type
        a.isOptional = optional
        return a
    }
    let folder = NSEntityDescription()
    folder.name = "Folder"
    folder.managedObjectClassName = NSStringFromClass(NSManagedObject.self)
    let note = NSEntityDescription()
    note.name = "Note"
    note.managedObjectClassName = NSStringFromClass(NSManagedObject.self)

    let notes = NSRelationshipDescription()
    notes.name = "notes"
    notes.destinationEntity = note
    notes.minCount = 0
    notes.maxCount = 0            // to-many
    notes.isOptional = true
    notes.deleteRule = .cascadeDeleteRule
    let folderRel = NSRelationshipDescription()
    folderRel.name = "folder"
    folderRel.destinationEntity = folder
    folderRel.maxCount = 1
    folderRel.isOptional = true
    folderRel.deleteRule = .nullifyDeleteRule
    notes.inverseRelationship = folderRel
    folderRel.inverseRelationship = notes

    folder.properties = [attribute("name", .stringAttributeType), notes]
    note.properties = [
        attribute("title", .stringAttributeType),
        attribute("body", .stringAttributeType),
        attribute("priority", .integer64AttributeType),
        attribute("created", .dateAttributeType),
        folderRel,
    ]
    let model = NSManagedObjectModel()
    model.entities = [folder, note]
    return model
}()

/// A fresh in-memory Core Data stack (no .xcdatamodeld needed) that shares the one model.
func makeContainer() -> NSPersistentContainer {
    let container = NSPersistentContainer(name: "Notes", managedObjectModel: sharedNotesModel)
    let description = NSPersistentStoreDescription()
    description.type = NSInMemoryStoreType
    container.persistentStoreDescriptions = [description]
    container.loadPersistentStores { _, error in precondition(error == nil) }
    return container
}

import Foundation

func pages(total: Int, pageSize: Int) async -> [String] {
    let container = makeContainer()   // keep the container alive: the context doesn't own it
    // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
    // private-queue context and do ALL work inside `await context.perform`, which runs on the
    // context's own queue (performAndWait would run inline on the caller's thread — here, main).
    let context = container.newBackgroundContext()
    return await context.perform {
    for i in stride(from: 1, through: total, by: 1) {
        let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
        note.setValue(String(format: "n%03d", i), forKey: "title")
        note.setValue("", forKey: "body")
        note.setValue(Int64(0), forKey: "priority")
        note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
    }
    try? context.save()
    let countRequest = NSFetchRequest<NSManagedObject>(entityName: "Note")
    var log = ["count \((try? context.count(for: countRequest)) ?? 0)"]
    guard pageSize > 0 else { return log }
    var page = 0
    while true {
        let r = NSFetchRequest<NSManagedObject>(entityName: "Note")
        r.sortDescriptors = [NSSortDescriptor(key: "title", ascending: true)]
        r.fetchLimit = pageSize
        r.fetchOffset = page * pageSize
        let items = ((try? context.fetch(r)) ?? []).compactMap { $0.value(forKey: "title") as? String }
        guard let firstTitle = items.first, let lastTitle = items.last else { break }
        log.append("page \(page): \(firstTitle)..\(lastTitle)")
        page += 1
    }
    withExtendedLifetime(container) {}
    return log
    }
}
