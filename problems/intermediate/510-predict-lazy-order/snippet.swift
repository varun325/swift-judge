func log(_ s: String) -> Int { print("computing", s); return s.count }

struct Report {
    let eager: Int = log("eager")
    lazy var deferred: Int = log("lazy")
    var computed: Int { log("computed") }
}

print("start")
var r = Report()
print("created")
print(r.deferred)
print(r.deferred)
print(r.computed)
print(r.computed)
