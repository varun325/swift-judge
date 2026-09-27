The heart of CodeBreaker's model: `func match(against master: Code) -> [Match]`. For a guess:
 - **exact** = right peg in the right position
 - **inexact** = right peg in the wrong position — but each master peg can only be matched **once** (duplicates make this tricky!)

 Implement it first with loops, then refactor with `map`/`zip` as L5 does. Return `"<exact>E <inexact>I"` for each guess. Empty strings are "missing" pegs and never match.
