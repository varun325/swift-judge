protocol Notifier {
    func send(_ message: String, urgent: Bool) -> String
}

extension Notifier {
    func send(_ message: String) -> String { send(message, urgent: false) }
}

struct EmailNotifier: Notifier {
    func send(_ message: String, urgent: Bool) -> String { "email: \(message)\(urgent ? "!" : "")" }
}

struct SMSNotifier: Notifier {
    func send(_ message: String, urgent: Bool) -> String { "sms: \(urgent ? message.uppercased() : message)" }
}

func notify(_ channels: [String], message: String) -> [String] {
    channels.flatMap { ch -> [String] in
        let n: any Notifier = ch == "sms" ? SMSNotifier() : EmailNotifier()
        return [n.send(message), n.send(message, urgent: true)]
    }
}
