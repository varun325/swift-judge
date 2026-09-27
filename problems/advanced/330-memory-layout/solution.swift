struct Loose { let flag: Bool; let value: Int64; let small: Bool }
struct Packed { let value: Int64; let flag: Bool; let small: Bool }

func info<T>(_: T.Type) -> [Int] {
    [MemoryLayout<T>.size, MemoryLayout<T>.stride, MemoryLayout<T>.alignment]
}

func layouts() -> [[Int]] {
    [info(Loose.self), info(Packed.self), info(Int.self), info(Bool.self), info(String?.self), info(AnyObject.self)]
}
