let a = [1, 2, 3]
var b = a
b[0] = 99
print(a[0], b[0])
print("👨‍👩‍👧".count, "👨‍👩‍👧".utf16.count)
print(Int8.max &+ 1)
print(-7 % 3, 7.5.truncatingRemainder(dividingBy: 2))
print([3, 1, 2].sorted() == [1, 2, 3], [1, 2].lexicographicallyPrecedes([1, 3]))
let optionalOptional: Int?? = .some(nil)
print(optionalOptional == nil, optionalOptional! == nil)
print(String(describing: 0.1 + 0.2))
