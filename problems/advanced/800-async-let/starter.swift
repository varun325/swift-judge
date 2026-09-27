func loadProfile(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "profile \(id)" }
func loadFeed(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "feed \(id)" }
func loadNotifications(_ id: Int) async -> String { try? await Task.sleep(for: .milliseconds(300)); return "notifications \(id)" }

func dashboard(userID: Int) async -> [String] {
    let profile = await loadProfile(userID)
    let feed = await loadFeed(userID)
    let notifications = await loadNotifications(userID)
    return [profile, feed, notifications]
}
