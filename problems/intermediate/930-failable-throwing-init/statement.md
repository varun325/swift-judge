Write `struct Email` two ways:
 - `init?(_ raw: String)` — returns nil if invalid
 - `init(validating raw: String) throws` — throws `EmailError.missingAt`, `.emptyUser` or `.emptyDomain`

 Valid = exactly one `@`, non-empty parts. For each input return `"<email> ok"` using the failable init, else the error case name from the throwing init.
