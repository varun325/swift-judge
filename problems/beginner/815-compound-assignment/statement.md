Start with `score = 10` and `title = "Game"`. Apply events using **compound assignment**:
 - `"+n"` → `score += n`, `"-n"` → `score -= n`, `"*n"` → `score *= n`, `"/n"` → `score /= n` (skip if n is 0)
 - `"!word"` → `title += " " + word`

 Return `[title, "\(score)"]`.
