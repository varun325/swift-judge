Validate in this order, returning the **first** failure message:
 1. username present and 3–16 characters → else `"bad username"`
 2. age present, an integer, and ≥ 13 → else `"bad age"`
 3. email present and contains exactly one `@` with text on both sides → else `"bad email"`

 Otherwise return `"welcome <username>"`. Use a `guard` for each rule so the happy path stays unindented.
