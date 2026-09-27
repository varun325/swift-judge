final class Box<T> { var value: T; init(_ v: T) { value = v } }

func memoizeRecursive<In: Hashable, Out>(_ body: @escaping ((In) -> Out, In) -> Out) -> (In) -> Out {
    let cache = Box<[In: Out]>([:])
    let recurse = Box<((In) -> Out)?>(nil)
    let memo: (In) -> Out = { input in
        if let hit = cache.value[input] { return hit }
        let result = body(recurse.value!, input)
        cache.value[input] = result
        return result
    }
    recurse.value = memo
    return memo
}

func memoDemo(_ n: Int) -> [Int] {
    let calls = Box(0)
    let fib: (Int) -> Int = memoizeRecursive { fib, k in
        calls.value += 1
        return k < 2 ? k : fib(k - 1) + fib(k - 2)
    }
    return [fib(n), calls.value]
}
