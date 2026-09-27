protocol Notifier {
    func send(_ message: String, urgent: Bool = false)
}
