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

func fetchNotes(_ context: NSManagedObjectContext, title: String? = nil) -> [NSManagedObject] {
    let request = NSFetchRequest<NSManagedObject>(entityName: "Note")
    if let title { request.predicate = NSPredicate(format: "title == %@", title) }
    request.sortDescriptors = [NSSortDescriptor(key: "priority", ascending: false), NSSortDescriptor(key: "title", ascending: true)]
    return (try? context.fetch(request)) ?? []
}

func notesCRUD(_ ops: [String]) async -> [String] {
    let container = makeContainer()   // keep the container alive: the context doesn't own it
    // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
    // private-queue context and do ALL work inside `await context.perform`, which runs on the
    // context's own queue (performAndWait would run inline on the caller's thread — here, main).
    let context = container.newBackgroundContext()
    return await context.perform {
    var log: [String] = []
    for op in ops {
        let p = op.split(separator: " ").map(String.init)
        switch (p.first ?? "", p.count) {
        case ("add", 3):
            let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
            note.setValue(p[1], forKey: "title")
            note.setValue("", forKey: "body")
            note.setValue(Int64(p[2]) ?? 0, forKey: "priority")
            note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
        case ("rename", 3): fetchNotes(context, title: p[1]).first?.setValue(p[2], forKey: "title")
        case ("delete", 2): fetchNotes(context, title: p[1]).first.map(context.delete)
        case ("list", 1):
            log.append(fetchNotes(context).map { "\($0.value(forKey: "title") as! String)(\($0.value(forKey: "priority") as! Int64))" }.joined(separator: ","))
        default: break
        }
        if context.hasChanges { try? context.save() }
    }
    withExtendedLifetime(container) {}
    return log
    }
}
