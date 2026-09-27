L12 builds one sheet that both **creates** a new game and **edits** an existing one, binding to an `@Observable` game with `@Bindable`. Model `@Observable final class GameConfig { var name; var pegChoices: [String] }` with rules: 2…6 choices, no duplicates, name non-empty. The editor works on a **draft copy**; `save` validates and either appends (create) or writes back (edit); `cancel` discards.

 Actions: `new`, `edit <name>`, `name <n>`, `addPeg <c>`, `removePeg <c>`, `save`, `cancel`. Log after `save` (`"saved"` or `"invalid: <reason>"`) and at the end list games as `"<name>(<pegs>)"`.
