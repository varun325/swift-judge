`a?.b?.c.count` short-circuits to `nil` at the first missing link, and the result is **one level** of optional (`Int?`), however many `?`s are in the chain.
