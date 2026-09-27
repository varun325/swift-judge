Model `enum OrderStatus { case placed, paid, shipped, delivered, cancelled }` with a `mutating func handle(_ event: String) -> Bool` implementing the rules:
 - `pay`: placed → paid · `ship`: paid → shipped · `deliver`: shipped → delivered
 - `cancel`: placed or paid → cancelled
 - anything else is rejected (status unchanged, returns `false`)

 Return `"<event>: <status>"` or `"<event>: rejected"` for each event, starting from `.placed`.
