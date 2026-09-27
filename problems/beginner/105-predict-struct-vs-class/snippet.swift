struct PointS { var x = 0 }
final class PointC { var x = 0 }

var a = PointS()
var b = a
b.x = 10

let c = PointC()
let d = c
d.x = 10

print(a.x, b.x)
print(c.x, d.x)
print(c === d)
