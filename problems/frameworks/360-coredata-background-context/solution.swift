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

func importInBackground(_ titles: [String]) async -> [String] {
    let container = makeContainer()
    container.viewContext.automaticallyMergesChangesFromParent = true
    let background = container.newBackgroundContext()
    let ids: [NSManagedObjectID] = await background.perform {
        let notes = titles.map { title -> NSManagedObject in
            let note = NSEntityDescription.insertNewObject(forEntityName: "Note", into: background)
            note.setValue(title, forKey: "title")
            note.setValue("", forKey: "body")
            note.setValue(Int64(0), forKey: "priority")
            note.setValue(Date(timeIntervalSince1970: 0), forKey: "created")
            return note
        }
        try? background.save()
        return notes.map(\.objectID)
    }
    let main = container.viewContext
    return await main.perform {
        let count = (try? main.count(for: NSFetchRequest<NSManagedObject>(entityName: "Note"))) ?? 0
        let first = ids.first.flatMap { try? main.existingObject(with: $0).value(forKey: "title") as? String } ?? "-"
        return ["background saved \(ids.count)", "main sees \(count)", first]
    }
}
