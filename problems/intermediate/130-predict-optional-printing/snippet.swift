let a: Int? = 5
let b: Int? = nil
let c: Int! = 7
print(a as Any)
print(b as Any)
print(a ?? 0, b ?? 0)
print(c + 1)
let d = c
print(type(of: d))
print(a.map { $0 * 2 } as Any, b.map { $0 * 2 } as Any)
