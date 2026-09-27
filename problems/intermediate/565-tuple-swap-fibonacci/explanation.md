The right-hand tuple is fully evaluated **before** assignment, so `(x, y) = (y, x + y)` uses the old values of both. `var (x, y) = (0, 1)` declares two variables at once.
