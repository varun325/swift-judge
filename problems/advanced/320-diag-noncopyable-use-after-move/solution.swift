struct Token: ~Copyable { let id: Int }

func demo() {
    let a = Token(id: 1)
    let b = a
    print(a.id)
    print(b.id)
}
demo()
