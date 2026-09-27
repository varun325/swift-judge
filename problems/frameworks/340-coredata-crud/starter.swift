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

func notesCRUD(_ ops: [String]) async -> [String] {
    let container = makeContainer()   // keep the container alive: the context doesn't own it
    // Contexts are confined to their queue, and the judge calls you on the main thread, so use a
    // private-queue context and do ALL work inside `await context.perform`, which runs on the
    // context's own queue (performAndWait would run inline on the caller's thread — here, main).
    let context = container.newBackgroundContext()
    return await context.perform {
        var log: [String] = []
        // implement the ops (inside perform: the context's own queue)
        withExtendedLifetime(container) {}
        return log
    }
}
