Swiftful's *Firestore Pagination*. Offsets break when new items arrive; **cursors** don't. Posts are `[id, createdAt]` (integers). Sort by `createdAt` descending then id ascending, and page with a cursor: each page takes up to `pageSize` items strictly **after** the last item of the previous page (compare the `(createdAt, id)` key). Return pages as ids joined by `,`, then `"end"`.

 To prove cursor stability, after producing the first page insert a **new** post `["new", <max createdAt + 1>]` (it sorts first) — later pages must not repeat or skip items.
