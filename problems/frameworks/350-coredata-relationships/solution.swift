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

func first(_ entity: String, named key: String, _ value: String, in context: NSManagedObjectContext) -> NSManagedObject? {
    let r = NSFetchRequest<NSManagedObject>(entityName: entity)
    r.predicate = NSPredicate(format: "%K == %@", key, value)
    r.fetchLimit = 1
    return try? context.fetch(r).first
}

func folders(_ ops: [String]) async -> [String] {
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
        case ("folder", 2):
            NSEntityDescription.insertNewObject(forEntityName: "Folder", into: context).setValue(p[1], forKey: "name")
        case ("note", 3):
            guard let folder = first("Folder", named: "name", p[2], in: context) else { continue }
            let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: context)
            note.setValue(p[1], forKey: "title")
            note.setValue("", forKey: "body")
            note.setValue(Int64(0), forKey: "priority")
            note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
            note.setValue(folder, forKey: "folder")
        case ("delete-folder", 2): first("Folder", named: "name", p[1], in: context).map(context.delete)
        case ("delete-note", 2): first("Note", named: "title", p[1], in: context).map(context.delete)
        case ("report", 1):
            let r = NSFetchRequest<NSManagedObject>(entityName: "Folder")
            r.sortDescriptors = [NSSortDescriptor(key: "name", ascending: true)]
            for f in (try? context.fetch(r)) ?? [] {
                let count = (f.value(forKey: "notes") as? Set<NSManagedObject>)?.count ?? 0
                log.append("\(f.value(forKey: "name") as! String):\(count)")
            }
            log.append("notes \((try? context.count(for: NSFetchRequest<NSManagedObject>(entityName: "Note"))) ?? 0)")
        default: break
        }
        if context.hasChanges { try? context.save() }
    }
    withExtendedLifetime(container) {}
    return log
    }
}
