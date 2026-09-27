import Foundation

struct AASA: Decodable {
    struct Applinks: Decodable { let details: [Detail] }
    struct Detail: Decodable { let components: [Component] }
    struct Component: Decodable {
        let path: String
        let exclude: Bool?
        enum CodingKeys: String, CodingKey { case path = "/", exclude }
    }
    let applinks: Applinks
}

func wildcardMatches(_ pattern: String, _ text: String) -> Bool {
    let p = Array(pattern), t = Array(text)
    var memo: [[Bool?]] = Array(repeating: Array(repeating: nil, count: t.count + 1), count: p.count + 1)
    func match(_ i: Int, _ j: Int) -> Bool {
        if let cached = memo[i][j] { return cached }
        let result: Bool
        if i == p.count { result = j == t.count }
        else if p[i] == "*" { result = match(i + 1, j) || (j < t.count && match(i, j + 1)) }
        else { result = j < t.count && (p[i] == "?" || p[i] == t[j]) && match(i + 1, j + 1) }
        memo[i][j] = result
        return result
    }
    return match(0, 0)
}

func matchLinks(aasa: String, urls: [String]) -> [String] {
    guard let file = try? JSONDecoder().decode(AASA.self, from: Data(aasa.utf8)) else { return urls.map { _ in "web" } }
    let components = file.applinks.details.flatMap(\.components)
    return urls.map { url in
        guard let path = URLComponents(string: url)?.path else { return "web" }
        guard let hit = components.first(where: { wildcardMatches($0.path, path) }) else { return "web" }
        return hit.exclude == true ? "web" : "app"
    }
}
