Group words by length (as a String key) using a single `reduce(into:)`, keeping first-seen order within each group.

 ```swift
 lengthHistogram(["hi", "yo", "hey"])   // ["2": ["hi", "yo"], "3": ["hey"]]
 ```
