enum Event {
    case login(user: String)
    case purchase(item: String, cents: Int)
    case logout
}

let events: [Event] = [.login(user: "ana"), .purchase(item: "book", cents: 1299), .purchase(item: "pen", cents: 150), .logout]

var total = 0
for event in events {
    if case .purchase(_, let cents) = event {
        total += cents
    }
}
print("spent \(total)")

for case .purchase(let item, let cents) in events where cents > 1000 {
    print("big: \(item)")
}

if case .login(let user) = events[0] {
    print(user.uppercased())
}
print(events.count)
