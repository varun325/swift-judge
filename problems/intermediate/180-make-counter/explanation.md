The returned closure captures `total` **by reference**, keeping it alive after `makeCounter` returns. Each call to `makeCounter` creates a fresh `total`, so `a` and `b` are independent.
