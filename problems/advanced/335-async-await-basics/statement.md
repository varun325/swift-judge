`func fetchUser(_ id: Int) async -> String` (given) sleeps briefly and returns `"user<id>"`. Your `fetchAll` must return users for **all** ids in input order, but run the fetches **concurrently** — the judge's time limit is tight enough that doing them one by one fails for long inputs.

 Use a `TaskGroup` that returns `(index, user)` pairs and reassemble in order.
