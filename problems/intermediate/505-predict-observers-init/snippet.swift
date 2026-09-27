struct Thermostat {
    var target: Int {
        willSet { print("will", target, "->", newValue) }
        didSet { print("did", oldValue, "->", target) }
    }
    init(target: Int) {
        self.target = target
        print("init done")
    }
    mutating func bump() { target += 1 }
}

var t = Thermostat(target: 20)
t.target = 22
t.bump()
let same = t.target
t.target = same
