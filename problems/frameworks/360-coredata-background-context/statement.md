Swiftful's *Multi-threading* + Core Data. Import notes on a **background context** (`container.newBackgroundContext()` + `await context.perform { … }`), save it, and verify the **view context** sees them because `viewContext.automaticallyMergesChangesFromParent = true`. Pass only `NSManagedObjectID`s (Sendable) between contexts — never managed objects.

 Return `["background saved <n>", "main sees <n>", first imported title fetched on main via its objectID]`.
