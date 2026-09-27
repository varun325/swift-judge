Implement on `Collection`:
 - `func windows(ofCount k: Int) -> [SubSequence]` — every contiguous slice of length k (none if k > count)
 - `func adjacentPairs() -> [(Element, Element)]`

 Return `[moving sums over windows(ofCount: window), differences b - a over adjacentPairs]`.
