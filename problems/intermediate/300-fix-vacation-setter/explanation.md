Any get/set pair should satisfy the round trip `x.p = v; x.p == v`. The setter receives `newValue`; solving `allowed - taken = newValue` gives `allowed = taken + newValue`.
