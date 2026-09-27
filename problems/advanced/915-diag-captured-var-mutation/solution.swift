func work() async {
    var count = 0
    Task { count += 1 }
    count += 1
    print(count)
}
