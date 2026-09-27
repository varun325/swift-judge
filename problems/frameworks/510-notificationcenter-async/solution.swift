import Foundation

extension Notification.Name {
    static let chatMessage = Notification.Name("chat.message")
}

actor Inbox {
    private(set) var texts: [String] = []
    func add(_ t: String) { texts.append(t) }
}

func broadcast(_ messages: [String]) async -> [String] {
    let center = NotificationCenter()
    let inbox = Inbox()
    let ready = AsyncStream<Void>.makeStream()
    let listener = Task {
        let stream = center.notifications(named: .chatMessage)
        ready.continuation.yield()
        for await note in stream {
            let text = note.userInfo?["text"] as? String ?? ""
            if text == "bye" { break }
            await inbox.add(text)
        }
    }
    for await _ in ready.stream { break }
    for m in messages + ["bye"] {
        center.post(name: .chatMessage, object: nil, userInfo: ["text": m])
        try? await Task.sleep(for: .milliseconds(5))
    }
    await listener.value
    return await inbox.texts
}
