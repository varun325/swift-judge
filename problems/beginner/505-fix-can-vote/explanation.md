`x ? true : false` is always just `x` (and `x ? false : true` is `!x`). Off-by-one boundaries are the classic comparison bug — test the exact boundary value.
