`reduce(into:)` passes the accumulator as `inout`, so you mutate it in place instead of copying a new dictionary each step (which plain `reduce` would do — O(n²) for collections).
