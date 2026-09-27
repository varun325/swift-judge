Swiftful's *NavigationStack*. Model routes as `enum Route: Hashable, Codable { case profile(id: Int), settings, detail(String) }` and drive a `NavigationPath`:
 - `push profile 7`, `push settings`, `push detail x` · `pop` (if not empty) · `root` (clear)
 - `save` — encode `path.codable` to JSON and restore a new path from it, logging `"restored <count>"`

 Log `"depth <n>"` after each other command.
