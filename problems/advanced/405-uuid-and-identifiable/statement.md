For each string, return `"valid <UPPERCASED uuidString>"` if `UUID(uuidString:)` accepts it, else `"invalid"`. Finally append `"unique"` if two freshly generated `UUID()`s differ, and `"<n>"` = the character count of a generated `uuidString`.

 Also declare `struct Todo: Identifiable { let id = UUID(); let title: String }` and use it once (e.g. confirm two todos with the same title have different ids) — append `"ids differ"`.
