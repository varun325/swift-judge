JavaScript would just recurse over `any`; Swift makes the shape explicit with a recursive enum. A single-value container can try several types in turn, and `flatMap(\.flattened)` does the recursion.
