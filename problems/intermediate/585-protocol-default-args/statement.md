Protocol requirements **can't** declare default argument values. Declare `protocol Notifier { func send(_ message: String, urgent: Bool) -> String }` and use a protocol extension to add the convenience `func send(_ message: String) -> String` that forwards with `urgent: false`.

 `EmailNotifier` returns `"email: <msg><!>"` and `SMSNotifier` returns `"sms: <MSG uppercased when urgent>"`. For each channel (`"email"`/`"sms"`), call both `send(message)` and `send(message, urgent: true)`.
