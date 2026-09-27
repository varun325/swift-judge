Swiftful's *Core Data relationships, predicates, and delete rules*. The model has `Folder.notes` (to-many, **cascade**) and `Note.folder` (to-one, **nullify**). Ops:
 - `folder <name>`, `note <title> <folderName>` (set `note.folder`; the inverse updates automatically)
 - `delete-folder <name>` (notes cascade), `delete-note <title>` (folder keeps existing)
 - `report` → `"<folder>:<note count>"` per folder (sorted) + `"notes <total>"`, via a fetch count
