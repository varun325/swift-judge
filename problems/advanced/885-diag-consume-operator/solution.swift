func demo() {
    let data = [1, 2, 3]
    let moved = consume data
    print(data.count)
    print(moved.count)
}
demo()
