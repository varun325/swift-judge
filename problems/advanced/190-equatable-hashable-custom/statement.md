Email identity rules: case-insensitive; in the local part (before `@`) dots are ignored and anything after a `+` is ignored. So `"J.Doe+news@Mail.com"` equals `"jdoe@mail.com"`.

 Write `struct Email: Hashable` storing the **original** string, but implement `==` and `hash(into:)` on the **normalised** form yourself. Return how many distinct emails there are (a `Set<Email>`).
