Write a generic `func memoizeRecursive<In: Hashable, Out>(_ body: @escaping ((In) -> Out, In) -> Out) -> (In) -> Out` that caches results in a captured dictionary and lets `body` call the memoised function recursively.

 Use it for Fibonacci and return `[fib(n), callCount]`, where `callCount` counts how many times `body` actually ran (should be `n + 1` for `n ≥ 1`, thanks to the cache). `n ≤ 90`.
