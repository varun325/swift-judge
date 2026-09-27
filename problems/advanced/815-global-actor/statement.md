Declare `@globalActor actor AnalyticsActor { static let shared = AnalyticsActor() }`. Mark a class `@AnalyticsActor final class Tracker` holding `var events: [String]`, and a free function `@AnalyticsActor func log(_ e: String, to t: Tracker)`. All of it is isolated to the **same** actor, so `log` can touch `t.events` synchronously.

 Log each event (skipping empty strings) and return the tracker's events plus `"count <n>"`.
