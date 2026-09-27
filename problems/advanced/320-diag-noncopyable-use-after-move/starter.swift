struct Token: ~Copyable { let id: Int }

let a = Token(id: 1)
let b = a
print(b.id)
