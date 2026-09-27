Swift's standard library has no heap. Write `struct Heap<Element>` with a stored `areSorted: (Element, Element) -> Bool` comparator, `insert`, `popTop() -> Element?`, `peek` and `count` (sift up / sift down).

 Use a **min-heap of size k** to find the k-th largest element (1 ≤ k ≤ count).
