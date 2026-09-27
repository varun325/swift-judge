import Foundation

func searchURL(query: String, page: Int, filters: [String]) -> String {
    var c = URLComponents()
    c.scheme = "https"
    c.host = "api.example.com"
    c.path = "/v1/search"
    var items = [URLQueryItem(name: "q", value: query)]
    if page > 1 { items.append(URLQueryItem(name: "page", value: String(page))) }
    items += filters.map { URLQueryItem(name: "filter", value: $0) }
    c.queryItems = items
    return c.url?.absoluteString ?? "invalid"
}
