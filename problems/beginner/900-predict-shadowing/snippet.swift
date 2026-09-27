let name: String? = "Ana"
if let name {
    print(name, type(of: name))
}
print(name ?? "none", type(of: name))
let count = 3
do {
    let count = count * 2
    print(count)
}
print(count)
func greet(_ name: String?) {
    guard let name else { print("no name"); return }
    print("hi \(name)")
}
greet(nil)
greet(name)
