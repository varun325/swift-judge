`stride(from:through:by:)` includes the end if it lands on it; `stride(from:to:by:)` excludes it. A negative step counts down. The result is a lazy sequence — `Array(...)` materialises it.
