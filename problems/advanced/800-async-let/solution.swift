func loadProfile(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "profile \(id)" }
func loadFeed(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "feed \(id)" }
func loadNotifications(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "notifications \(id)" }

func dashboard(userID: Int) async -> [String] {
    async let profile = loadProfile(userID)
    async let feed = loadFeed(userID)
    async let notifications = loadNotifications(userID)
    return await [profile, feed, notifications]
}
