Swiftful's *Core Data with MVVM*. The starter builds an **in-memory** Core Data stack in code (entities `Note` and `Folder`). Implement ops against `container.viewContext`:
 - `add <title> <priority>` → insert a `Note` (use `NSEntityDescription.insertNewObject` / `setValue`)
 - `rename <old> <new>`, `delete <title>` (first match)
 - `list` → fetch all notes sorted by priority **descending** then title, logging `"title(p)"` joined by `,`

 Save after every change.
