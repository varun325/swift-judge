import Foundation

struct Push: Decodable {
    struct APS: Decodable {
        let title: String?
        let body: String?
        let badge: Int?
        let contentAvailable: Int?

        enum CodingKeys: String, CodingKey { case alert, badge, contentAvailable = "content-available" }
        enum AlertKeys: String, CodingKey { case title, body }

        init(from decoder: Decoder) throws {
            let c = try decoder.container(keyedBy: CodingKeys.self)
            badge = try c.decodeIfPresent(Int.self, forKey: .badge)
            contentAvailable = try c.decodeIfPresent(Int.self, forKey: .contentAvailable)
            if let text = try? c.decode(String.self, forKey: .alert) {
                title = nil
                body = text
            } else if let alert = try? c.nestedContainer(keyedBy: AlertKeys.self, forKey: .alert) {
                title = try alert.decodeIfPresent(String.self, forKey: .title)
                body = try alert.decodeIfPresent(String.self, forKey: .body)
            } else {
                title = nil
                body = nil
            }
        }
    }

    let aps: APS
    let deeplink: String?

    var isSilent: Bool { aps.contentAvailable == 1 && aps.title == nil && aps.body == nil }
}

func handlePush(_ payloads: [String]) -> [String] {
    payloads.map { json in
        guard let p = try? JSONDecoder().decode(Push.self, from: Data(json.utf8)) else { return "invalid" }
        return "\(p.aps.title ?? "-") | \(p.aps.body ?? "-") | badge \(p.aps.badge.map(String.init) ?? "-") | \(p.isSilent ? "silent" : "visible") | \(p.deeplink ?? "-")"
    }
}
