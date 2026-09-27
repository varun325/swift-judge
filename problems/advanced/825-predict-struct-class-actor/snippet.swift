struct S { var n = 0 }
final class C { var n = 0 }
actor A {
    var n = 0
    func bump() -> Int { n += 1; return n }
}

var s1 = S(); var s2 = s1; s2.n = 5
let c1 = C(); let c2 = c1; c2.n = 5
let a1 = A(); let a2 = a1
_ = await a2.bump()
print(s1.n, s2.n)
print(c1.n, c2.n, c1 === c2)
print(await a1.n, await a1.bump(), a1 === a2)
