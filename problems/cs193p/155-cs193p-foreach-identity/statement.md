L10: a `ForEach` identifier must be **unique**, **stable** (the same item keeps the same id across updates) and **Hashable**. Each snapshot is a list of `"<id>:<content>"` items, representing the list at successive moments. Report problems:
 - `"duplicate <id> in snapshot <n>"` for repeated ids within a snapshot
 - `"unstable <content>"` when the same content appears with a **different** id in a later snapshot (e.g. using array indices as ids)

 Return the problems sorted, or `["ok"]`.
