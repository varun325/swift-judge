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

func queryNotes(_ notes: [[String]], queries: [String]) async -> [String] {
    let container = makeContainer()   // keep the container alive: the context doesn't own it
    // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
    // private-queue context and do ALL work inside `await context.perform`, which runs on the
    // context's own queue (performAndWait would run inline on the caller's thread — here, main).
    let context = container.newBackgroundContext()
    return await context.perform {
    for n in notes {
        let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
        note.setValue(n[0], forKey: "title")
        note.setValue(n[1], forKey: "body")
        note.setValue(Int64(n[2]) ?? 0, forKey: "priority")
        note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
    }
    try? context.save()
    return queries.map { q in
        let p = q.split(separator: " ", maxSplits: 1).map(String.init)
        let arg = p.count > 1 ? p[1] : ""
        let predicate: NSPredicate
        switch p[0] {
        case "search": predicate = NSPredicate(format: "title CONTAINS[cd] %@ OR body CONTAINS[cd] %@", arg, arg)
        case "between":
            let bounds = arg.split(separator: " ").compactMap { Int($0) }
            predicate = NSPredicate(format: "priority BETWEEN %@", bounds.count == 2 ? bounds : [0, 0])
        case "in": predicate = NSPredicate(format: "title IN %@", arg.split(separator: ",").map(String.init))
        default: predicate = NSPredicate(format: "priority >= 3 AND NOT (title BEGINSWITH[c] %@)", "draft")
        }
        let request = NSFetchRequest<NSManagedObject>(entityName: "Note")
        request.predicate = predicate
        let titles = ((try? context.fetch(request)) ?? []).compactMap { $0.value(forKey: "title") as? String }
        return withExtendedLifetime(container) { titles.sorted().joined(separator: ",") }
    }
    }
}
