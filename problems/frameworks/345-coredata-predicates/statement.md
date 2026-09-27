Insert notes `[title, body, priority]`, then run each query and return matching titles (sorted) joined by `,`:
 - `search <text>` → `title CONTAINS[cd] %@ OR body CONTAINS[cd] %@`
 - `between <lo> <hi>` → `priority BETWEEN {lo, hi}` (use `%@` with an array)
 - `in <a,b,c>` → `title IN %@`
 - `urgent` → `priority >= 3 AND NOT (title BEGINSWITH[c] 'draft')`

 Always pass values with `%@` — never interpolate them into the format string.
